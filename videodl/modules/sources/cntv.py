'''
Function:
    央视网视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from .base import Base
from ..utils.misc import *


'''央视网视频下载器类'''
class CNTV(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(CNTV, self).__init__(config, logger_handle, **kwargs)
        self.source = 'cntv'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url)
        pid = re.findall(r'var guid = "(\w+)"', response.text)[0]
        params = {
            'pid': pid,
            'client': 'flash',
            'im': '0',
            'tsp': str(int(time.time())),
            'vn': '2049',
            'vc': '9BFAED20B5E91364B9B1E5A777565554',
            'uid': 'A15780E361D8094E78EAE9AB2BD31534',
            'wlan': '',
        }
        response = self.session.get(self.getHttpVideoInfo_url, params=params)
        response_json = response.json()
        download_url, flag = [], False
        for video_type in response_json['video']:
            for support_type in ['chapters4', 'chapters3', 'chapters2', 'chapters', 'lowChapters']:
                if support_type == video_type:
                    for item in response_json['video'][video_type]:
                        download_url.append(item['url'])
                    flag = True
                    break
            if flag: break
        if len(download_url) == 1: download_url = download_url[0]
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': '_'.join([self.source, filterBadCharacter(response_json.get('title', f'视频走丢啦_{time.time()}'))]),
            'ext': 'mp4',
            'split_ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        self.getHttpVideoInfo_url = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['v.cctv.com']
        for host in valid_hosts:
            if host in url: return True
        return False