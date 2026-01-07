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
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            if url.startswith('http://xhslink.com'): url = self.get(url, allow_redirects=True, **request_overrides).url
            vid = urlparse(url).path.strip('/').split('/')[-1]
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            raw_data = json_repair.loads(re.findall(r"window\.__INITIAL_STATE__\s*=\s*(.*?)</script></body></html>", resp.text)[0])
            video_info.update(dict(raw_data=raw_data))
            download_url = searchdictbykey(raw_data, "masterUrl")
            if not download_url: download_url = searchdictbykey(raw_data, "backupUrls")
            while isinstance(download_url, list): download_url = download_url[0]
            video_info.update(dict(download_url=download_url))
            video_title = searchdictbykey(raw_data, 'title')
            video_title = video_title[-1] if video_title else null_backup_title
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid
            ))
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.xiaohongshu.com", "xhslink.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)