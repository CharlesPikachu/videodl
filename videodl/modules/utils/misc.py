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
import time
import html
import emoji
import random
import bleach
import hashlib
import filetype
import requests
import puremagic
import mimetypes
import functools
import json_repair
import unicodedata
from pathlib import Path
from .data import VideoInfo
from datetime import datetime
from bs4 import BeautifulSoup
from contextlib import suppress
from http.cookies import SimpleCookie
from .importutils import optionalimport
from urllib.parse import urlparse, unquote
from pathvalidate import sanitize_filename
from typing import Optional, Iterable, Any, TYPE_CHECKING
curl_cffi = optionalimport('curl_cffi')
if TYPE_CHECKING: import curl_cffi as curl_cffi


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
    if isinstance(cookies, str): (c := SimpleCookie()).load(cookies); return {k: morsel.value for k, morsel in c.items()}
    raise TypeError(f'cookies type is "{type(cookies)}", expect cookies to "str" or "dict" or "None".')


'''cookies2string'''
def cookies2string(cookies: str | dict = None):
    if not cookies: cookies = ""
    if isinstance(cookies, str): return cookies
    if isinstance(cookies, dict): return (lambda c: ([c.__setitem__(k, "" if v is None else str(v)) for k, v in cookies.items()], "; ".join(m.OutputString() for m in c.values()))[1])(SimpleCookie())
    raise TypeError(f'cookies type is "{type(cookies)}", expect cookies to "str" or "dict" or "None".')


'''decodehtml'''
def decodehtml(resp: requests.Response) -> str:
    ct, content_bytes = resp.headers.get("Content-Type", ""), resp.content
    enc = m.group(1).strip('"').lower() if (m := re.search(r"charset=([^\s;]+)", ct, re.I)) else None
    if not enc:
        head = content_bytes[:8192].decode("ascii", "ignore")
        enc = m.group(1).lower() if (m := re.search(r'charset=["\']?\s*([a-zA-Z0-9_\-]+)', head, re.I)) else None
    if not enc or enc in ("iso-8859-1", "latin-1"): enc = (resp.apparent_encoding or "utf-8").lower()
    if enc in ("gbk", "gb2312"): enc = "gb18030"
    return content_bytes.decode(enc, errors="replace")


'''extracttitlefromurl'''
def extracttitlefromurl(url: str, *, timeout: float = 10.0, headers: dict = None, cookies: dict = None, request_overrides: dict = None) -> Optional[str]:
    request_overrides, headers, cookies = request_overrides or {}, headers or {}, cookies or {}
    (resp := requests.get(url, headers=headers, timeout=timeout, cookies=cookies, allow_redirects=True, **request_overrides)).raise_for_status()
    soup = BeautifulSoup(decodehtml(resp), "html.parser")
    for css, attr in [('meta[property="og:title"]', "content"), ('meta[name="twitter:title"]', "content"), ("title", None), ("h1", None)]:
        if not (el := soup.select_one(css)): continue
        t: str = (el.get(attr) if attr else el.get_text(" ", strip=True)) or ""
        t: str = html.unescape(re.sub(r"\s+", " ", t)).strip(" -|\u2013\u2014")
        if t: return t
    return None


