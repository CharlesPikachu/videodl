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
from .nuvid import NuVidVideoClient
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
from .leshi import LeshiVideoClient
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
from .eastday import EastDayVideoClient
from .kugoumv import KugouMVVideoClient
from .wittytv import WittyTVVideoClient
from .open163 import Open163VideoClient
from .foxnews import FoxNewsVideoClient
from .youtube import YouTubeVideoClient
from .rednote import RednoteVideoClient
from .sixroom import SixRoomVideoClient
from .tencent import TencentVideoClient
from .xuexicn import XuexiCNVideoClient
from .cctvnews import CCTVNewsVideoClient
from .playerpl import PlayerPLVideoClient
from .plusfifa import PlusFIFAVideoClient
from .kuaishou import KuaishouVideoClient
from .bilibili import BilibiliVideoClient
from .yinyuetai import YinyuetaiVideoClient
from .duxiaoshi import DuxiaoshiVideoClient
from .dongchedi import DongchediVideoClient
from .kankannews import KanKanNewsVideoClient
from .baidutieba import BaiduTiebaVideoClient
from .eyepetizer import EyepetizerVideoClient
from .chinadaily import ChinaDailyVideoClient
from .pipigaoxiao import PipigaoxiaoVideoClient
from .xinpianchang import XinpianchangVideoClient


'''VideoClientBuilder'''
class VideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = video_clients = {
        'ABCVideoClient': ABCVideoClient,                   'AcFunVideoClient': AcFunVideoClient,               'ArteTVVideoClient': ArteTVVideoClient,             'BaiduTiebaVideoClient': BaiduTiebaVideoClient,
        'BeaconVideoClient': BeaconVideoClient,             'BilibiliVideoClient': BilibiliVideoClient,         'C56VideoClient': C56VideoClient,                   'CCCVideoClient': CCCVideoClient,
        'CCtalkVideoClient': CCtalkVideoClient,             'DongchediVideoClient': DongchediVideoClient,       'DouyinVideoClient': DouyinVideoClient,             'CCTVNewsVideoClient': CCTVNewsVideoClient,
        'DuxiaoshiVideoClient': DuxiaoshiVideoClient,       'EyepetizerVideoClient': EyepetizerVideoClient,     'FoxNewsVideoClient': FoxNewsVideoClient,           'GeniusVideoClient': GeniusVideoClient,
        'HaokanVideoClient': HaokanVideoClient,             'HuyaVideoClient': HuyaVideoClient,                 'IQiyiVideoClient': IQiyiVideoClient,               'KakaoVideoClient': KakaoVideoClient,
        'Ku6VideoClient': Ku6VideoClient,                   'KuaishouVideoClient': KuaishouVideoClient,         'KugouMVVideoClient': KugouMVVideoClient,           'M1905VideoClient': M1905VideoClient,
        'MGTVVideoClient': MGTVVideoClient,                 'MeipaiVideoClient': MeipaiVideoClient,             'OasisVideoClient': OasisVideoClient,               'Open163VideoClient': Open163VideoClient,
        'PearVideoClient': PearVideoClient,                 'PipigaoxiaoVideoClient': PipigaoxiaoVideoClient,   'PipixVideoClient': PipixVideoClient,               'PlayerPLVideoClient': PlayerPLVideoClient,
        'PlusFIFAVideoClient': PlusFIFAVideoClient,         'RedditVideoClient': RedditVideoClient,             'RednoteVideoClient': RednoteVideoClient,           'SinaVideoClient': SinaVideoClient,
        'SixRoomVideoClient': SixRoomVideoClient,           'SohuVideoClient': SohuVideoClient,                 'TBNUKVideoClient': TBNUKVideoClient,               'TedVideoClient': TedVideoClient,
        'TencentVideoClient': TencentVideoClient,           'UnityVideoClient': UnityVideoClient,               'WWEVideoClient': WWEVideoClient,                   'WeSingVideoClient': WeSingVideoClient,
        'WeiboVideoClient': WeiboVideoClient,               'WeishiVideoClient': WeishiVideoClient,             'WittyTVVideoClient': WittyTVVideoClient,           'XiguaVideoClient': XiguaVideoClient,
        'XinpianchangVideoClient': XinpianchangVideoClient, 'XuexiCNVideoClient': XuexiCNVideoClient,           'YinyuetaiVideoClient': YinyuetaiVideoClient,       'YouTubeVideoClient': YouTubeVideoClient,
        'YoukuVideoClient': YoukuVideoClient,               'ZhihuVideoClient': ZhihuVideoClient,               'ZuiyouVideoClient': ZuiyouVideoClient,             'LeshiVideoClient': LeshiVideoClient,
        'KanKanNewsVideoClient': KanKanNewsVideoClient,     'NuVidVideoClient': NuVidVideoClient,               'ChinaDailyVideoClient': ChinaDailyVideoClient,     'EastDayVideoClient': EastDayVideoClient,
        'CCTVVideoClient': CCTVVideoClient,                 
    }


'''BuildVideoClient'''
BuildVideoClient = VideoClientBuilder().build