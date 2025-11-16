'''
Function:
    酷6视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from .base import Base
from ..utils import filterBadCharacter


'''酷6视频下载器类'''
class Ku6(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Ku6, self).__init__(config, logger_handle, **kwargs)
        self.source = 'ku6'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url, headers=self.headers)
        download_url = re.findall(r'src: "(https://.*?)"', response.text)
        if not download_url: return []
        title = re.findall(r'document.title = "(.*?)";', response.text)
        videoinfo = {
            'source': self.source,
            'download_url': download_url[0],
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(title[0] if title else f'视频走丢啦_{time.time()}'),
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
        valid_hosts = ['ku6.com']
        for host in valid_hosts:
            if host in url: return True
        return False