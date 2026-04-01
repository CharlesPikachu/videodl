'''
Function:
    Implementation of Data Format Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from collections.abc import MutableMapping
from .youtubeutils import Stream as YouTubeStreamObj
from dataclasses import dataclass, field, fields, MISSING
from typing import Any, Dict, Optional, ClassVar, Iterator, Callable


'''VideoInfo'''
@dataclass
class VideoInfo(MutableMapping):
    # meta info
    source: Any = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    title: str = ""
    cover_url: Any = None
    err_msg: str = ""
    _extra: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    # download info
    chunk_size: int = 1024 * 1024
    download_url: str = ""
    default_download_headers: Any = None
    default_download_cookies: Any = None
    audio_download_url: str = ""
    default_audio_download_headers: Any = None
    default_audio_download_cookies: Any = None
    # ext and save path
    ext: str = "mp4"
    save_path: str = ""
    guess_video_ext_result: Dict[str, Any] = field(default_factory=dict)
    audio_ext: str = "m4a"
    audio_save_path: str = ""
    guess_audio_ext_result: Dict[str, Any] = field(default_factory=dict)
    # ffmpeg
    download_with_ffmpeg: bool = False
    ffmpeg_settings: Dict[str, Any] | Callable[..., Any] | tuple[Any, ...] = field(default_factory=dict)
    # nm3u8dlre
    enable_nm3u8dlre: Optional[bool] = None
    nm3u8dlre_settings: Dict[str, Any] | Callable[..., Any] | tuple[Any, ...] = field(default_factory=dict)
    # aria2c
    download_with_aria2c: bool = False
    aria2c_settings: Dict[str, Any] | Callable[..., Any] | tuple[Any, ...] = field(default_factory=dict)
    # unique id
    identifier: str = ""
    # filed names
    _field_names: ClassVar[tuple[str, ...]] = (
        "source", "raw_data", "title", "cover_url", "err_msg", "download_url", "default_download_headers", "default_download_cookies", "audio_download_url", "default_audio_download_headers", "default_audio_download_cookies", "ext", "save_path", 
        "guess_video_ext_result", "audio_ext", "audio_save_path", "guess_audio_ext_result", "download_with_ffmpeg", "ffmpeg_settings", "enable_nm3u8dlre", "nm3u8dlre_settings", "download_with_aria2c", "aria2c_settings", "identifier",
    )
    # with valid video download url
    @property
    def with_valid_download_url(self) -> bool:
        return bool(self.download_url) and (isinstance(self.download_url, YouTubeStreamObj) or os.path.exists(str(self.download_url)) or str(self.download_url).startswith('http'))
    # with valid audio download url
    @property
    def with_valid_audio_download_url(self) -> bool:
        return bool(self.audio_download_url) and (isinstance(self.audio_download_url, YouTubeStreamObj) or os.path.exists(str(self.audio_download_url)) or str(self.audio_download_url).startswith('http'))
    '''todict'''
    def todict(self) -> Dict[str, Any]:
        (data := {name: getattr(self, name) for name in self._field_names}).update(self._extra)
        return data
    '''fromdict'''
    @classmethod
    def fromdict(cls, data: Dict[str, Any]) -> "VideoInfo":
        known_fields = cls.knownfields()
        known = {k: v for k, v in data.items() if k in known_fields}
        extra = {k: v for k, v in data.items() if k not in known_fields}
        (obj := cls(**known))._extra.update(extra)
        return obj
    '''defaultvaluefor'''
    def defaultvaluefor(self, key: str) -> Any:
        f = next((f for f in fields(self) if f.name == key), None)
        return (f.default if f and f.default is not MISSING else f.default_factory() if f and f.default_factory is not MISSING else (_ for _ in ()).throw(KeyError(key)))
    '''knownfields'''
    @classmethod
    def knownfields(cls) -> set[str]: return set(cls._field_names)
    '''keys'''
    def keys(self): return list(iter(self))
    '''values'''
    def values(self): return [self[k] for k in self]
    '''items'''
    def items(self): return [(k, self[k]) for k in self]
    '''get'''
    def get(self, key: str, default: Any = None) -> Any: return self[key] if key in self else default
    '''clearextra'''
    def clearextra(self) -> None: self._extra.clear()
    '''update'''
    def update(self, other: dict = None, **kwargs) -> None:
        other = other or {}
        for k, v in (other.items() if hasattr(other, "items") else other): self[k] = v
        for k, v in kwargs.items(): self[k] = v
    '''pop'''
    def pop(self, key: str, default: Any = MISSING) -> Any:
        if key in self: value = self[key]; del self[key]; return value
        if default is not MISSING: return default
        raise KeyError(key)
    '''getattr'''
    def __getattr__(self, item: str) -> Any:
        extra = self.__dict__.get("_extra", None)
        if extra is not None and item in extra: return extra[item]
        raise AttributeError(f'"VideoInfo" object has no attribute "{item}"')
    '''setattr'''
    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_") or key in type(self).knownfields(): object.__setattr__(self, key, value)
        else: (object.__setattr__(self, "_extra", {}) if "_extra" not in self.__dict__ else None); self._extra[key] = value
    '''delattr'''
    def __delattr__(self, item: str) -> None:
        if item.startswith("_"): object.__delattr__(self, item)
        elif item in type(self).knownfields(): object.__setattr__(self, item, self.defaultvaluefor(item))
        else: self._extra.pop(item) if item in self._extra else (_ for _ in ()).throw(AttributeError(f'"VideoInfo" object has no attribute "{item}"'))
    '''getitem'''
    def __getitem__(self, key: str) -> Any:
        if key in type(self).knownfields(): return getattr(self, key)
        if key in self._extra: return self._extra[key]
        raise KeyError(key)
    '''setitem'''
    def __setitem__(self, key: str, value: Any) -> None:
        if key in type(self).knownfields(): setattr(self, key, value)
        else: self._extra[key] = value
    '''delitem'''
    def __delitem__(self, key: str) -> None:
        if key in type(self).knownfields(): setattr(self, key, self.defaultvaluefor(key))
        elif key in self._extra: del self._extra[key]
        else: raise KeyError(key)
    '''iter'''
    def __iter__(self) -> Iterator[str]:
        yield from self._field_names
        yield from self._extra
    '''len'''
    def __len__(self) -> int:
        return len(self._field_names) + len(self._extra)
    '''contains'''
    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str): return False
        return key in type(self).knownfields() or key in self._extra
    '''dir'''
    def __dir__(self):
        return sorted(set(super().__dir__()) | set(self._field_names) | set(self._extra.keys()))