'''legalizestring'''
def legalizestring(string: str, fit_gbk: bool = True, max_len: int = 255, fit_utf8: bool = True, replace_null_string: str = 'NULL'):
    # null string
    if not string: return replace_null_string
    # naive clean
    string = str(string).replace(r'\"', '"')
    string = re.sub(r"<\\/", "</", string)
    string = re.sub(r"\\/>", "/>", string)
    string = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), string)
    # html.unescape
    string = string if (u := html.unescape(string)) == string else (u if (v := html.unescape(u)) == u else v)
    # bleach.clean
    try: string = BeautifulSoup(string, "lxml").get_text(separator="")
    except: string = bleach.clean(string, tags=[], attributes={}, strip=True)
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
def shortenpathsinvideoinfos(video_infos: list[VideoInfo], key: str = "save_path", max_path: int = 240, keep_ext: bool = True, with_hash_suffix: bool = False):
    assert isinstance(video_infos, Iterable); used_paths = set()
    for video_info in video_infos:
        if not (raw_path := (video_info.get(key) or "").strip()) or raw_path.upper() == "NULL": continue
        src_path = Path(raw_path); output_dir = src_path.parent.resolve(); output_dir.mkdir(parents=True, exist_ok=True)
        ext, stem, digest = src_path.suffix if keep_ext else "", src_path.stem, hashlib.md5(str(src_path).encode("utf-8")).hexdigest()
        for hash_len in (6, 8, 10, 12):
            hash_suffix = f"-{digest[:hash_len]}" if with_hash_suffix else ""
            max_stem_len = max(1, max_path - (len(str(output_dir)) + 1 + len(hash_suffix) + len(ext)))
            safe_stem = (stem[:max_stem_len].rstrip(" .") or "NULL")
            out_path = str(output_dir / f"{safe_stem}{hash_suffix}{ext}")
            if out_path.lower() not in used_paths: break
        used_paths.add(out_path.lower()); video_info[key] = out_path
    return video_infos


'''resp2json'''
def resp2json(resp: requests.Response) -> dict:
    valid_resp_object = (requests.Response, curl_cffi.requests.Response) if curl_cffi else requests.Response
    if not isinstance(resp, valid_resp_object): return {}
    try: result = resp.json()
    except Exception: result = json_repair.loads(resp.text)
    return (result if result else dict())


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


'''hashablesth'''
def hashablesth(obj):
    return tuple((k, hashablesth(v)) for k, v in sorted(obj.items())) if isinstance(obj, dict) else tuple(hashablesth(x) for x in obj) if isinstance(obj, list) else tuple(sorted(hashablesth(x) for x in obj)) if isinstance(obj, set) else obj


'''dedupkeeporder'''
def dedupkeeporder(seq):
    seen, out = set(), []
    for item in seq: (seen.add(key), out.append(item)) if (key := hashablesth(item)) not in seen else None
    return out


'''searchdictbykey'''
def searchdictbykey(obj, target_key: str | list | tuple | set) -> list:
    results, target_key = [], [target_key] if isinstance(target_key, str) else target_key
    if isinstance(obj, dict):
        for k, v in obj.items(): results += ([v] if k in target_key else []) + searchdictbykey(v, target_key)
    elif isinstance(obj, list):
        for item in obj: results.extend(searchdictbykey(item, target_key))
    return dedupkeeporder(results)


'''safeextractfromdict'''
def safeextractfromdict(data, progressive_keys, default_value: Any = None):
    try: result = functools.reduce(lambda x, k: x[k], progressive_keys, data)
    except Exception: result = default_value
    return result


'''traverseobj'''
def traverseobj(obj, *paths, default: Any = None, expected_type: Any = None, get_all: bool = True):
    return next((result for path in paths if (result := traversesingle(obj, path, expected_type, get_all)) is not None), default)


'''traversesingle'''
def traversesingle(obj, path, expected_type, get_all):
    path, current, branched, MISSING = (path,) if not isinstance(path, (list, tuple)) else path, [obj], False, object()
    def safe_cast_func(func, v):
        with suppress(Exception): return func(v)
    def safe_match_func(key, a, v):
        try: return key(a, v)
        except Exception: return False
    def safe_index_func(seq, key, default=MISSING):
        try: return seq[key]
        except IndexError: return default
    for key in path:
        new_current = []
        for item in current:
            if item is None or item == {}: continue
            if key is Ellipsis: branched = True; new_current.extend(item.values() if isinstance(item, dict) else (item if isinstance(item, (list, tuple)) else ()))
            elif callable(key) and not isinstance(key, type): branched = True; new_current.extend(v for a, v in (item.items() if isinstance(item, dict) else enumerate(item) if isinstance(item, (list, tuple)) else ()) if safe_match_func(a, v))
            elif isinstance(key, str): isinstance(item, dict) and (val := item.get(key)) is not None and new_current.append(val)
            elif isinstance(key, int): (val := (safe_index_func(item, key) if isinstance(item, (list, tuple)) else item.get(key, MISSING) if isinstance(item, dict) else MISSING)) is not MISSING and (not isinstance(item, dict) or val is not None) and new_current.append(val)
        current = new_current
    if expected_type is not None:
        if isinstance(expected_type, type): current = [v for v in current if isinstance(v, expected_type)]
        elif callable(expected_type): current = [r for v in current if (r := safe_cast_func(expected_type, v)) is not None]
    if not (current := [v for v in current if v is not None and v != {}]): return None
    return (current if branched and get_all else current[0])


