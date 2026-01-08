'''initialize'''
from .bv import BVVideoClient
from .vget import VgetVideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .bugpk import BugPkVideoClient
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
        'XMFlvVideoClient': XMFlvVideoClient, 'VideoFKVideoClient': VideoFKVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient, 'IIILabVideoClient': IIILabVideoClient,
        'VgetVideoClient': VgetVideoClient, 'SnapWCVideoClient': SnapWCVideoClient, 'KedouVideoClient': KedouVideoClient, 'KuKuToolVideoClient': KuKuToolVideoClient, 
        'QZXDPToolsVideoClient': QZXDPToolsVideoClient, 'BugPkVideoClient': BugPkVideoClient, 'NoLogoVideoClient': NoLogoVideoClient, 'LongZhuVideoClient': LongZhuVideoClient, 
        'ZanqianbaVideoClient': ZanqianbaVideoClient, 'BVVideoClient': BVVideoClient, 'XiazaitoolVideoClient': XiazaitoolVideoClient, 'QingtingVideoClient': QingtingVideoClient, 
        'GVVIPVideoClient': GVVIPVideoClient, 
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build