'''
Function:
    Implementation of CMD Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import os
from .data import VideoInfo
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional, Sequence, Union


'''CmdArg'''
@dataclass
class CmdArg:
    key: Optional[str] = None
    value: Optional[str] = None


'''CmdOp'''
@dataclass
class CmdOp:
    op: str
    key: Optional[str] = None
    value: Any = None
    occurrence: int = 0
    remove_all: bool = True
    '''set'''
    @classmethod
    def set(cls, key: str, value: Any, occurrence: int = 0) -> "CmdOp": return cls(op="set", key=key, value=value, occurrence=occurrence)
    '''add'''
    @classmethod
    def add(cls, key: str, value: Any = None) -> "CmdOp": return cls(op="add", key=key, value=value)
    '''remove'''
    @classmethod
    def remove(cls, key: str, remove_all: bool = True) -> "CmdOp": return cls(op="remove", key=key, remove_all=remove_all)
    '''beforeoutput'''
    @classmethod
    def beforeoutput(cls, key: str, value: Any = None) -> "CmdOp": return cls(op="before_output", key=key, value=value)


'''ModType'''
ModType = Union[Callable[["CommandBuilder"], None], Mapping[str, Any], Sequence[Union[CmdOp, tuple, Mapping[str, Any]]]]


'''CommandBuilder'''
class CommandBuilder:
    def __init__(self, executable: str):
        self.executable = executable
        self.args: list[CmdArg] = []
    '''flag'''
    def flag(self, key: str) -> "CommandBuilder":
        self.args.append(CmdArg(key=key, value=None))
        return self
    '''opt'''
    def opt(self, key: str, value: Any) -> "CommandBuilder":
        self.args.append(CmdArg(key=key, value=str(value)))
        return self
    '''positional'''
    def positional(self, value: Any) -> "CommandBuilder":
        self.args.append(CmdArg(key=None, value=str(value)))
        return self
    '''add'''
    def add(self, key: str, value: Any = None) -> "CommandBuilder":
        if value is None: return self.flag(key)
        return self.opt(key, value)
    '''set'''
    def set(self, key: str, value: Any, occurrence: int = 0, append_if_missing: bool = True) -> "CommandBuilder":
        if (match := next((arg for i, arg in enumerate(a for a in self.args if a.key == key) if i == occurrence), None)) is not None:
            match.value = None if value is None else str(value)
            return self
        if append_if_missing: return self.insertbeforeoutput(key, value)
        return self
    '''remove'''
    def remove(self, key: str, remove_all: bool = True) -> "CommandBuilder":
        if remove_all: self.args = [arg for arg in self.args if arg.key != key]; return self
        idx = next((i for i, arg in enumerate(self.args) if arg.key == key), None)
        self.args = self.args if idx is None else self.args[:idx] + self.args[idx+1:]
        return self
    '''insertbeforeoutput'''
    def insertbeforeoutput(self, key: str, value: Any = None) -> "CommandBuilder":
        idx = next((i for i in range(len(self.args) - 1, -1, -1) if self.args[i].key is None), len(self.args))
        self.args.insert(idx, CmdArg(key=key, value=None if value is None else str(value)))
        return self
    '''insertpositionalbeforeoutput'''
    def insertpositionalbeforeoutput(self, value: Any) -> "CommandBuilder":
        idx = next((i for i in range(len(self.args) - 1, -1, -1) if self.args[i].key is None), len(self.args))
        self.args.insert(idx, CmdArg(key=None, value=str(value)))
        return self
    '''tolist'''
    def tolist(self) -> list[str]:
        cmd = [self.executable] + [x for arg in self.args for x in ((arg.value,) if arg.key is None else (arg.key,) if arg.value is None else (arg.key, arg.value))]
        return cmd
    '''repr'''
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tolist()!r})"


'''CommandModsApplier'''
class CommandModsApplier:
    RESERVED_KEYS = {"__add__", "__remove__", "__before_output__"}
    '''apply'''
    @classmethod
    def apply(cls, builder: CommandBuilder, mods: Optional[ModType]) -> CommandBuilder:
        if mods is None or not mods: return builder
        if callable(mods): mods(builder); return builder
        if isinstance(mods, Mapping): cls.applydictmods(builder, mods); return builder
        if isinstance(mods, Sequence) and not isinstance(mods, (str, bytes)): list(map(lambda item: cls.applyoneop(builder, item), mods)); return builder
        raise TypeError(f"Unsupported mods type: {type(mods)!r}")
    '''applydictmods'''
    @classmethod
    def applydictmods(cls, builder: CommandBuilder, mods: Mapping[str, Any]) -> None:
        # 1) non-special keys
        for key, value in mods.items():
            if key in cls.RESERVED_KEYS: continue
            if value is False: builder.remove(key)
            elif value is True: builder.insertbeforeoutput(key) if not any(arg.key == key for arg in builder.args) else None
            else: builder.set(key, value)
        # 2) __remove__
        for item in mods.get("__remove__", []):
            if isinstance(item, str): builder.remove(item)
            elif isinstance(item, (tuple, list)): builder.remove(item[0]) if len(item) == 1 else builder.remove(item[0], remove_all=bool(item[1]))
            elif isinstance(item, Mapping): builder.remove(item["key"], remove_all=item.get("remove_all", True))
            else: raise TypeError(f"Unsupported __remove__ item: {item!r}")
        # 3) __add__
        for item in mods.get("__add__", []): cls.applyaddlike(builder, item, before_output=False)
        # 4) __before_output__
        for item in mods.get("__before_output__", []): cls.applyaddlike(builder, item, before_output=True)
    '''applyaddlike'''
    @classmethod
    def applyaddlike(cls, builder: CommandBuilder, item: Any, before_output: bool) -> None:
        if isinstance(item, (tuple, list)): key, value = (item[0], None) if len(item) == 1 else (item[0], item[1]) if len(item) == 2 else (_ for _ in ()).throw(ValueError(f"Tuple/list mod must have length 1 or 2: {item!r}"))
        elif isinstance(item, Mapping): key, value = item["key"], item.get("value")
        else: raise TypeError(f"Unsupported add-like item: {item!r}")
        if before_output: builder.insertbeforeoutput(key, value)
        else: builder.add(key, value)
    '''applyoneop'''
    @classmethod
    def applyoneop(cls, builder: CommandBuilder, op_item: Union[CmdOp, tuple, Mapping[str, Any]]) -> None:
        if isinstance(op_item, CmdOp): op, key, value, occurrence, remove_all = op_item.op, op_item.key, op_item.value, op_item.occurrence, op_item.remove_all
        elif isinstance(op_item, Mapping): op, key, value, occurrence, remove_all = op_item["op"], op_item.get("key"), op_item.get("value"), op_item.get("occurrence", 0), op_item.get("remove_all", True)
        elif isinstance(op_item, tuple): op, key, value, occurrence, remove_all = op_item[0], op_item[1], op_item[2] if len(op_item) >= 3 else None, op_item[3] if len(op_item) >= 4 else 0, op_item[4] if len(op_item) >= 5 else True
        else: raise TypeError(f"Unsupported op item: {op_item!r}")
        if op == "set": builder.set(key, value, occurrence=occurrence)
        elif op == "add": builder.add(key, value)
        elif op == "remove": builder.remove(key, remove_all=remove_all)
        elif op == "before_output": builder.insertbeforeoutput(key, value)
        else: raise ValueError(f"Unknown operation: {op}")


'''FFmpegCommandFactory'''
class FFmpegCommandFactory:
    def __init__(self, executable: str = "ffmpeg"):
        self.executable = executable
    '''newbuilder'''
    def newbuilder(self) -> CommandBuilder:
        return CommandBuilder(self.executable)
    '''applymods'''
    def applymods(self, builder: CommandBuilder, mods: Optional[ModType]) -> CommandBuilder:
        return CommandModsApplier.apply(builder, mods)


'''MergeCCTVTsFilesFFmpegCommand'''
class MergeCCTVTsFilesFFmpegCommand(FFmpegCommandFactory):
    '''build'''
    def build(self, video_info: VideoInfo, ts_work_dir: str, mods: Optional[ModType] = None) -> list[str]:
        txt_file, output_file = os.path.join(ts_work_dir, f"{video_info.identifier}.txt"), video_info.save_path
        builder = (
            self.newbuilder().flag("-y").opt("-fflags", "+genpts").opt("-f", "concat").opt("-safe", "0").opt("-i", txt_file).opt("-avoid_negative_ts", "make_zero").opt("-map", "0:v:0").opt("-map", "0:a?")
            .opt("-c:v", "libx264").opt("-preset", "veryfast").opt("-crf", "16").opt("-pix_fmt", "yuv420p").opt("-c:a", "copy").opt("-movflags", "+faststart").opt("-vsync", "0").positional(output_file)
        )
        self.applymods(builder, mods)
        return builder.tolist()


'''MergeVideoAudioFFmpegCommand'''
class MergeVideoAudioFFmpegCommand(FFmpegCommandFactory):
    '''build'''
    def build(self, video_file_path: str, audio_file_path: str, output_file_path: str, mods: Optional[ModType] = None) -> list[str]:
        builder = (self.newbuilder().flag("-y").opt("-i", str(video_file_path)).opt("-i", str(audio_file_path)).opt("-c", "copy").opt("-map", "0:v:0").opt("-map", "1:a:0").positional(output_file_path))
        self.applymods(builder, mods)
        return builder.tolist()


'''DownloadFromLocalTxtFileFFmpegCommand'''
class DownloadFromLocalTxtFileFFmpegCommand(FFmpegCommandFactory):
    '''build'''
    def build(self, video_info: VideoInfo, request_overrides: Optional[Mapping[str, Any]] = None, mods: Optional[ModType] = None) -> list[str]:
        request_overrides, download_url, output_file = request_overrides or {}, video_info.download_url, video_info.save_path
        builder = (self.newbuilder().flag("-y").opt("-protocol_whitelist", "file,http,https,tcp,tls"))
        proxies = request_overrides.get("proxies", {}) if isinstance(request_overrides, Mapping) else {}
        if (proxy_url := next(iter((proxies or {}).values()), None)): builder.opt("-http_proxy", proxy_url)
        builder = (builder.opt("-f", "concat").opt("-safe", "0").opt("-i", download_url).opt("-c", "copy").positional(output_file))
        self.applymods(builder, mods)
        return builder.tolist()


'''DownloadWithFFmpegCommand'''
class DownloadWithFFmpegCommand(FFmpegCommandFactory):
    '''build'''
    def build(self, video_info: VideoInfo, header_opt: str, audio_header_opt: str, request_overrides: Optional[Mapping[str, Any]] = None, mods: Optional[ModType] = None) -> list[str]:
        request_overrides, download_url, audio_download_url, output_file = request_overrides or {}, video_info.download_url, video_info.audio_download_url, video_info.save_path
        builder = (self.newbuilder().flag("-y").opt("-protocol_whitelist", "file,http,https,tcp,tls"))
        proxies = request_overrides.get("proxies", {}) if isinstance(request_overrides, Mapping) else {}
        if (proxy_url := next(iter((proxies or {}).values()), None)): builder.opt("-http_proxy", proxy_url)
        if video_info.with_valid_audio_download_url:
            header_opt and builder.opt("-headers", header_opt); builder.opt("-i", download_url)
            audio_header_opt and builder.opt("-headers", audio_header_opt); builder.opt("-i", audio_download_url)
            builder = (builder.opt("-c:v", "copy").opt("-c:a", "copy").opt("-map", "0:v:0").opt("-map", "1:a:0").flag("-shortest").opt("-bsf:a", "aac_adtstoasc").positional(output_file))
        else:
            header_opt and builder.opt("-headers", header_opt); builder.opt("-i", download_url)
            builder = (builder.opt("-c", "copy").opt("-bsf:a", "aac_adtstoasc").positional(output_file))
        self.applymods(builder, mods)
        return builder.tolist()


'''NM3U8DLRECommandFactory'''
class NM3U8DLRECommandFactory:
    def __init__(self, executable: str = "N_m3u8DL-RE"):
        self.executable = executable
    '''newbuilder'''
    def newbuilder(self) -> CommandBuilder:
        return CommandBuilder(self.executable)
    '''applymods'''
    def applymods(self, builder: CommandBuilder, mods: Optional[ModType]) -> CommandBuilder:
        return CommandModsApplier.apply(builder, mods)


'''DownloadWithNM3U8DLRECommand'''
class DownloadWithNM3U8DLRECommand(NM3U8DLRECommandFactory):
    DISABLE_CHECK_SEGMENTS_COUNT_SOURCES = {"XMFlvVideoClient", "IM1907VideoClient"}
    '''build'''
    def build(self, video_info: VideoInfo, default_headers: Optional[Mapping[str, Any]] = None, request_overrides: Optional[Mapping[str, Any]] = None, mods: Optional[ModType] = None, log_file_path: Optional[str] = None) -> list[str]:
        request_overrides, default_headers, download_url, output_file = request_overrides or {}, default_headers or {}, video_info.download_url, video_info.save_path
        save_dir, save_name, ext = os.path.dirname(output_file) or ".", os.path.splitext(os.path.basename(output_file))[0], video_info.ext
        builder = (self.newbuilder().positional(download_url).flag("--auto-select").opt("--save-dir", save_dir).opt("--save-name", save_name).opt("--thread-count", '8').opt("--download-retry-count", '3'))
        builder.opt("--check-segments-count", "false") if video_info.source in DownloadWithNM3U8DLRECommand.DISABLE_CHECK_SEGMENTS_COUNT_SOURCES else builder.flag("--check-segments-count")
        builder.flag("--del-after-done").opt("-M", f"format={ext}").opt("--log-file-path", log_file_path)
        for k, v in default_headers.items(): builder.opt("-H", f"{k}: {v}")
        proxies = request_overrides.get("proxies", {}) if isinstance(request_overrides, Mapping) else {}
        if (proxy_url := next(iter((proxies or {}).values()), None)): builder.opt("--custom-proxy", proxy_url)
        self.applymods(builder, mods)
        return builder.tolist()
    '''addkeyafterretry'''
    @staticmethod
    def addkeyafterretry(key_value: str):
        if not key_value or not isinstance(key_value, str): return {}
        def insert_decrypt_key_func(builder: CommandBuilder):
            builder.remove("--key")
            if (i := next((i for i, arg in enumerate(builder.args) if arg.key == "--download-retry-count"), None)) is not None: builder.args.insert(i + 1, CmdArg(key="--key", value=str(key_value))); return
            builder.add("--key", key_value)
        return insert_decrypt_key_func


'''Aria2cCommandFactory'''
class Aria2cCommandFactory:
    def __init__(self, executable: str = "aria2c"):
        self.executable = executable
    '''newbuilder'''
    def newbuilder(self) -> CommandBuilder:
        return CommandBuilder(self.executable)
    '''applymods'''
    def applymods(self, builder: CommandBuilder, mods: Optional[ModType]) -> CommandBuilder:
        return CommandModsApplier.apply(builder, mods)


'''DownloadWithAria2cCommand'''
class DownloadWithAria2cCommand(Aria2cCommandFactory):
    '''build'''
    def build(self, video_info: VideoInfo, default_headers: Optional[Mapping[str, Any]] = None, request_overrides: Optional[Mapping[str, Any]] = None, mods: Optional[ModType] = None) -> list[str]:
        request_overrides, default_headers, download_url, output_file = request_overrides or {}, default_headers or {}, video_info.download_url, video_info.save_path
        save_dir, save_name = os.path.dirname(output_file) or ".", os.path.basename(output_file)
        builder = (self.newbuilder().flag("-c").opt("-x", "8").opt("-s", "8").opt("-k", '1M').opt("--file-allocation", "none").opt("--max-tries", "5").opt("--max-concurrent-downloads", "1").opt("-o", save_name).opt("-d", save_dir))
        for k, v in default_headers.items(): builder.opt("--header", f"{k}: {v}")
        proxies = request_overrides.get("proxies", {}) if isinstance(request_overrides, Mapping) else {}
        if (proxy_url := next(iter((proxies or {}).values()), None)): builder.opt("--all-proxy", proxy_url)
        builder.positional(download_url); self.applymods(builder, mods)
        return builder.tolist()