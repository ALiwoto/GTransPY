from GTransPY.types import Lang
import httpx
import re
import ujson as json



def DetectLanguage(text: str) -> Lang:
    url = "\u0068\u0074\u0074ps://de\u0074ec\u0074language\u002e" +\
        "\u0063o\u006d/\u0064emo"
    my_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://detectlanguage.com/',
            'Content-Type': 'application/json',
            'Origin': 'https://detectlanguage.com',
            'Alt-Used': 'htmlcsstoimage.com',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
            'q': text,
        }

    try:
        resp = httpx.post(url, json=my_headers)
        if resp.status_code != 200:
            raise Exception(f"Got status code of {resp.status_code} from API")
        if resp.content:
            strs = re.split('<pre>|</pre>', resp.content.decode())
            #print(strs[1])
            return Lang.from_dict(dict(json.decode(strs[1])))
        else:
            raise Exception("unexpected response from API server")

    except httpx.NetworkError:
        return None


