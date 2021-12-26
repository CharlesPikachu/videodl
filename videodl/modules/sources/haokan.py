'''
Function:
    好看视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import json
import time
from .base import Base
from ..utils.misc import *


'''好看视频下载器类'''
class Haokan(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Haokan, self).__init__(config, logger_handle, **kwargs)
        self.source = 'haokan'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url, headers=self.headers)
        response_json = json.loads(re.findall(r'PRELOADED_STATE__\s=\s(.*?);', response.text)[0])
        download_url = response_json['curVideoMeta']['playurl']
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': '_'.join([self.source, filterBadCharacter(response_json.get('curVideoMeta', {}).get('title', f'视频走丢啦_{time.time()}'))]),
            'ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['haokan.baidu.com']
        for host in valid_hosts:
            if host in url: return True
        return False