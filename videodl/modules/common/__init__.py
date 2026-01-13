'''initialize'''
from .bv import BVVideoClient
from .pv import PVVideoClient
from .ray import RayVideoClient
from .xzdx import XZDXVideoClient
from .vget import VgetVideoClient
from .kit9 import KIT9VideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .bugpk import BugPkVideoClient
from .mizhi import MiZhiVideoClient
from .xcvts import XCVTSVideoClient
from .snapwc import SnapWCVideoClient
from .nologo import NoLogoVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .videofk import VideoFKVideoClient
from .longzhu import LongZhuVideoClient
from .snapany import SnapAnyVideoClient
from .qingting import QingtingVideoClient
from .kukutool import KuKuToolVideoClient
from .zanqianba import ZanqianbaVideoClient
from .qzxdptools import QZXDPToolsVideoClient
from .xiazaitool import XiazaitoolVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'XMFlvVideoClient': XMFlvVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient, 'PVVideoClient': PVVideoClient, 'IIILabVideoClient': IIILabVideoClient,
        'VideoFKVideoClient': VideoFKVideoClient, 'VgetVideoClient': VgetVideoClient, 'SnapWCVideoClient': SnapWCVideoClient, 'RayVideoClient': RayVideoClient, 
        'KedouVideoClient': KedouVideoClient, 'KuKuToolVideoClient': KuKuToolVideoClient, 'XZDXVideoClient': XZDXVideoClient, 'KIT9VideoClient': KIT9VideoClient, 
        'QZXDPToolsVideoClient': QZXDPToolsVideoClient, 'MiZhiVideoClient': MiZhiVideoClient, 'BugPkVideoClient': BugPkVideoClient, 'NoLogoVideoClient': NoLogoVideoClient, 
        'LongZhuVideoClient': LongZhuVideoClient, 'ZanqianbaVideoClient': ZanqianbaVideoClient, 'BVVideoClient': BVVideoClient, 'XiazaitoolVideoClient': XiazaitoolVideoClient, 
        'QingtingVideoClient': QingtingVideoClient, 'GVVIPVideoClient': GVVIPVideoClient, 'XCVTSVideoClient': XCVTSVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build