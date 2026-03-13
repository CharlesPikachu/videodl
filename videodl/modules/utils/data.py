'''
Function:
    Implementation of Data Format Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from typing import Any, ClassVar, Dict, Optional, Tuple


'''VideoInfo'''
class VideoInfo(dict):
    source: Any
    raw_data: Dict[str, Any]
    download_url: str
    title: str
    file_path: str
    ext: str
    err_msg: str
    download_with_ffmpeg: bool
    download_with_aria2c: bool
    aria2c_settings: Dict[str, Any]
    enable_nm3u8dlre: Optional[bool]
    nm3u8dlre_settings: Dict[str, Any]
    identifier: str
    guess_video_ext_result: Dict[str, Any]
    audio_download_url: str
    guess_audio_ext_result: Dict[str, Any]
    audio_ext: str
    audio_file_path: str
    default_download_headers: Any
    default_download_cookies: Any
    cover_url: Any
    _defaults: ClassVar[Dict[str, Any]] = {
        'source': None, 'raw_data': {}, 'download_url': '', 'title': '', 'file_path': '', 'ext': 'mp4', 'err_msg': '', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 'aria2c_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 
        'identifier': '', 'guess_video_ext_result': {}, 'audio_download_url': '', 'guess_audio_ext_result': {}, 'audio_ext': 'm4a', 'audio_file_path': '', 'default_download_headers': None, 'default_download_cookies': None, 'cover_url': None,
    }
    _field_names: ClassVar[Tuple[str, ...]] = tuple(_defaults.keys())
    def __init__(self, *args, **kwargs):
        (data := dict(self._defaults)).update(dict(*args, **kwargs))
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
    '''dir'''
    def __dir__(self):
        return sorted(set(super().__dir__()) | set(self._field_names) | set(self.keys()))