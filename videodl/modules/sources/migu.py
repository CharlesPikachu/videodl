'''
Function:
    咪咕视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import time
from .base import Base
from ..utils.misc import *


'''咪咕视频下载器类'''
class Migu(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Migu, self).__init__(config, logger_handle, **kwargs)
        self.source = 'migu'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        # 获得下载链接
        params = {
            'contId': url.split('?')[-1].split('=')[-1],
            'clientId': '2e2919355618c3465540e0d7b0e98642',
        }
        response = self.session.get(self.play_url, params=params, headers=self.headers)
        response_json = response.json()
        download_url, params_dict = response_json['body']['urlInfo']['url'], {}
        # 获得真实下载链接
        for c in download_url.split('&'):
            params_dict[c.split('=')[0]] = c.split('=')[1]
        data, p, ddCalcu = list(params_dict['puData']), 0, []
        while (2 * p) < len(data):
            ddCalcu.append(data[len(data) - p - 1])
            if p < len(data) - p - 1: ddCalcu.append(params_dict['puData'][p])
            if p == 1: ddCalcu.append('e')
            if p == 2: ddCalcu.append(list(params_dict['timestamp'])[6])
            if p == 3: ddCalcu.append(list(params_dict['ProgramID'])[2])
            if p == 4: ddCalcu.append(list(params_dict['Channel_ID'])[len(list(params_dict['Channel_ID'])) - 4])
            p += 1
        ddCalcu = ''.join(ddCalcu)
        # 构造videoinfo
        download_url = f'{download_url}&ddCalcu={ddCalcu}'
        title = response_json.get('body', {}).get('content', {}).get('contName', f'视频走丢啦_{time.time()}')
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': '_'.join([self.source, filterBadCharacter(title)]),
            'ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        self.play_url = 'https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['miguvideo.com']
        for host in valid_hosts:
            if host in url: return True
        return False