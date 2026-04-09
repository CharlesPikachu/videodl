'''
Function:
    Implementation of WWW163VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''WWW163VideoClient'''
class WWW163VideoClient(BaseVideoClient):
    source = 'WWW163VideoClient'
    def __init__(self, **kwargs):
        super(WWW163VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, html_text: str):
        player = (soup := BeautifulSoup(html_text, "lxml")).select_one("#dplayer")
        title = ((soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else None) or (soup.select_one('meta[property="og:title"]') or {}).get("content"))
        return {"title": title, "video_url": player.get("data-url") if player else None, "cover_url": player.get("data-poster") if player else None}
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
        valid_domains = set(valid_domains or []) | {"www.163.com"}
        return BaseVideoClient.belongto(url, valid_domains)