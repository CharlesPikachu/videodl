'''
Function:
    Implementation of Common Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import time
import html
import emoji
import random
import bleach
import hashlib
import requests
import mimetypes
import functools
import json_repair
import unicodedata
from pathlib import Path
from typing import Optional
from datetime import datetime
from bs4 import BeautifulSoup
from contextlib import suppress
from .importutils import optionalimport
from pathvalidate import sanitize_filename
from urllib.parse import urlparse, urlsplit


'''naivedetermineext'''
def naivedetermineext(url: str, default_ext='unknown_video'):
    if url is None or '.' not in url: return default_ext
    guess = url.partition('?')[0].rpartition('.')[2]
    if re.match(r'^[A-Za-z0-9]+$', guess): return guess
    return default_ext


'''floatornone'''
def floatornone(v, scale=1):
    if v is None: return None
    try: return float(v) / scale
    except (ValueError, TypeError): return None


'''intornone'''
def intornone(v):
    if v is None: return None
    try: return int(v)
    except (ValueError, TypeError): return None


'''naivejstojson'''
def naivejstojson(code):
    COMMENT_RE = r'/\*(?:(?!\*/).)*?\*/|//[^\n]*\n'
    code = re.sub(COMMENT_RE, '', code)
    code = re.sub(r"'([^']*)'", r'"\1"', code)
    code = re.sub(r'(?<=[{,])\s*([a-zA-Z_$][\w$]*)\s*:', r'"\1":', code)
    code = re.sub(r',\s*([}\]])', r'\1', code)
    code = re.sub(r'\bundefined\b', 'null', code)
    code = re.sub(r'\bvoid\s+0\b', 'null', code)
    return code


'''naivecleanhtml'''
def naivecleanhtml(text):
    if text is None: return None
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text.strip()


'''cookies2dict'''
def cookies2dict(cookies: str | dict = None):
    if not cookies: cookies = {}
    if isinstance(cookies, dict): return cookies
    if isinstance(cookies, str): return dict(item.split("=", 1) for item in cookies.split("; "))
    raise TypeError(f'cookies type is "{type(cookies)}", expect cookies to "str" or "dict" or "None".')


'''cookies2string'''
def cookies2string(cookies: str | dict = None):
    if not cookies: cookies = ""
    if isinstance(cookies, str): return cookies
    if isinstance(cookies, dict): return "; ".join(f"{k}={v}" for k, v in cookies.items())
    raise TypeError(f'cookies type is "{type(cookies)}", expect cookies to "str" or "dict" or "None".')


'''decodehtml'''
def decodehtml(resp: requests.Response) -> str:
    b = resp.content
    ct = resp.headers.get("Content-Type", "")
    m = re.search(r"charset=([^\s;]+)", ct, re.I)
    enc = m.group(1).strip('"').lower() if m else None
    if not enc:
        head = b[:8192].decode("ascii", "ignore")
        m = re.search(r'charset=["\']?\s*([a-zA-Z0-9_\-]+)', head, re.I)
        enc = m.group(1).lower() if m else None
    if not enc or enc in ("iso-8859-1", "latin-1"): enc = (resp.apparent_encoding or "utf-8").lower()
    if enc in ("gbk", "gb2312"): enc = "gb18030"
    return b.decode(enc, errors="replace")


'''extracttitlefromurl'''
def extracttitlefromurl(url: str, *, timeout: float = 10.0, headers: dict = None, cookies: dict = None, request_overrides: dict = None) -> Optional[str]:
    request_overrides, headers, cookies = request_overrides or {}, headers or {}, cookies or {}
    resp = requests.get(url, headers=headers, timeout=timeout, cookies=cookies, allow_redirects=True, **request_overrides)
    resp.raise_for_status()
    text = decodehtml(resp)
    soup = BeautifulSoup(text, "html.parser")
    for css, attr in [('meta[property="og:title"]', "content"), ('meta[name="twitter:title"]', "content"), ("title", None), ("h1", None)]:
        el = soup.select_one(css)
        if not el: continue
        t: str = (el.get(attr) if attr else el.get_text(" ", strip=True)) or ""
        t: str = html.unescape(re.sub(r"\s+", " ", t)).strip(" -|\u2013\u2014")
        if t: return t
    return None


'''legalizestring'''
def legalizestring(string: str, fit_gbk: bool = True, max_len: int = 255, fit_utf8: bool = True, replace_null_string: str = 'NULL'):
    if not string: return replace_null_string
    string = str(string)
    string = string.replace(r'\"', '"')
    string = re.sub(r"<\\/", "</", string)
    string = re.sub(r"\\/>", "/>", string)
    string = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), string)
    # html.unescape
    for _ in range(2):
        new_string = html.unescape(string)
        if new_string == string: break
        string = new_string
    # bleach.clean
    try:
        string = BeautifulSoup(string, "lxml").get_text(separator="")
    except:
        string = bleach.clean(string, tags=[], attributes={}, strip=True)
    # unicodedata.normalize
    string = unicodedata.normalize("NFC", string)
    # emoji.replace_emoji
    string = emoji.replace_emoji(string, replace="")
    # isprintable
    string = "".join([ch for ch in string if ch.isprintable() and not unicodedata.category(ch).startswith("C")])
    # sanitize_filename
    string = sanitize_filename(string, max_len=max_len)
    # fix encoding
    if fit_gbk: string = string.encode("gbk", errors="ignore").decode("gbk", errors="ignore")
    if fit_utf8: string = string.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    # return
    string = re.sub(r"\s+", " ", string).strip()
    if not string: string = replace_null_string
    return string.rstrip(" .")


'''shortenpathsinvideoinfos'''
def shortenpathsinvideoinfos(video_infos: list[dict], key: str = "file_path", max_path: int = 240, keep_ext: bool = True, with_hash_suffix: bool = False):
    used_paths = set()
    for info in video_infos:
        raw_path = (info.get(key) or "").strip()
        if not raw_path or raw_path.upper() == "NULL": continue
        src_path = Path(raw_path)
        output_dir = src_path.parent.resolve(); output_dir.mkdir(parents=True, exist_ok=True)
        ext = src_path.suffix if keep_ext else ""
        stem = src_path.stem
        digest = hashlib.md5(str(src_path).encode("utf-8")).hexdigest()
        for hash_len in (8, 10):
            hash_suffix = f"-{digest[:hash_len]}" if with_hash_suffix else ""
            max_stem_len = max(1, max_path - (len(str(output_dir)) + 1 + len(hash_suffix) + len(ext)))
            safe_stem = (stem[:max_stem_len].rstrip(" .") or "NULL")
            out_path = str(output_dir / f"{safe_stem}{hash_suffix}{ext}")
            if out_path.lower() not in used_paths: break
        used_paths.add(out_path.lower()); info[key] = out_path
    return video_infos


'''byte2mb'''
def byte2mb(size: int):
    try:
        size = int(float(size))
        if size == 0: return 'NULL'
        size = f'{round(size / 1024 / 1024, 2)} MB'
    except:
        size = 'NULL'
    return size


'''resp2json'''
def resp2json(resp: requests.Response):
    curl_cffi = optionalimport('curl_cffi')
    valid_resp_object = (requests.Response, curl_cffi.requests.Response) if curl_cffi else requests.Response
    if not isinstance(resp, valid_resp_object): return {}
    try: result = resp.json()
    except: result = json_repair.loads(resp.text)
    if not result: result = dict()
    return result


'''usedownloadheaderscookies'''
def usedownloadheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.default_headers = self.default_download_headers
        if hasattr(self, 'default_download_cookies'): self.default_cookies = self.default_download_cookies
        if hasattr(self, 'enable_download_curl_cffi'): self.enable_curl_cffi = self.enable_download_curl_cffi
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''useparseheaderscookies'''
def useparseheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.default_headers = self.default_parse_headers
        if hasattr(self, 'default_parse_cookies'): self.default_cookies = self.default_parse_cookies
        if hasattr(self, 'enable_parse_curl_cffi'): self.enable_curl_cffi = self.enable_parse_curl_cffi
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''usesearchheaderscookies'''
def usesearchheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.default_headers = self.default_search_headers
        if hasattr(self, 'default_search_cookies'): self.default_cookies = self.default_search_cookies
        if hasattr(self, 'enable_search_curl_cffi'): self.enable_curl_cffi = self.enable_search_curl_cffi
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''searchdictbykey'''
def searchdictbykey(obj, target_key: str):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == target_key: results.append(v)
            results.extend(searchdictbykey(v, target_key))
    elif isinstance(obj, list):
        for item in obj: results.extend(searchdictbykey(item, target_key))
    return results


