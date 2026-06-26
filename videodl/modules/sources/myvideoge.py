'''
Function:
    Implementation of MyVideoGeVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import ast
import html
import json
import urllib.parse
from typing import Any
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''MyVideoGeVideoClient'''
class MyVideoGeVideoClient(BaseVideoClient):
    source = 'MyVideoGeVideoClient'
    def __init__(self, **kwargs):
        super(MyVideoGeVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', "Accept": "*/*", "Referer": "https://www.myvideo.ge/",}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_jsarraytopython'''
    def _jsarraytopython(self, raw: str) -> Any:
        text = re.sub(r"(?s)/\*.*?\*/|//[^\n\r]*", "", raw).strip()
        text = re.sub(r"([{,]\s*)([A-Za-z_$][\w$-]*)\s*:", r'\1"\2":', text)
        text = re.sub(r",\s*([}\]])", r"\1", text)
        try: return json.loads(text)
        except Exception: pass
        py_text = re.sub(r"\btrue\b", "True", text)
        py_text = re.sub(r"\bfalse\b", "False", py_text)
        py_text = re.sub(r"\bnull\b", "None", py_text)
        try: return ast.literal_eval(py_text)
        except Exception: return None
    '''_fallbackparsesources'''
    def _fallbackparsesources(self, raw: str) -> list[dict[str, Any]]:
        sources: list[dict[str, Any]] = []
        for obj in re.findall(r"{(.*?)}", raw, flags=re.S):
            if not (m_file := re.search(r"\b(?:file|src)\s*:\s*(['\"])(.*?)\1", obj, flags=re.S)): continue
            m_label = re.search(r"\b(?:label|format_id)\s*:\s*(['\"])(.*?)\1", obj, flags=re.S)
            m_type = re.search(r"\btype\s*:\s*(['\"])(.*?)\1", obj, flags=re.S)
            sources.append({"file": m_file.group(2), "label": m_label.group(2) if m_label else None, "type": m_type.group(2) if m_type else None})
        return sources
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        html_search_regex_func = lambda pattern, webpage, default=None, flags=0: (lambda m: default if not m else next((group for group in m.groups() if group is not None), m.group(0)))(re.search(pattern, webpage, flags))
        search_meta_func = lambda webpage, name: html.unescape(str(value)).strip() if (value := html_search_regex_func((rf"<meta\b" rf"(?=[^>]*(?:property|name)\s*=\s*['\"]{re.escape(name)}['\"])" rf"(?=[^>]*content\s*=\s*['\"]([^'\"]+)['\"])" rf"[^>]*>"), webpage, flags=re.I | re.S)) else None
        clean_html_func = lambda text: None if not text else (lambda cleaned: cleaned or None)(re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", re.sub(r"(?is)<(script|style)\b.*?</\1>", "", text)))).strip())
        get_element_by_attr_func = lambda attr, value, webpage: (lambda m: m.group("content") if m else None)(re.search((r"<(?P<tag>[a-zA-Z0-9]+)\b" rf"(?=[^>]*\b{re.escape(attr)}\s*=\s*(['\"])[^'\"]*\b{re.escape(value)}\b[^'\"]*\2)" r"[^>]*>(?P<content>.*?)</(?P=tag)>"), webpage, flags=re.I | re.S))
        get_element_by_class_func = lambda class_name, webpage: get_element_by_attr_func("class", class_name, webpage)
        # try parse
        try:
            video_id = re.compile(r"https?://(?:www\.)?myvideo\.ge/v/(?P<id>[0-9]+)").match(url).group("id")
            webpage = self.get(url, timeout=20, **request_overrides).text
            video_title = (search_meta_func(webpage, "og:title") or clean_html_func(get_element_by_class_func("my_video_title", webpage)) or clean_html_func(html_search_regex_func(r"<title\b[^>]*>([^<]+)</title\b", webpage, flags=re.I | re.S)) or video_id)
            m = re.search(r"""(?s)jwplayer\s*\(\s*['"]mvplayer['"]\s*\)\s*\.\s*setup\s*\(.*?""" r"""\bsources\s*:\s*(\[.*?])\s*[,});]""", webpage)
            formats = [x for x in parsed if isinstance(x, dict)] if isinstance((parsed := self._jsarraytopython(m.group(1))), list) else self._fallbackparsesources(m.group(1))
            download_url = next((x.get("file") or x.get("src") for x in formats if x.get("file") or x.get("src")), None)
            assert download_url, f'fail to fetch download url from {url}, maybe html structure changes'
            download_url = urllib.parse.urljoin(url, str(download_url)); video_info.update(dict(raw_data=formats, download_url=download_url))
            video_title = legalizestring(video_title or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_id, cover_url=search_meta_func(webpage, "og:image")))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"myvideo.ge"}
        return BaseVideoClient.belongto(url, valid_domains)