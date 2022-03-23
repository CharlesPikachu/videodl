'''
Function:
    皮皮虾视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
from .base import Base
from ..utils import filterBadCharacter


'''皮皮虾视频下载器类'''
class Pipix(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Pipix, self).__init__(config, logger_handle, **kwargs)
        self.source = 'pipix'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        item_id = re.findall(r'item/(\d+)', url)[0]
        url = self.detail_url.format(item_id)
        response = self.session.get(url)
        response_json = response.json()
        videoinfo = {
            'source': self.source,
            'download_url': response_json['data']['item']['video']['video_download']['url_list'][0]['url'],
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(response_json['data']['item']['share']['title']),
            'ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
        }
        self.detail_url = 'https://h5.pipix.com/bds/webapi/item/detail/?item_id={}&source=share'
        self.session.headers.update(self.headers)
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['h5.pipix.com']
        for host in valid_hosts:
            if host in url: return True
        return False