'''yieldtimerelatedtitle'''
def yieldtimerelatedtitle(source: str):
    dt = datetime.fromtimestamp(time.time())
    date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
    return f'{date_str} {source}-unknowtitle'


'''SpinWithBackoff'''
class SpinWithBackoff:
    def __init__(self, start_secs: int = 1, backoff_factor: float = 1.5, max_secs: int = 60):
        self.nth = 0
        self.max_secs = max_secs
        self.cur_secs = start_secs
        self.backoff_factor = backoff_factor
    '''sleep'''
    def sleep(self):
        time.sleep(self.cur_secs + random.random() * 0.5)
        self.cur_secs = min(self.cur_secs * self.backoff_factor, self.max_secs)
        self.nth += 1


'''FileTypeSniffer'''
class FileTypeSniffer():
    COMMON_MEDIA_EXTS = {
        # videos
        "3g2", "3gp", "3gp2", "3gpp", "3gpp2", "amv", "apng", "asf", "avi", "avc", "avs", "avs2", "c2", "cdxl", "cgi", "cif", "dif", "dv", "f4p", "f4v", "flv", "gif", "gifv", "mng", "vc1", "vob", "webm", "wmv",
        "h261", "h263", "h264", "h265", "h26l", "hevc", "idf", "ism", "isma", "ismv", "j2k", "m2p", "m2ts", "m2v", "mts", "ts", "m4v", "mj2", "mjpeg", "mjpg", "mk3d", "mks", "mkv", "yuv", "yuv10", "m3u", "svi", 
        "mov", "mp4", "mp4v", "mpe", "mpeg", "mpg", "mpv", "mpo", "mvi", "mxf", "nsv", "obu", "ogg", "ogm", "ogv", "psp", "qcif", "rgb", "rm", "rmvb", "roq", "rrc", "v210", 
        # audios
        "aac", "aax", "aaxc", "ac3", "adts", "aif", "aifc", "aiff", "alac", "amr", "ape", "au", "avr", "awb", "caf", "cda", "dff", "dfsf", "dsf", "dss", "dts", "dtshd", "ec3", "f32", "ofs", "opus", "paf", "stm", 
        "f64", "flac", "gsm", "hca", "htk", "iff", "ima", "ircam", "kar", "kss", "la", "l16", "m15", "m3u8", "m4a", "m4b", "m4p", "m4r", "mat4", "mat5", "med", "midi", "mid", "mlp", "tak", "at3", "aa3", "16svx", 
        "mod", "mo3", "mp1", "mp2", "mp3", "mpa", "mpc", "mp+", "mpp", "mptm", "msv", "mt2", "mtm", "mxmf", "nist", "nsf", "oga", "ogg", "okt", "oma", "ofr", "amf", "dmf", "far", "gbs", "at9", "3ga", "xm", "xi", 
        "pcm", "ptm", "pvf", "ra", "ram", "rf64", "rmi", "rmj", "rmm", "rmx", "roq", "raw", "s3m", "sap", "sds", "sd2", "sd2f", "sf", "shn", "sid", "snd", "spc", "spx", "8svx", "669", "usf", "2sf", "gsf", "qsf", 
        "tta", "thd", "ul", "ult", "umx", "voc", "vgm", "vgz", "wav", "wave", "wax", "w64", "wma", "wve", "wv", "wvx", "spu", "psf", "psf1", "psf2", "ssf", "miniusf", "gym", "hes", "it", "mdl", "mpc2k", "nsa", 
        # special
        "m4s",
    }
    PREFERRED_MIME_TO_EXT = {
        # video
        "video/mp4": "mp4", "video/quicktime": "mov", "video/x-msvideo": "avi", "video/x-ms-wmv": "wmv", "video/webm": "webm", "video/x-flv": "flv", "video/x-matroska": "mkv", "video/mp2t": "ts", "video/mpeg": "mpeg", "application/vnd.apple.mpegurl": "m3u8",
        # audio
        "audio/mpeg": "mp3", "audio/mp4": "m4a", "audio/x-m4a": "m4a", "audio/aac": "aac", "audio/flac": "flac", "audio/wav": "wav", "audio/x-wav": "wav", "audio/ogg": "ogg", "audio/opus": "opus", "audio/webm": "webm", "audio/x-ms-wma": "wma", "audio/aiff": "aiff", "audio/x-aiff": "aiff",
    }
    '''pickextfrommime'''
    @classmethod
    def pickextfrommime(cls, content_type: str):
        if not content_type: return None
        mime = content_type.split(";", 1)[0].strip().lower()
        if (ext := cls.PREFERRED_MIME_TO_EXT.get(mime)) in cls.COMMON_MEDIA_EXTS: return ext
        for ext in (mimetypes.guess_all_extensions(mime, strict=False) or []):
            if (ext := ext.lstrip(".").lower()) in cls.COMMON_MEDIA_EXTS: return ext
        return None
    '''pickextfromurl'''
    @classmethod
    def pickextfromurl(cls, url: str):
        ext = os.path.splitext(unquote(urlparse(url).path))[-1].lstrip(".").lower()
        return ext if ext in cls.COMMON_MEDIA_EXTS else None
    '''pickextfrombytes'''
    @classmethod
    def pickextfrombytes(cls, chunk: bytes):
        # no chunk data
        if not chunk: return None, None
        # filetype
        try:
            if (kind := filetype.guess(chunk)) and kind.extension:
                if (ext := str(kind.extension).lower()) in cls.COMMON_MEDIA_EXTS: return ext, "filetype"
        except Exception:
            pass
        # puremagic
        try:
            if (ext := puremagic.from_string(chunk)):
                if (ext := str(ext).lower().lstrip(".")) in cls.COMMON_MEDIA_EXTS: return ext, "puremagic"
        except Exception:
            pass
        # all fails
        return None, None
    '''getfileextensionfromurl'''
    @staticmethod
    def getfileextensionfromurl(url: str, headers: dict = None, cookies: dict = None, request_overrides: dict = None, skip_urllib_parse: bool = False):
        # prepare
        outputs = {"ext": "NULL", "sniffer": "NULL", "ok": False}
        headers, cookies, request_overrides = dict(headers or {}), dict(cookies or {}), dict(request_overrides or {})
        request_overrides.setdefault("headers", headers); request_overrides.setdefault("cookies", cookies)
        # 1) URL path
        if not skip_urllib_parse:
            if (ext := FileTypeSniffer.pickextfromurl(url)): outputs.update({"ext": ext, "sniffer": "urllib.parse", "ok": True}); return outputs
        # 2) Requests.HEAD
        try:
            with requests.head(url, allow_redirects=True, **request_overrides) as resp:
                if (ext := FileTypeSniffer.pickextfrommime(resp.headers.get("Content-Type", ""))): outputs.update({"ext": ext, "sniffer": "requests.head", "ok": True}); return outputs
        except Exception:
            pass
        # 3) Requests.GET + Range
        try:
            (range_headers := dict(request_overrides.get("headers") or {})).setdefault("Range", "bytes=0-8191")
            (range_overrides := dict(request_overrides))["headers"] = range_headers
            with requests.get(url, allow_redirects=True, stream=True, **range_overrides) as resp:
                # 3.1 look headers
                if (ext := FileTypeSniffer.pickextfrommime(resp.headers.get("Content-Type", ""))): outputs.update({"ext": ext, "sniffer": "requests.get.stream.headers", "ok": True}); return outputs
                # 3.2 look first few kbs
                if (ext, sniffer := FileTypeSniffer.pickextfrombytes(resp.raw.read(8192, decode_content=True) or b""))[0]: outputs.update({"ext": ext, "sniffer": sniffer, "ok": True}); return outputs
        except Exception:
            pass
        # all fails
        return outputs