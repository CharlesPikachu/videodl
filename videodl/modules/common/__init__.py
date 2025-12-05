'''initialize'''
from .kedou import KedouVideoClient
from ..utils import BaseModuleBuilder


'''CommonVideoClientBuilder'''
class CommonVideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'KedouVideoClient': KedouVideoClient,
    }


'''BuildCommonVideoClient'''
BuildCommonVideoClient = CommonVideoClientBuilder().build