'''
Function:
    Implementation of XinhuaNetVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''XinhuaNetVideoClient'''
class XinhuaNetVideoClient(BaseVideoClient):
    source = 'XinhuaNetVideoClient'
    def __init__(self, **kwargs):
        super(XinhuaNetVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractmedia'''
    def _extractmedia(self, base_url: str, html_text: str) -> dict:
        soup = BeautifulSoup(html_text, "lxml")
        first_text_func = lambda selectors: next((text for sel in selectors if (tag := soup.select_one(sel)) and (text := (tag.get("content") or tag.get_text(" ", strip=True)))), None)
        first_attr_func = lambda selectors, attr: next((urljoin(base_url, val) for sel in selectors if (tag := soup.select_one(sel)) and (val := tag.get(attr))), None)
        title = first_text_func(["meta[property='og:title']", "meta[name='title']", "h1", ".title", "title"])
        if title and soup.select_one("title") and title == soup.select_one("title").get_text(strip=True): title = re.sub(r"[-_｜|].*$", "", title).strip()
        if not title: title = tag.get_text(" ", strip=True) if (tag := soup.select_one("h1 .title, .mheader .title, #wxtitle")) else None
        video_url = first_attr_func(["video source", "video", "source", ".pageVideo", "[video_src]", "meta[property='og:video']", "meta[property='og:video:url']"], "src")
        if not video_url: video_url = first_attr_func([".pageVideo", "[video_src]"], "video_src")
        if not video_url: video_url = urljoin(base_url, tag.get("video_src")) if (tag := soup.select_one(".pageVideo[video_src]")) else None
        if not video_url: video_url = urljoin(base_url, txt) if (tag := soup.select_one("#fontsize")) and (txt := tag.get_text(strip=True)).startswith(("http://", "https://")) else None
        cover = first_attr_func(["meta[property='og:image']", "meta[name='twitter:image']", ".pageVideo", "[poster]", "video", "img"], "content")
        if not cover: cover = first_attr_func([".pageVideo", "[poster]", "video"], "poster")
        if not cover: cover = first_attr_func(["article img", "#detail img", ".content img", "img"], "src")
        if not cover: cover = urljoin(base_url, tag.get("poster")) if (tag := soup.select_one(".pageVideo[poster]")) else cover
        video_id = meta_id["content"] if (meta_id := soup.select_one("meta[name='contentid']")) and meta_id.get("content") else None
        if not video_id: video_id = next((tag.get(k) for sel in [".pageVideo", "video", "[data-video-id]", "[data-id]"] if (tag := soup.select_one(sel)) for k in ["data-video-id", "data-id", "id", "vid"] if tag.get(k)), None)
        if not video_id and video_url: video_id = m.group(1) if (m := re.search(r"/([A-Za-z0-9_-]{10,})\.(mp4|m3u8)", video_url)) else None
        return {"title": title, "video_url": video_url, "cover_url": cover, "video_id": video_id}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := self._extractmedia(urljoin(url, "/"), resp.text)))); video_info.update(dict(download_url=raw_data['video_url']))
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=raw_data['video_id'], cover_url=raw_data.get('cover_url')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"news.cn", "xinhuanet.com"}
        return BaseVideoClient.belongto(url, valid_domains)