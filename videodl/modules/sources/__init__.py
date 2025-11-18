'''initialize'''
from .ted import TedVideoClient
from .ku6 import Ku6VideoClient
from .base import BaseVideoClient
from .acfun import AcFunVideoClient
from .pipix import PipixVideoClient
from .mgtv import MGTVkanVideoClient
from .haokan import HaokanVideoClient
from ..utils import BaseModuleBuilder
from .kuaishou import KuaishouVideoClient
from .bilibili import BilibiliVideoClient
from .yinyuetai import YinyuetaiVideoClient
from .baidutieba import BaiduTiebaVideoClient
from .pipigaoxiao import PipigaoxiaoVideoClient


'''VideoClientBuilder'''
class VideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'AcFunVideoClient': AcFunVideoClient, 'HaokanVideoClient': HaokanVideoClient, 'TedVideoClient': TedVideoClient,
        'PipigaoxiaoVideoClient': PipigaoxiaoVideoClient, 'PipixVideoClient': PipixVideoClient, 'Ku6VideoClient': Ku6VideoClient,
        'KuaishouVideoClient': KuaishouVideoClient, 'BilibiliVideoClient': BilibiliVideoClient, 'YinyuetaiVideoClient': YinyuetaiVideoClient,
        'BaiduTiebaVideoClient': BaiduTiebaVideoClient, 'MGTVkanVideoClient': MGTVkanVideoClient,
    }


'''VideoClientBuilder'''
BuildVideoClient = VideoClientBuilder().build