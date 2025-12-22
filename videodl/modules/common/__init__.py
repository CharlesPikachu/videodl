'''initialize'''
from .vget import VgetVideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .bugpk import BugPkVideoClient
from .snapwc import SnapWCVideoClient
from .nologo import NoLogoVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .longzhu import LongZhuVideoClient
from .snapany import SnapAnyVideoClient
from .iloveapi import ILoveAPIVideoClient
from .kukutool import KuKuToolsVideoClient
from .zanqianba import ZanqianbaVideoClient
from .cenguigui import CenguiguiVideoClient
from .qzxdptools import QZXDPToolsVideoClient
from .xiazaitool import XiazaitoolVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'SnapWCVideoClient': SnapWCVideoClient, 'IIILabVideoClient': IIILabVideoClient, 'KedouVideoClient': KedouVideoClient, 
        'SnapAnyVideoClient': SnapAnyVideoClient, 'XMFlvVideoClient': XMFlvVideoClient, 'VgetVideoClient': VgetVideoClient, 
        'GVVIPVideoClient': GVVIPVideoClient, 'QZXDPToolsVideoClient': QZXDPToolsVideoClient, 'LongZhuVideoClient': LongZhuVideoClient,
        'KuKuToolsVideoClient': KuKuToolsVideoClient, 'XiazaitoolVideoClient': XiazaitoolVideoClient, 'NoLogoVideoClient': NoLogoVideoClient,
        'ILoveAPIVideoClient': ILoveAPIVideoClient, 'BugPkVideoClient': BugPkVideoClient, 'ZanqianbaVideoClient': ZanqianbaVideoClient,
        'CenguiguiVideoClient': CenguiguiVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build