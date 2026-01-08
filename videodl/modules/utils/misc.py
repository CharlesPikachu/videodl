'''
Function:
    Implementation of common utils
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
import requests
import mimetypes
import functools
import json_repair
import unicodedata
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathvalidate import sanitize_filename


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
def shortenpathsinvideoinfos(video_infos: list[dict], key: str = "file_path", max_path: int = 240, keep_ext: bool = True):
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
            hash_suffix = f"_{digest[:hash_len]}"
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
    if not isinstance(resp, requests.Response): return {}
    try:
        result = resp.json()
    except:
        result = json_repair.loads(resp.text)
    if not result: result = dict()
    return result


'''usedownloadheaderscookies'''
def usedownloadheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.default_headers = self.default_download_headers
        if hasattr(self, 'default_download_cookies'):
            self.default_cookies = self.default_download_cookies
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''useparseheaderscookies'''
def useparseheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.default_headers = self.default_parse_headers
        if hasattr(self, 'default_parse_cookies'):
            self.default_cookies = self.default_parse_cookies
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''usesearchheaderscookies'''
def usesearchheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.default_headers = self.default_search_headers
        if hasattr(self, 'default_search_cookies'):
            self.default_cookies = self.default_search_cookies
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
def safeextractfromdict(data, progressive_keys, default_value):
    try:
        result = data
        for key in progressive_keys: result = result[key]
    except:
        result = default_value
    return result


'''yieldtimerelatedtitle'''
def yieldtimerelatedtitle(source: str):
    dt = datetime.fromtimestamp(time.time())
    date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
    return f'{source}_null_{date_str}'


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
    '''getfileextensionfromurl'''
    @staticmethod
    def getfileextensionfromurl(url: str, headers: dict = None, cookies: dict = None, request_overrides: dict = None, skip_urllib_parse: bool = False):
        # prepare
        headers, cookies, request_overrides = headers or {}, cookies or {}, request_overrides or {}
        if 'cookies' not in request_overrides: request_overrides['cookies'] = cookies
        if 'headers' not in request_overrides: request_overrides['headers'] = headers
        outputs = {'ext': 'NULL', 'sniffer': 'NULL', 'ok': False}
        # urllib.parse
        if not skip_urllib_parse:
            ext = os.path.splitext(urlparse(url).path)[1].removeprefix('.')
            if ext:
                outputs.update(dict(ext=ext, sniffer='urllib.parse', ok=True))
                return outputs
        # requests.head
        resp = requests.head(url, allow_redirects=True, **request_overrides)
        content_type = resp.headers.get('Content-Type', '').split(';')[0]
        if content_type:
            ext = mimetypes.guess_extension(content_type).removeprefix('.')
            if ext:
                outputs.update(dict(ext=ext, sniffer='requests.head', ok=True))
                return outputs
        # requests.get.stream
        resp = requests.get(url, allow_redirects=True, stream=True, **request_overrides)
        content_type = resp.headers.get('Content-Type', '').split(';')[0]
        if content_type:
            ext = mimetypes.guess_extension(content_type).removeprefix('.')
            if ext:
                outputs.update(dict(ext=ext, sniffer='requests.get.stream', ok=True))
                return outputs
        # return
        return outputs