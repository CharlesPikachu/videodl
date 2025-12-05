'''initialize'''
from .gvvip import GVVIPVideoClient
from .kedou import KedouVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .snapany import SnapAnyVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'IIILabVideoClient': IIILabVideoClient, 'KedouVideoClient': KedouVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient,
        'GVVIPVideoClient': GVVIPVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build