'''initialize'''
from .ted import TedVideoClient
from .ku6 import Ku6VideoClient
from .pear import PearVideoClient
from .huya import HuyaVideoClient
from .base import BaseVideoClient
from .mgtv import MGTVVideoClient
from .cctv import CCTVVideoClient
from .acfun import AcFunVideoClient
from .xigua import XiguaVideoClient
from .pipix import PipixVideoClient
from .oasis import OasisVideoClient
from .weibo import WeiboVideoClient
from .weishi import WeishiVideoClient
from .haokan import HaokanVideoClient
from .zuiyou import ZuiyouVideoClient
from .meipai import MeipaiVideoClient
from ..utils import BaseModuleBuilder
from .wesing import WeSingVideoClient
from .rednote import RednoteVideoClient
from .sixroom import SixRoomVideoClient
from .kuaishou import KuaishouVideoClient
from .bilibili import BilibiliVideoClient
from .yinyuetai import YinyuetaiVideoClient
from .duxiaoshi import DuxiaoshiVideoClient
from .baidutieba import BaiduTiebaVideoClient
from .pipigaoxiao import PipigaoxiaoVideoClient
from .xinpianchang import XinpianchangVideoClient


'''VideoClientBuilder'''
class VideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'AcFunVideoClient': AcFunVideoClient, 'HaokanVideoClient': HaokanVideoClient, 'TedVideoClient': TedVideoClient,
        'PipigaoxiaoVideoClient': PipigaoxiaoVideoClient, 'PipixVideoClient': PipixVideoClient, 'Ku6VideoClient': Ku6VideoClient,
        'KuaishouVideoClient': KuaishouVideoClient, 'BilibiliVideoClient': BilibiliVideoClient, 'YinyuetaiVideoClient': YinyuetaiVideoClient,
        'BaiduTiebaVideoClient': BaiduTiebaVideoClient, 'MGTVVideoClient': MGTVVideoClient, 'OasisVideoClient': OasisVideoClient,
        'PearVideoClient': PearVideoClient, 'HuyaVideoClient': HuyaVideoClient, 'MeipaiVideoClient': MeipaiVideoClient,
        'WeishiVideoClient': WeishiVideoClient, 'SixRoomVideoClient': SixRoomVideoClient, 'DuxiaoshiVideoClient': DuxiaoshiVideoClient,
        'ZuiyouVideoClient': ZuiyouVideoClient, 'XinpianchangVideoClient': XinpianchangVideoClient, 'WeSingVideoClient': WeSingVideoClient,
        'XiguaVideoClient': XiguaVideoClient, 'RednoteVideoClient': RednoteVideoClient, 'WeiboVideoClient': WeiboVideoClient,
        'CCTVVideoClient': CCTVVideoClient,
    }


'''VideoClientBuilder'''
BuildVideoClient = VideoClientBuilder().build