'''
Function:
    Implementation of Data format related utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from typing import Any


'''VideoInfo'''
class VideoInfo(dict):
    _defaults = {
        'source': None, 'raw_data': {}, 'download_url': '', 'title': '', 'file_path': '', 'ext': 'mp4', 'err_msg': '', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 
        'aria2c_settings': {}, 'enable_nm3u8dlre': False, 'nm3u8dlre_settings': {}, 'identifier': '', 'guess_video_ext_result': {}, 'audio_download_url': '', 'guess_audio_ext_result': {}, 
        'audio_ext': 'm4a', 'audio_file_path': '', 'default_download_headers': None, 'default_download_cookies': None, 'cover_url': None,
    }
    def __init__(self, *args, **kwargs):
        data = dict(self._defaults)
        data.update(dict(*args, **kwargs))
        super(VideoInfo, self).__init__(data)
    '''getattr'''
    def __getattr__(self, item):
        try: return self[item]
        except KeyError: raise AttributeError(f'"VideoInfo" object has no attribute "{item}"')
    '''setattr'''
    def __setattr__(self, key: str, value: Any):
        if key.startswith('_'): object.__setattr__(self, key, value)
        else: self[key] = value
    '''delattr'''
    def __delattr__(self, item: str):
        if item.startswith('_'): object.__delattr__(self, item)
        else:
            try: del self[item]
            except KeyError: raise AttributeError(f'"VideoInfo" object has no attribute "{item}"')