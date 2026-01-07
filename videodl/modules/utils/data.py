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
        'source': None, 'raw_data': 'NULL', 'download_url': 'NULL', 'title': 'NULL', 'file_path': 'NULL', 'ext': 'mp4', 
        'download_with_ffmpeg': False, 'download_with_aria2c': False, 'download_with_ffmpeg_cctv': False, 'err_msg': "NULL", 
        'identifier': 'NULL', 'guess_video_ext_result': 'NULL', 'enable_nm3u8dlre': False, 'audio_download_url': 'NULL',
        'guess_audio_ext_result': 'NULL', 'audio_ext': 'm4a', 'audio_file_path': 'NULL',
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