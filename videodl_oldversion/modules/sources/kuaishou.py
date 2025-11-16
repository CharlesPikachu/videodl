'''
Function:
    快手视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from .base import Base
from ..utils import filterBadCharacter


'''快手视频下载器类'''
class Kuaishou(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Kuaishou, self).__init__(config, logger_handle, **kwargs)
        self.source = 'kuaishou'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url, headers=self.headers)
        title = re.findall(r'"caption":"(.*?)"', response.text)
        download_url = re.findall(r'"url":"(.*?)"', response.text)
        if not download_url: return []
        download_url = download_url[0].encode('utf-8').decode('unicode_escape')
        if 'mp4' in download_url: ext = 'mp4'
        else: ext = 'm3u8'
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(title[0] if title else f'视频走丢啦_{time.time()}'),
            'ext': ext,
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'Cookie': 'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_b70de6065feca15ca705414b711516d2; didv=1648100245000',
            'Host': 'www.kuaishou.com',
            'Referer': 'https://www.kuaishou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['kuaishou.com']
        for host in valid_hosts:
            if host in url: return True
        return False