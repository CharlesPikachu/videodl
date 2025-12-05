'''initialize'''
from .kedou import KedouVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder
from .snapany import SnapAnyVideoClient


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'IIILabVideoClient': IIILabVideoClient, 'KedouVideoClient': KedouVideoClient, 'SnapAnyVideoClient': SnapAnyVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build