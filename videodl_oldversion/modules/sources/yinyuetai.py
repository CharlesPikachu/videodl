'''
Function:
    音悦台视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from .base import Base
from ..utils import filterBadCharacter


'''音悦台视频下载器类'''
class Yinyuetai(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Yinyuetai, self).__init__(config, logger_handle, **kwargs)
        self.source = 'yinyuetai'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        vid = re.findall(r'id=(\d+)', url)[0]
        response = self.session.get(self.videoinfo_url.format(vid), headers=self.headers)
        response_json = response.json()
        videoinfo = {
            'source': self.source,
            'download_url': response_json['videoUrl'],
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(response_json.get('videoName', f'视频走丢啦_{time.time()}')),
            'ext': 'mp4',
        }
        response = self.session.get(self.favicon_url, headers=self.headers)
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        self.videoinfo_url = 'https://data.yinyuetai.com/video/getVideoInfo?id={}'
        self.favicon_url = 'https://www.yinyuetai.com/favicon.ico'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['yinyuetai.com']
        for host in valid_hosts:
            if host in url: return True
        return False