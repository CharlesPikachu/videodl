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
import time
import json_repair
from .base import BaseVideoClient
from ..utils import legalizestring


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
    def parsefromurl(self, url: str, request_overrides: dict = {}):
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            result = json_repair.loads(re.findall('window.pageInfo =(.*?);', resp.text)[0].split('=', 1)[-1].strip())
        except:
            pass

        response_json = json.loads()
        download_url = json.loads(response_json['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['url']
        title = response_json.get('title', f'视频走丢啦_{time.time()}')
        # construct video info
        video_infos = [{
            'source': self.source, 'download_url': download_url, 'file_name': file_name, 
            'file_path': os.path.join(self.work_dir, self.source, file_name), 'ext': 'm3u8',
        }]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["acfun.cn"]
        BaseVideoClient.belongto(url=url, valid_domains=valid_domains)