'''safeextractfromdict'''
def safeextractfromdict(data, progressive_keys, default_value=None):
    try:
        result = data
        for key in progressive_keys: result = result[key]
    except:
        result = default_value
    return result


'''traverseobj'''
def traverseobj(obj, *paths, default=None, expected_type=None, get_all=True):
    for path in paths:
        result = traversesingle(obj, path, expected_type, get_all)
        if result is not None: return result
    return default


'''traversesingle'''
def traversesingle(obj, path, expected_type, get_all):
    if not isinstance(path, (list, tuple)): path = (path,)
    current, branched = [obj], False
    for key in path:
        new_current = []
        for item in current:
            if item is None or item == {}: continue
            if key is Ellipsis: branched = True; new_current.extend(item.values() if isinstance(item, dict) else (item if isinstance(item, (list, tuple)) else ()))
            elif callable(key) and not isinstance(key, type):
                branched = True
                it = item.items() if isinstance(item, dict) else (enumerate(item) if isinstance(item, (list, tuple)) else ())
                for a, v in it:
                    try: key(a, v) and new_current.append(v)
                    except Exception: pass
            elif isinstance(key, str): isinstance(item, dict) and (val := item.get(key)) is not None and new_current.append(val)
            elif isinstance(key, int):
                if isinstance(item, (list, tuple)):
                    try: new_current.append(item[key])
                    except IndexError: pass
                elif isinstance(item, dict) and (val := item.get(key)) is not None: new_current.append(val)
        current = new_current
    if expected_type is not None:
        if isinstance(expected_type, type): current = [v for v in current if isinstance(v, expected_type)]
        elif callable(expected_type):
            filtered = []
            for v in current:
                with suppress(Exception): r = expected_type(v); r is not None and filtered.append(r)
            current = filtered
    current = [v for v in current if v is not None and v != {}]
    if not current: return None
    if branched and get_all: return current
    return current[0]


