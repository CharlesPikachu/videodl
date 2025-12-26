'''initialize'''
from .wwe import WWEVideoClient
from .ted import TedVideoClient
from .ku6 import Ku6VideoClient
from .c56 import C56VideoClient
from .pear import PearVideoClient
from .huya import HuyaVideoClient
from .sina import SinaVideoClient
from .base import BaseVideoClient
from .mgtv import MGTVVideoClient
from .cctv import CCTVVideoClient
from .sohu import SohuVideoClient
from .unity import UnityVideoClient
from .acfun import AcFunVideoClient
from .xigua import XiguaVideoClient
from .pipix import PipixVideoClient
from .oasis import OasisVideoClient
from .weibo import WeiboVideoClient
from .zhihu import ZhihuVideoClient
from .kakao import KakaoVideoClient
from .youku import YoukuVideoClient
from .m1905 import M1905VideoClient
from .iqiyi import IQiyiVideoClient
from .artetv import ArteTVVideoClient
from .reddit import RedditVideoClient
from .genius import GeniusVideoClient
from .weishi import WeishiVideoClient
from .haokan import HaokanVideoClient
from .zuiyou import ZuiyouVideoClient
from .meipai import MeipaiVideoClient
from ..utils import BaseModuleBuilder
from .wesing import WeSingVideoClient
from .cctalk import CCtalkVideoClient
from .open163 import Open163VideoClient
from .foxnews import FoxNewsVideoClient
from .youtube import YouTubeVideoClient
from .rednote import RednoteVideoClient
from .sixroom import SixRoomVideoClient
from .tencent import TencentVideoClient
from .xuexicn import XuexiCNVideoClient
from .kuaishou import KuaishouVideoClient
from .bilibili import BilibiliVideoClient
from .yinyuetai import YinyuetaiVideoClient
from .duxiaoshi import DuxiaoshiVideoClient
from .baidutieba import BaiduTiebaVideoClient
from .eyepetizer import EyepetizerVideoClient
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
        'CCTVVideoClient': CCTVVideoClient, 'SohuVideoClient': SohuVideoClient, 'YouTubeVideoClient': YouTubeVideoClient,
        'ZhihuVideoClient': ZhihuVideoClient, 'KakaoVideoClient': KakaoVideoClient, 'YoukuVideoClient': YoukuVideoClient,
        'TencentVideoClient': TencentVideoClient, 'GeniusVideoClient': GeniusVideoClient, 'UnityVideoClient': UnityVideoClient,
        'FoxNewsVideoClient': FoxNewsVideoClient, 'SinaVideoClient': SinaVideoClient, 'XuexiCNVideoClient': XuexiCNVideoClient,
        'Open163VideoClient': Open163VideoClient, 'CCtalkVideoClient': CCtalkVideoClient, 'EyepetizerVideoClient': EyepetizerVideoClient,
        'ArteTVVideoClient': ArteTVVideoClient, 'C56VideoClient': C56VideoClient, 'RedditVideoClient': RedditVideoClient,
        'WWEVideoClient': WWEVideoClient, 'M1905VideoClient': M1905VideoClient, 'IQiyiVideoClient': IQiyiVideoClient,
    }


'''BuildVideoClient'''
BuildVideoClient = VideoClientBuilder().build