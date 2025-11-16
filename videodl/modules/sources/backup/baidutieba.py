'''
Function:
    百度贴吧视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from .base import Base
from ..utils import filterBadCharacter


'''百度贴吧视频下载器类'''
class BaiduTieba(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(BaiduTieba, self).__init__(config, logger_handle, **kwargs)
        self.source = 'baidutieba'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url, headers=self.headers)
        title = re.findall(r"'threadTitle': '(.*?)'", response.text)
        videoinfos, download_urls = [], re.findall(r'data-video="(.*?)"', response.text)
        for idx, download_url in enumerate(download_urls):
            if idx == 0: idx = ''
            videoinfo = {
                'source': self.source,
                'download_url': download_url,
                'savedir': self.config['savedir'],
                'savename': filterBadCharacter(title[0] + str(idx) if title else f'视频走丢啦{idx}_{time.time()}'),
                'ext': 'mp4',
            }
            videoinfos.append(videoinfo)
        return videoinfos
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['tieba.baidu.com']
        for host in valid_hosts:
            if host in url: return True
        return False