'''
Function:
    Ted视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
from .base import Base
from ..utils import filterBadCharacter


'''Ted视频下载器类'''
class Ted(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Ted, self).__init__(config, logger_handle, **kwargs)
        self.source = 'ted'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url)
        title = re.findall(r'<meta name="title" content="(.*?)"/>', response.text)[0]
        download_url = re.findall(r'"(https://py\.tedcdn\.com/.*?).mp4', response.text)
        if not download_url:
            download_url = re.findall(r'"(https://download\.ted\.com/.*?).mp4', response.text)
        download_url = download_url[-1]
        videoinfo = {
            'source': self.source,
            'download_url': download_url + '.mp4',
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(title),
            'ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        self.session.headers.update(self.headers)
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['ted.com']
        for host in valid_hosts:
            if host in url: return True
        return False