'''initialize'''
from .acfun import AcFunVideoClient
from .haokan import HaokanVideoClient
from ..utils import BaseModuleBuilder


'''VideoClientBuilder'''
class VideoClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'AcFunVideoClient': AcFunVideoClient, 'HaokanVideoClient': HaokanVideoClient,
    }


'''VideoClientBuilder'''
BuildVideoClient = VideoClientBuilder().build