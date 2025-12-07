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
import html
import emoji
import bleach
import requests
import mimetypes
import functools
import json_repair
import unicodedata
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathvalidate import sanitize_filename


'''legalizestring'''
def legalizestring(string: str, fit_gbk: bool = True, max_len: int = 255, fit_utf8: bool = True, replace_null_string: str = 'NULL'):
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
    return string


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