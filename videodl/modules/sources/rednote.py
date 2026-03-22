'''
Function:
    Implementation of RednoteVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from urllib.parse import urlparse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, searchdictbykey, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''RednoteVideoClient'''
class RednoteVideoClient(BaseVideoClient):
    source = 'RednoteVideoClient'
    def __init__(self, **kwargs):
        super(RednoteVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            if url.startswith('http://xhslink.com'): url = self.get(url, allow_redirects=True, **request_overrides).url
            vid = urlparse(url).path.strip('/').split('/')[-1]; (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(re.findall(r"window\.__INITIAL_STATE__\s*=\s*(.*?)</script></body></html>", resp.text)[0]))))
            if not (download_url := searchdictbykey(raw_data, "masterUrl")): download_url = searchdictbykey(raw_data, "backupUrls")
            while isinstance(download_url, list): download_url = download_url[0]
            video_info.update(dict(download_url=download_url)); video_title = searchdictbykey(raw_data, 'title')
            if not video_title[-1]: video_title = searchdictbykey(raw_data, 'desc')
            video_title = video_title[-1] if video_title else null_backup_title
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            try: cover_url = searchdictbykey(raw_data, 'imageList')[0][0]['urlDefault']
            except Exception: cover_url = None
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"xiaohongshu.com", "xhslink.com"}
        return BaseVideoClient.belongto(url, valid_domains)