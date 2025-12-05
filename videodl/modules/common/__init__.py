'''initialize'''
from .kedou import KedouVideoClient
from .iiilab import IIILabVideoClient
from ..utils import BaseModuleBuilder


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'IIILabVideoClient': IIILabVideoClient, 'KedouVideoClient': KedouVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build