'''yieldtimerelatedtitle'''
def yieldtimerelatedtitle(source: str):
    dt = datetime.fromtimestamp(time.time())
    date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
    return f'{source}_null_{date_str}'


'''requestsproxytoplaywright'''
def requestsproxytoplaywright(proxy: dict | str, *, prefer: tuple = ("https", "http", "all"), bypass: str = None):
    if not proxy: return None
    s = (proxy if isinstance(proxy, str) else next((proxy.get(k) for k in prefer if proxy.get(k)), None) or next(iter(proxy.values()), None))
    if not s or not isinstance(s, str): return None
    s = s.strip()
    if "://" not in s: s = "http://" + s
    u = urlsplit(s)
    scheme = ("socks5" if u.scheme == "socks5h" else u.scheme)
    host, port = u.hostname, u.port
    if not host or port is None: raise ValueError(f"Invalid proxy (need host:port): {s!r}")
    host = f"[{host}]" if ":" in host else host
    out = {"server": f"{scheme}://{host}:{port}"}
    if u.username: out["username"] = u.username
    if u.password: out["password"] = u.password
    if bypass: out["bypass"] = bypass
    return out


'''SpinWithBackoff'''
class SpinWithBackoff:
    def __init__(self, start_secs=1, backoff_factor=1.5, max_secs=60):
        self.cur_secs = start_secs
        self.backoff_factor = backoff_factor
        self.max_secs = max_secs
        self.nth = 0
    '''sleep'''
    def sleep(self):
        secs = self.cur_secs + random.random() * 0.5
        time.sleep(secs)
        self.cur_secs = min(self.cur_secs * self.backoff_factor, self.max_secs)
        self.nth += 1


