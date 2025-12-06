'''initialize'''
from .vget import VgetVideoClient
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .snapany import SnapAnyVideoClient
from .iloveapi import ILoveAPIVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'IIILabVideoClient': IIILabVideoClient, 'KedouVideoClient': KedouVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient,
        'GVVIPVideoClient': GVVIPVideoClient, 'VgetVideoClient': VgetVideoClient, 'ILoveAPIVideoClient': ILoveAPIVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build