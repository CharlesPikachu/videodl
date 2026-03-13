'''initialize'''
from .abc import ABCVideoClient
from .wwe import WWEVideoClient
from .ted import TedVideoClient
from .ku6 import Ku6VideoClient
from .c56 import C56VideoClient
from .ccc import CCCVideoClient
from .pear import PearVideoClient
from .huya import HuyaVideoClient
from .sina import SinaVideoClient
from .base import BaseVideoClient
from .mgtv import MGTVVideoClient
from .cctv import CCTVVideoClient
from .sohu import SohuVideoClient
from .tbnuk import TBNUKVideoClient
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
from .douyin import DouyinVideoClient
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
from .beacon import BeaconVideoClient
from .kugoumv import KugouMVVideoClient
from .wittytv import WittyTVVideoClient
from .open163 import Open163VideoClient
from .foxnews import FoxNewsVideoClient
from .youtube import YouTubeVideoClient
from .rednote import RednoteVideoClient
from .sixroom import SixRoomVideoClient
from .tencent import TencentVideoClient
from .xuexicn import XuexiCNVideoClient
from .plusfifa import PlusFIFAVideoClient
from .kuaishou import KuaishouVideoClient
from .bilibili import BilibiliVideoClient
from .yinyuetai import YinyuetaiVideoClient
from .duxiaoshi import DuxiaoshiVideoClient
from .dongchedi import DongchediVideoClient
from .baidutieba import BaiduTiebaVideoClient
from .eyepetizer import EyepetizerVideoClient
from .pipigaoxiao import PipigaoxiaoVideoClient
from .xinpianchang import XinpianchangVideoClient


'''VideoClientBuilder'''
class VideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'CCCVideoClient': CCCVideoClient, 'BilibiliVideoClient': BilibiliVideoClient, 'AcFunVideoClient': AcFunVideoClient, 'HaokanVideoClient': HaokanVideoClient, 'YinyuetaiVideoClient': YinyuetaiVideoClient,
        'HuyaVideoClient': HuyaVideoClient, 'TedVideoClient': TedVideoClient, 'PipigaoxiaoVideoClient': PipigaoxiaoVideoClient, 'PipixVideoClient': PipixVideoClient, 'PlusFIFAVideoClient': PlusFIFAVideoClient,
        'BaiduTiebaVideoClient': BaiduTiebaVideoClient, 'MGTVVideoClient': MGTVVideoClient, 'OasisVideoClient': OasisVideoClient, 'MeipaiVideoClient': MeipaiVideoClient, 'ZuiyouVideoClient': ZuiyouVideoClient,
        'DuxiaoshiVideoClient': DuxiaoshiVideoClient, 'Ku6VideoClient': Ku6VideoClient, 'RednoteVideoClient': RednoteVideoClient, 'WeiboVideoClient': WeiboVideoClient, 'Open163VideoClient': Open163VideoClient,
        'KuaishouVideoClient': KuaishouVideoClient, 'WeishiVideoClient': WeishiVideoClient, 'ZhihuVideoClient': ZhihuVideoClient, 'YouTubeVideoClient': YouTubeVideoClient, 'M1905VideoClient': M1905VideoClient, 
        'XinpianchangVideoClient': XinpianchangVideoClient, 'ArteTVVideoClient': ArteTVVideoClient, 'WWEVideoClient': WWEVideoClient, 'DouyinVideoClient': DouyinVideoClient, 'C56VideoClient': C56VideoClient,
        'DongchediVideoClient': DongchediVideoClient, 'FoxNewsVideoClient': FoxNewsVideoClient, 'SinaVideoClient': SinaVideoClient, 'XuexiCNVideoClient': XuexiCNVideoClient, 'PearVideoClient': PearVideoClient, 
        'SixRoomVideoClient': SixRoomVideoClient, 'WeSingVideoClient': WeSingVideoClient, 'XiguaVideoClient': XiguaVideoClient, 'TencentVideoClient': TencentVideoClient, 'GeniusVideoClient': GeniusVideoClient, 
        'CCtalkVideoClient': CCtalkVideoClient, 'RedditVideoClient': RedditVideoClient, 'IQiyiVideoClient': IQiyiVideoClient,   'WittyTVVideoClient': WittyTVVideoClient, 'YoukuVideoClient': YoukuVideoClient, 
        'CCTVVideoClient': CCTVVideoClient, 'SohuVideoClient': SohuVideoClient, 'EyepetizerVideoClient': EyepetizerVideoClient, 'KugouMVVideoClient': KugouMVVideoClient, 'UnityVideoClient': UnityVideoClient, 
        'KakaoVideoClient': KakaoVideoClient, 'BeaconVideoClient': BeaconVideoClient, 'ABCVideoClient': ABCVideoClient, 'TBNUKVideoClient': TBNUKVideoClient, 
    }


'''BuildVideoClient'''
BuildVideoClient = VideoClientBuilder().build