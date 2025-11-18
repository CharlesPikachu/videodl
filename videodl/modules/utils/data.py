'''
Function:
    Implementation of Data format related utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import functools


'''VideoInfo'''
class VideoInfo(dict):
    _defaults = {
        'source': None, 'raw_data': 'NULL', 'download_url': 'NULL', 'title': 'NULL', 'file_path': 'NULL',
        'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': "NULL",
    }
    def __init__(self, *args, **kwargs):
        data = dict(self._defaults)
        data.update(dict(*args, **kwargs))
        super(VideoInfo, self).__init__(data)
    '''__getattr__'''
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f'"VideoInfo" object has no attribute "{item}"')
    '''__setattr__'''
    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self[key] = value
    '''__delattr__'''
    def __delattr__(self, item):
        if item.startswith('_'):
            object.__delattr__(self, item)
        else:
            try:
                del self[item]
            except KeyError:
                raise AttributeError(f'"VideoInfo" object has no attribute "{item}"')