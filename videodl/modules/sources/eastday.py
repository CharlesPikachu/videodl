'''
Function:
    Implementation of EastDayVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import html
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''EastDayVideoClient'''
class EastDayVideoClient(BaseVideoClient):
    source = 'EastDayVideoClient'
    def __init__(self, **kwargs):
        super(EastDayVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, html_text: str):
        first_func, soup = lambda *xs: next((str(x).strip() for x in xs if x and str(x).strip()), ""), BeautifulSoup(html_text, "lxml")
        title = first_func(soup.select_one('meta[property="og:title"]') and soup.select_one('meta[property="og:title"]').get("content"), soup.title and soup.title.get_text(), soup.select_one("h1") and soup.select_one("h1").get_text(" ", strip=True))
        cover = first_func(soup.select_one('meta[property="og:image"]') and soup.select_one('meta[property="og:image"]').get("content"), soup.select_one('meta[name="imageurl"]') and soup.select_one('meta[name="imageurl"]').get("content"), soup.select_one('meta[name="poster"]') and soup.select_one('meta[name="poster"]').get("content"), soup.select_one("video") and soup.select_one("video").get("poster"))
        video = first_func(soup.select_one('meta[name="videourl"]') and soup.select_one('meta[name="videourl"]').get("content"), soup.select_one("video") and soup.select_one("video").get("src"))
        if not video and (m := re.search(r'contentHtml\s*=\s*"(.+?)";', html_text, re.S)): inner_soup = BeautifulSoup(html.unescape(m.group(1).replace(r"\/", "/").replace(r"\"", '"')), "html.parser"); video = first_func(inner_soup.select_one("video") and inner_soup.select_one("video").get("src")); cover = cover or first_func(inner_soup.select_one("video") and inner_soup.select_one("video").get("poster"))
        return {"title": title, "cover_url": cover, "video_url": video}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url=url).path.strip('/').split('/')[-1].removesuffix('.html').removesuffix('.htm')
            (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := self._extractvideoinfo(resp.text)))); video_info.update(dict(download_url=raw_data['video_url']))
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
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
        valid_domains = set(valid_domains or []) | {"eastday.com"}
        return BaseVideoClient.belongto(url, valid_domains)