'''initialize'''
from .vget import VgetVideoClient
from .xmflv import XMFlvVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .longzhu import LongZhuVideoClient
from .snapany import SnapAnyVideoClient
from .iloveapi import ILoveAPIVideoClient
from .kukutool import KuKuToolsVideoClient
from .youchuang import YouChuangVideoClient
from .qzxdptools import QZXDPToolsVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'IIILabVideoClient': IIILabVideoClient, 'KedouVideoClient': KedouVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient,
        'GVVIPVideoClient': GVVIPVideoClient, 'VgetVideoClient': VgetVideoClient, 'ILoveAPIVideoClient': ILoveAPIVideoClient,
        'XMFlvVideoClient': XMFlvVideoClient, 'QZXDPToolsVideoClient': QZXDPToolsVideoClient, 'YouChuangVideoClient': YouChuangVideoClient,
        'KuKuToolsVideoClient': KuKuToolsVideoClient, 'LongZhuVideoClient': LongZhuVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build