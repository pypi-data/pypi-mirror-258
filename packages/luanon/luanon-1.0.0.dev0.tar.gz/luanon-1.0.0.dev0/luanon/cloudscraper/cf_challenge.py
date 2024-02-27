"""
    Tác giả: GnU
    Ngày tạo: 11/06/2023
    ©2023 LuaNonTeam
"""

import json
import time

import requests

from dataclasses import dataclass

from . import cf_exception, cf_util
from .cf_body import CfRequestBody, CfResponseBody
from .jsdom_runtime import JSDomRuntime


@dataclass
class CfChallenge:
    __slots__ = ["cloudflare_scraper", "session", "response"]
    cloudflare_scraper: "CloudflareScraper"
    session: requests.Session
    response: requests.Response | None

    @classmethod
    def render(cls, cloudflare_scraper: "CloudflareScraper", session: requests.Session, response: requests.Response) -> "CfChallenge":
        return cls(cloudflare_scraper, session, response)

    @property
    def is_solved(self) -> bool:
        return cf_util.check_cloudflare_enabled(self.response)

    def solve_challenge(self) -> None:
        # Khởi tạo
        jsdom_runtime = JSDomRuntime("jsdom_runtime/jsdom_runtime.js")
        jsdom_runtime.eval("""
            const requests_list = [];
            
            class CustomResourceLoader extends jsdom.ResourceLoader {
                fetch(url, options) {
                    requests_list.push({
                        url,
                        method: "GET",
                        body: null
                    });
                    //let not_allowed = ["https://challenges.cloudflare.com/turnstile/v0/"];
                    //for (let block of not_allowed) {
                    //    if (url.includes(block)) {
                    //        return null;
                    //    }
                    //}
                    return super.fetch(url, options);
                }
            }
            
            const loader = new CustomResourceLoader({
                userAgent: `""" + self.cloudflare_scraper.headers["User-Agent"] + """`
            });
            
            const dom = new jsdom.JSDOM(
                `""" + open("assets/index.html").read() + """`,
                {
                    url: `""" + cf_util.get_base_url(self.response.url) + """`,
                    referer: `""" + cf_util.get_base_url(self.response.url) + """`,
                    contentType: "text/html",
                    includeNodeLocations: true,
                    runScripts: "dangerously",
                    pretendToBeVisual: true,
                    resources: loader,
                    allowSpecialUseDomain: true,
                    rejectPublicSuffixes: false,
                    beforeParse: function (window) {
                        window.XMLHttpRequest = class CustomXMLHttpRequest extends window.XMLHttpRequest {
                            open(method, url) {
                                this._url = url;
                                this._method = method;
                                super.open(method, url);
                            }
                            send(data) {
                                if (this._method === "POST") {
                                    requests_list.push({
                                        url: this._url,
                                        method: this._method,
                                        data: data
                                    });
                                    super.send(data);
                                } else {
                                    super.send(data);
                                }
                            }
                        };
                    }
                }
            );
            
            const ctx = dom.getInternalVMContext();
        """)
        _cf_chl_opt, cpo_url = cf_util.get_init_data(self.response)
        print(_cf_chl_opt)
        assert _cf_chl_opt["cType"] == "managed", "Oops"
        jsdom_runtime.eval(f"ctx.window._cf_chl_opt={json.dumps(_cf_chl_opt)};")

        base_challenge = self.session.get(cpo_url)
        init_script = cf_util.clean_script(base_challenge.text, "base")
        f = open("a.js", "w")
        f.write(init_script)
        f.close()
        secret_key = cf_util.get_secret_key(base_challenge, _cf_chl_opt)

        cf_request_body = CfRequestBody(secret_key)
        cf_response_body = CfResponseBody(_cf_chl_opt["cRay"])

        jsdom_runtime.eval(f"vm.runInContext(`{open("a.js", "r").read()}`, ctx)")
        input(">>> ")

        retries = 0
        max_retries = self.cloudflare_scraper.cf_max_retries * 5
        luanon_body = None

        while retries < max_retries and not luanon_body:
            requests_list, _, _ = jsdom_runtime.eval("JSON.stringify(requests_list)")
            requests_list = json.loads(requests_list)
            print(requests_list)
            for request in requests_list:
                if request["method"] == "POST":
                    if all(x in request["url"] for x in ["/cdn-cgi/challenge-platform/", _cf_chl_opt["cType"]]):
                        luanon_body = request["data"]
            if not luanon_body:
                time.sleep(1)
            retries += 1
        else:
            raise cf_exception.CloudflareChallengeError("Không lấy được luanon_body")

        luanon_headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "CF-Challenge": _cf_chl_opt["cHash"],
            "Content-Length": str(len(luanon_body)),
            "Origin": cf_util.get_base_url(base_challenge.url)[:-1],
            "Referer": cf_util.get_base_url(base_challenge.url),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        luanon_challenge = self.session.post(server_post_url, data=luanon_body, headers=luanon_headers)
        print(len(luanon_challenge.text), luanon_challenge.text)
        luanon_challenge_body = cf_response_body.decode(luanon_challenge.text)
        print(len(luanon_challenge_body), luanon_challenge_body)

        exit()

        # while True:
        #     requests_list, err, log = jsdom_runtime.eval("JSON.stringify(requests_list.shift())", timeout=60)
        #     try:
        #         requests_list = json.loads(requests_list)
        #         print(json.dumps(cf_request_body.decode(requests_list["data"].split("=", 1)[-1]), indent=4))
        #     except:
        #         pass
        #     print(requests_list, err, log)
        #     time.sleep(1)

        match _cf_chl_opt["cType"]:
            case "managed":
                pass
            case _:
                # Hmm
                return None
