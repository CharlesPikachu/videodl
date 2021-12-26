'''
Function:
    芒果TV下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import time
import uuid
import base64
from .base import Base
from ..utils.misc import *


'''芒果TV下载器类'''
class MGTV(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(MGTV, self).__init__(config, logger_handle, **kwargs)
        self.source = 'mgtv'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        # 计算tk2
        tk2 = bytes(f'did={self.did}|pno={self.pno}|ver=0.3.0301|clit={int(time.time())}'.encode())
        tk2 = base64.b64encode(tk2).decode().replace('/\+/g', '_').replace('/\//g', '~').replace('/=/g', '-')
        tk2 = list(' '.join(tk2).split())
        tk2.reverse()
        tk2 = ''.join(tk2)
        # 计算pm2
        params = {
            'did': self.did,
            'suuid': uuid.uuid4(),
            'cxid': '',
            'tk2': tk2,
            'type': 'pch5',
            'video_id': url.split('/', 5)[-1].split('.')[0],
            '_support': '10000000',
            'auth_mode': '',
            'src': '',
            'abroad': '',
        }
        response = self.session.get(self.video_url, params=params)
        response_json = response.json()
        title = response_json['data'].get('info', {}).get('title', f'视频走丢啦_{time.time()}')
        pm2 = response_json['data']['atc']['pm2']
        # 进行请求, 默认下载清晰度最高的
        params = {
            '_support': '10000000',
            'tk2': tk2,
            'pm2': pm2,
            'video_id': url.split('/', 5)[-1].split('.')[0],
            'type': 'pch5',
            'auth_mode': '',
            'src': '',
            'abroad': '',
        }
        response = self.session.get(self.getSource_url, headers=self.headers, params=params)
        response_json = response.json()
        for domian in response_json['data']['stream_domain']:
            stream_url = domian + response_json['data']['stream'][-1]['url']
            response = self.session.get(stream_url)
            if response.json().get('info', ''): 
                download_url = response.json()['info']
                break
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
        self.video_url = 'https://pcweb.api.mgtv.com/player/video'
        self.getSource_url = 'https://pcweb.api.mgtv.com/player/getSource'
        self.pno = '1030'
        self.did = 'e6e13014-393b-43e7-b6be-2323e4960939'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['mgtv.com']
        for host in valid_hosts:
            if host in url: return True
        return False