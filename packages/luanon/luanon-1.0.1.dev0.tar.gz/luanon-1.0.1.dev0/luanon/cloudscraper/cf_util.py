"""
    Tác giả: GnU
    Ngày tạo: 11/06/2023
    ©2023 LuaNonTeam
"""

import base64
import json
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from luanon.cloudscraper import cf_exception
from luanon.js_runtime import JSRuntime


def get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"


def urljoin(base_url: str, *args: str):
    for url in args:
        base_url = base_url.rstrip("/") + "/" + url.strip("/")
    return base_url


def check_cloudflare_enabled(response: requests.Response) -> bool:
    if '<span class="cf-code-label">Error code <span>1020</span></span>' in response.text:
        raise cf_exception.CloudflareAccessDenied()
    if (response.headers.get("server") == "cloudflare"
            and response.status_code in [503, 403]):
        return True
    return False


def get_init_data(response: requests.Response) -> tuple[dict, str] | None:
    soup = BeautifulSoup(response.content, features="html.parser")
    script = soup.find("script").text
    print(script)

    # window._cf_chl_opt={...};
    _cf_chl_opt = re.search(r"window\._cf_chl_opt=({.+?});", script)
    if not isinstance(_cf_chl_opt, re.Match):
        return None

    js_runtime = JSRuntime()
    _cf_chl_opt, _, _ = js_runtime.eval(f"JSON.stringify({_cf_chl_opt.group(1)})")
    js_runtime.close()

    quote = r"('|\")"
    # cpo.src = '/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1?ray=...';
    cpo_url = re.search(rf"cpo\.src\s*=\s*{quote}(.+?){quote};", script)
    if not isinstance(cpo_url, re.Match):
        return None

    # Group 1 -> ' | "
    # Group 2 -> /cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1?ray=...
    # Group 3 -> ' | "
    cpo_url = urljoin(get_base_url(response.url), cpo_url.group(2))

    return json.loads(_cf_chl_opt), cpo_url


def get_secret_key(response: requests.Response, _cf_chl_opt: dict[str, str | int]) -> str | None:
    quote = r"('|\")"
    string_ = r"[a-zA-Z0-9]"

    # function a(le){return xx='xxx'.split('x'),
    data = re.search(rf"function\s+{string_}{{1,}}\({string_}{{2,}}\){{return\s+{string_}{{2,}}\s*=\s*{quote}(.+?){quote}\.split\({quote}(.+?){quote}\),", response.text)
    if not isinstance(data, re.Match):
        return None

    # Group 1 -> ' | "
    # Group 2 -> xxx
    # Group 3 -> ' | "
    # Group 4 -> ' | "
    # Group 5 -> x
    # Group 6 -> ' | "
    data = data.group(2).split(data.group(5))

    value_generator = iter(value for value in data if (len(value) == 65 and re.match(r"^([a-zA-Z0-9+\-$]{65})$", value)))
    secret_key = next(value_generator, None)

    if not isinstance(secret_key, str):
        return None

    return secret_key


def clean_script(script: str, challenge: str) -> str:
    match challenge:
        case "base":
            # (/\r\n/g,'\n') -> (/\\r\\n/g,'\\n')
            # replace không xử lý được cái này nên đổi sang base64
            script = script.replace(base64.b64decode(b"KC9cclxuL2csJ1xuJyk=").decode(), base64.b64decode(b"KC9cXHJcXG4vZywnXFxuJyk=").decode())
            # \' -> \\' và \" -> \\"
            script = script.replace("\\'", "\\\'").replace('\\"', '\\\\"')
    return script
