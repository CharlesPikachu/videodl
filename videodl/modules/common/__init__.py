'''initialize'''
from .bv import BVVideoClient
from .pv import PVVideoClient
from .gv import GVVideoClient
from .ray import RayVideoClient
from .xzdx import XZDXVideoClient
from .vget import VgetVideoClient
from .kit9 import KIT9VideoClient
from .woof import WoofVideoClient
from .spapi import SpapiVideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .bugpk import BugPkVideoClient
from .mizhi import MiZhiVideoClient
from .xcvts import XCVTSVideoClient
from .odown import ODwonVideoClient
from .wzjun import WzjunVideoClient
from .qwkuns import QwkunsVideoClient
from .lvlong import LvlongVideoClient
from .snapwc import SnapWCVideoClient
from .nologo import NoLogoVideoClient
from .im1907 import IM1907VideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .jxm3u8 import JXM3U8VideoClient
from .videofk import VideoFKVideoClient
from .longzhu import LongZhuVideoClient
from .snapany import SnapAnyVideoClient
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
        'SnapAnyVideoClient': SnapAnyVideoClient,        'GVVideoClient': GVVideoClient,                  'IM1907VideoClient': IM1907VideoClient,          'XMFlvVideoClient': XMFlvVideoClient,
        'IIILabVideoClient': IIILabVideoClient,          'RayVideoClient': RayVideoClient,                'SnapWCVideoClient': SnapWCVideoClient,          'VeedMateVideoClient': VeedMateVideoClient,
        'VideoFKVideoClient': VideoFKVideoClient,        'VThreadsVideoClient': VThreadsVideoClient,      'SENJiexiVideoClient': SENJiexiVideoClient,      'JXM3U8VideoClient': JXM3U8VideoClient,
        'VgetVideoClient': VgetVideoClient,              'AnyFetcherVideoClient': AnyFetcherVideoClient,  'PVVideoClient': PVVideoClient,                  'KedouVideoClient': KedouVideoClient,
        'ODwonVideoClient': ODwonVideoClient,            'KuKuToolVideoClient': KuKuToolVideoClient,      'SpapiVideoClient': SpapiVideoClient,            'WzjunVideoClient': WzjunVideoClient,
        'QwkunsVideoClient': QwkunsVideoClient,          'XiaolvfangVideoClient': XiaolvfangVideoClient,  'BVVideoClient': BVVideoClient,                  'WoofVideoClient': WoofVideoClient,
        'KIT9VideoClient': KIT9VideoClient,              'MiZhiVideoClient': MiZhiVideoClient,            'QZXDPToolsVideoClient': QZXDPToolsVideoClient,  'BugPkVideoClient': BugPkVideoClient,
        'NoLogoVideoClient': NoLogoVideoClient,          'GVVIPVideoClient': GVVIPVideoClient,            'QingtingVideoClient': QingtingVideoClient,      'XCVTSVideoClient': XCVTSVideoClient,
        'LongZhuVideoClient': LongZhuVideoClient,        'XiazaitoolVideoClient': XiazaitoolVideoClient,  'ZanqianbaVideoClient': ZanqianbaVideoClient,    'XZDXVideoClient': XZDXVideoClient,
        'LvlongVideoClient': LvlongVideoClient,           
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build