'''FileTypeSniffer'''
class FileTypeSniffer:
    COMMON_MIDEA_EXTS = (
        # videos
        "3g2", "3gp", "3gp2", "3gpp", "3gpp2", "amv", "apng", "asf", "avi", "avc", "avs", "avs2", "c2", "cdxl", "cgi", "cif", "dif", "dv", "f4p", "f4v", "flv", "gif", "gifv", "mng",
        "h261", "h263", "h264", "h265", "h26l", "hevc", "idf", "ism", "isma", "ismv", "j2k", "m2p", "m2ts", "m2v", "mts", "ts", "m4v", "mj2", "mjpeg", "mjpg", "mk3d", "mks", "mkv", 
        "mov", "mp4", "mp4v", "mpe", "mpeg", "mpg", "mpv", "mpo", "mvi", "mxf", "nsv", "obu", "ogg", "ogm", "ogv", "psp", "qcif", "rgb", "rm", "rmvb", "roq", "rrc", "svi", "v210", 
        "vc1", "vob", "webm", "wmv", "yuv", "yuv10",
        # audios
        "aac", "aax", "aaxc", "ac3", "adts", "aif", "aifc", "aiff", "alac", "amr", "ape", "au", "avr", "awb", "caf", "cda", "dff", "dfsf", "dsf", "dss", "dts", "dtshd", "ec3", "f32", 
        "f64", "flac", "gsm", "hca", "htk", "iff", "ima", "ircam", "kar", "kss", "la", "l16", "m15", "m3u8", "m4a", "m4b", "m4p", "m4r", "mat4", "mat5", "med", "midi", "mid", "mlp", 
        "mod", "mo3", "mp1", "mp2", "mp3", "mpa", "mpc", "mp+", "mpp", "mptm", "msv", "mt2", "mtm", "mxmf", "nist", "nsf", "oga", "ogg", "okt", "oma", "ofr", "ofs", "opus", "paf", 
        "pcm", "ptm", "pvf", "ra", "ram", "rf64", "rmi", "rmj", "rmm", "rmx", "roq", "raw", "s3m", "sap", "sds", "sd2", "sd2f", "sf", "shn", "sid", "snd", "spc", "spx", "stm", "tak", 
        "tta", "thd", "ul", "ult", "umx", "voc", "vgm", "vgz", "wav", "wave", "wax", "w64", "wma", "wve", "wv", "wvx", "xi", "xm", "8svx", "16svx", "669", "amf", "dmf", "far", "gbs", 
        "gym", "hes", "it", "mdl", "mpc2k", "nsa", "psf", "psf1", "psf2", "ssf", "miniusf", "usf", "2sf", "gsf", "qsf", "spu", "at3", "aa3", "at9", "3ga",
        # special
        "m4s",
    )
    '''getfileextensionfromurl'''
    @staticmethod
    def getfileextensionfromurl(url: str, headers: dict = None, cookies: dict = None, request_overrides: dict = None, skip_urllib_parse: bool = False):
        # prepare
        headers, cookies, request_overrides = headers or {}, cookies or {}, copy.deepcopy(request_overrides or {})
        if 'cookies' not in request_overrides: request_overrides['cookies'] = cookies
        if 'headers' not in request_overrides: request_overrides['headers'] = headers
        outputs = {'ext': 'NULL', 'sniffer': 'NULL', 'ok': False}
        # urllib.parse
        if not skip_urllib_parse:
            ext = os.path.splitext(urlparse(url).path)[-1]
            if ext and (ext.strip('. ') in FileTypeSniffer.COMMON_MIDEA_EXTS):
                outputs.update(dict(ext=ext.strip('. '), sniffer='urllib.parse', ok=True))
                return outputs
        # requests.head
        resp = requests.head(url, allow_redirects=True, **request_overrides)
        content_type = resp.headers.get('Content-Type', '').split(';')[0]
        if content_type:
            ext = mimetypes.guess_extension(content_type)
            if ext and (ext.strip('. ') in FileTypeSniffer.COMMON_MIDEA_EXTS):
                outputs.update(dict(ext=ext.strip('. '), sniffer='requests.head', ok=True))
                return outputs
        # requests.get.stream
        resp = requests.get(url, allow_redirects=True, stream=True, **request_overrides)
        content_type = resp.headers.get('Content-Type', '').split(';')[0]
        if content_type:
            ext = mimetypes.guess_extension(content_type)
            if ext and (ext.strip('. ') in FileTypeSniffer.COMMON_MIDEA_EXTS):
                outputs.update(dict(ext=ext.strip('. '), sniffer='requests.get.stream', ok=True))
                return outputs
        # return
        return outputs