'''
Function:
    AcFun视频下载器类
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


'''AcFun视频下载器类'''
class AcFun(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(AcFun, self).__init__(config, logger_handle, **kwargs)
        self.source = 'acfun'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url, headers=self.headers)
        response_json = json.loads(re.findall('window.pageInfo =(.*?);', response.text)[0].split('=', 1)[-1].strip())
        download_url = json.loads(response_json['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['url']
        title = response_json.get('title', f'视频走丢啦_{time.time()}')
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': '_'.join([self.source, filterBadCharacter(title)]),
            'ext': 'm3u8',
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
        valid_hosts = ['acfun.cn']
        for host in valid_hosts:
            if host in url: return True
        return False