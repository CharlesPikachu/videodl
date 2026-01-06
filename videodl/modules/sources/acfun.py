'''
Function:
    Implementation of AcFunVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import json_repair
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo


'''AcFunVideoClient'''
class AcFunVideoClient(BaseVideoClient):
    source = 'AcFunVideoClient'
    def __init__(self, **kwargs):
        super(AcFunVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
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
        video_info = VideoInfo(download_with_ffmpeg=True, source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            raw_data = json_repair.loads(re.findall('window.pageInfo =(.*?);', resp.text)[0].split('=', 1)[-1].strip())
            video_info.update(dict(raw_data=raw_data))
            try:
                download_url = json_repair.loads(raw_data['currentVideoInfo']['ksPlayJsonHevc'])['adaptationSet'][0]['representation'][0]['url']
            except:
                download_url = json_repair.loads(raw_data['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['url']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data.get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info["ext"]}'), identifier=vid))
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
            valid_domains = ["www.acfun.cn"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)