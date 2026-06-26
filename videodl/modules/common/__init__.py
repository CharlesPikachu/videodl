'''initialize'''
from .bv import BVVideoClient
from .pv import PVVideoClient
from .gv import GVVideoClient
from .ray import RayVideoClient
from .vget import VgetVideoClient
from .kit9 import KIT9VideoClient
from .apicx import APICXVideoClient
from .spapi import SpapiVideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .bugpk import BugPkVideoClient
from .mizhi import MiZhiVideoClient
from .xcvts import XCVTSVideoClient
from .odown import ODwonVideoClient
from .wzjun import WzjunVideoClient
from .kuleu import KuLeuVideoClient
from .snapwc import SnapWCVideoClient
from .nologo import NoLogoVideoClient
from .im1907 import IM1907VideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .jxm3u8 import JXM3U8VideoClient
from .jisuyun import JisuYunVideoClient
from .videofk import VideoFKVideoClient
from .longzhu import LongZhuVideoClient
from .snapany import SnapAnyVideoClient
from .qingqiu import QingQiuVideoClient
from .vthreads import VThreadsVideoClient
from .veedmate import VeedMateVideoClient
from .qingting import QingtingVideoClient
from .kukutool import KuKuToolVideoClient
from .senjiexi import SENJiexiVideoClient
from .zanqianba import ZanqianbaVideoClient
from .xiaolvfang import XiaolvfangVideoClient
from .anyfetcher import AnyFetcherVideoClient
from .qzxdptools import QZXDPToolsVideoClient
from .xiazaitool import XiazaitoolVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'SnapAnyVideoClient': SnapAnyVideoClient,        'GVVideoClient': GVVideoClient,                  'SnapWCVideoClient': SnapWCVideoClient,          'IM1907VideoClient': IM1907VideoClient,
        'XMFlvVideoClient': XMFlvVideoClient,            'IIILabVideoClient': IIILabVideoClient,          'RayVideoClient': RayVideoClient,                'VeedMateVideoClient': VeedMateVideoClient,
        'VideoFKVideoClient': VideoFKVideoClient,        'VThreadsVideoClient': VThreadsVideoClient,      'SENJiexiVideoClient': SENJiexiVideoClient,      'JXM3U8VideoClient': JXM3U8VideoClient,
        'VgetVideoClient': VgetVideoClient,              'AnyFetcherVideoClient': AnyFetcherVideoClient,  'PVVideoClient': PVVideoClient,                  'KedouVideoClient': KedouVideoClient,
        'ODwonVideoClient': ODwonVideoClient,            'KuKuToolVideoClient': KuKuToolVideoClient,      'APICXVideoClient': APICXVideoClient,            'SpapiVideoClient': SpapiVideoClient,
        'QingQiuVideoClient': QingQiuVideoClient,        'WzjunVideoClient': WzjunVideoClient,            'XiaolvfangVideoClient': XiaolvfangVideoClient,  'BVVideoClient': BVVideoClient,
        'KuLeuVideoClient': KuLeuVideoClient,            'KIT9VideoClient': KIT9VideoClient,              'MiZhiVideoClient': MiZhiVideoClient,            'QZXDPToolsVideoClient': QZXDPToolsVideoClient,
        'BugPkVideoClient': BugPkVideoClient,            'NoLogoVideoClient': NoLogoVideoClient,          'GVVIPVideoClient': GVVIPVideoClient,            'JisuYunVideoClient': JisuYunVideoClient,
        'QingtingVideoClient': QingtingVideoClient,      'XCVTSVideoClient': XCVTSVideoClient,            'XiazaitoolVideoClient': XiazaitoolVideoClient,  'ZanqianbaVideoClient': ZanqianbaVideoClient,
        'LongZhuVideoClient': LongZhuVideoClient,        
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build