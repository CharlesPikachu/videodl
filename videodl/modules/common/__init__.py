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
from .qwkuns import QwkunsVideoClient
from .lvlong import LvlongVideoClient
from .snapwc import SnapWCVideoClient
from .nologo import NoLogoVideoClient
from .im1907 import IM1907VideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .videofk import VideoFKVideoClient
from .longzhu import LongZhuVideoClient
from .snapany import SnapAnyVideoClient
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
        'IM1907VideoClient': IM1907VideoClient, 'XMFlvVideoClient': XMFlvVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient, 'GVVideoClient': GVVideoClient, 'IIILabVideoClient': IIILabVideoClient, 'VideoFKVideoClient': VideoFKVideoClient, 
        'RayVideoClient': RayVideoClient, 'SnapWCVideoClient': SnapWCVideoClient, 'VgetVideoClient': VgetVideoClient, 'SENJiexiVideoClient': SENJiexiVideoClient, 'AnyFetcherVideoClient': AnyFetcherVideoClient, 'PVVideoClient': PVVideoClient, 
        'KedouVideoClient': KedouVideoClient, 'ODwonVideoClient': ODwonVideoClient, 'KuKuToolVideoClient': KuKuToolVideoClient, 'SpapiVideoClient': SpapiVideoClient, 'XiaolvfangVideoClient': XiaolvfangVideoClient, 'BVVideoClient': BVVideoClient, 
        'QwkunsVideoClient': QwkunsVideoClient, 'WoofVideoClient': WoofVideoClient, 'KIT9VideoClient': KIT9VideoClient, 'MiZhiVideoClient': MiZhiVideoClient, 'QZXDPToolsVideoClient': QZXDPToolsVideoClient, 'BugPkVideoClient': BugPkVideoClient, 
        'NoLogoVideoClient': NoLogoVideoClient, 'QingtingVideoClient': QingtingVideoClient, 'XCVTSVideoClient': XCVTSVideoClient, 'GVVIPVideoClient': GVVIPVideoClient, 'LongZhuVideoClient': LongZhuVideoClient, 'XZDXVideoClient': XZDXVideoClient, 
        'ZanqianbaVideoClient': ZanqianbaVideoClient, 'LvlongVideoClient': LvlongVideoClient, 'XiazaitoolVideoClient': XiazaitoolVideoClient, 
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build