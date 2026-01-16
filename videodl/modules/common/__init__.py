'''initialize'''
from .bv import BVVideoClient
from .pv import PVVideoClient
from .ray import RayVideoClient
from .xzdx import XZDXVideoClient
from .vget import VgetVideoClient
from .kit9 import KIT9VideoClient
from .nnxv import NNXVVideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .bugpk import BugPkVideoClient
from .mizhi import MiZhiVideoClient
from .xcvts import XCVTSVideoClient
from .odown import ODwonVideoClient
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
from .qzxdptools import QZXDPToolsVideoClient
from .xiazaitool import XiazaitoolVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'IM1907VideoClient': IM1907VideoClient, 'NNXVVideoClient': NNXVVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient, 'SENJiexiVideoClient': SENJiexiVideoClient, 
        'XMFlvVideoClient': XMFlvVideoClient, 'PVVideoClient': PVVideoClient, 'IIILabVideoClient': IIILabVideoClient, 'VideoFKVideoClient': VideoFKVideoClient, 
        'VgetVideoClient': VgetVideoClient, 'SnapWCVideoClient': SnapWCVideoClient, 'ODwonVideoClient': ODwonVideoClient, 'RayVideoClient': RayVideoClient, 
        'KedouVideoClient': KedouVideoClient, 'KuKuToolVideoClient': KuKuToolVideoClient, 'XZDXVideoClient': XZDXVideoClient, 'KIT9VideoClient': KIT9VideoClient, 
        'QZXDPToolsVideoClient': QZXDPToolsVideoClient, 'MiZhiVideoClient': MiZhiVideoClient, 'BugPkVideoClient': BugPkVideoClient, 'NoLogoVideoClient': NoLogoVideoClient, 
        'LongZhuVideoClient': LongZhuVideoClient, 'ZanqianbaVideoClient': ZanqianbaVideoClient, 'BVVideoClient': BVVideoClient, 'XiazaitoolVideoClient': XiazaitoolVideoClient, 
        'QingtingVideoClient': QingtingVideoClient, 'GVVIPVideoClient': GVVIPVideoClient, 'XCVTSVideoClient': XCVTSVideoClient, 
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build