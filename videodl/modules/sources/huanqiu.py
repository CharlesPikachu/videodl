'''
Function:
    Implementation of HuanQiuVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import html
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse, urljoin
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''HuanQiuVideoClient'''
class HuanQiuVideoClient(BaseVideoClient):
    source = 'HuanQiuVideoClient'
    def __init__(self, **kwargs):
        super(HuanQiuVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {
            "accept": "*/*", "host": "v6.huanqiucdn.cn", "referer": "https://www.huanqiu.com/", "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "video", 
            "sec-fetch-mode": "no-cors", "sec-fetch-site": "cross-site", "sec-fetch-storage-access": "active", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, base_url: str, html_text: str) -> dict:
        soup, base_url = BeautifulSoup(html_text, "lxml"), base_url or ''
        first_func = lambda *xs: next((x.strip() for x in xs if isinstance(x, str) and x and x.strip()), "")
        text_func = lambda css: (lambda node: node.get_text(" ", strip=True) if node else "")(soup.select_one(css))
        attr_func = lambda css, name: (lambda node: node.get(name, "") if node else "")(soup.select_one(css))
        norm_func = lambda url: "" if not (url := (url or "").strip()) else ("https:" + url if url.startswith("//") else urljoin(base_url, url))
        title = first_func(text_func("textarea.article-title"), attr_func("meta[property='og:title']", "content"), text_func("title"))
        inner = BeautifulSoup(content_html, "lxml") if (content_html := html.unescape(text_func("textarea.article-content"))) else None
        video_node = next((node for root in (inner, soup) if root and (node := root.select_one("video[src], source[src]"))), None)
        poster_url = norm_func(first_func(video_node.get("poster", "") if video_node else "", text_func("textarea.article-cover"), attr_func("meta[property='og:image']", "content")))
        return {"title": title, "video_url": norm_func(video_node.get("src", "") if video_node else ""), "cover_url": poster_url}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url=url).path.strip('/').split('/')[-1].removesuffix('.html').removesuffix('.htm')
            (resp := self.get(url, **request_overrides)).raise_for_status(); resp.encoding = resp.apparent_encoding
            video_info.update(dict(raw_data=(raw_data := self._extractvideoinfo(f"{urlparse(url).scheme}://{urlparse(url).netloc}", resp.text)))); video_info.update(dict(download_url=raw_data['video_url']))
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=raw_data.get('cover_url')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"huanqiu.com"}
        return BaseVideoClient.belongto(url, valid_domains)