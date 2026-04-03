'''
Function:
    Implementation of BaseVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import m3u8
import random
import base64
import pickle
import shutil
import requests
import subprocess
from pathlib import Path
from rich.text import Text
from typing import TYPE_CHECKING
from fake_useragent import UserAgent
from platformdirs import user_log_dir
from ..utils.youtubeutils import Stream as YouTubeStreamObj
from pathvalidate import sanitize_filepath, sanitize_filename
from ..utils.domains import obtainhostname, hostmatchessuffix
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, TimeElapsedColumn, ProgressColumn, Task
from ..utils import touchdir, useparseheaderscookies, usedownloadheaderscookies, usesearchheaderscookies, cookies2dict, generateuniquetmppath, shortenpathsinvideoinfos, optionalimport, optionalimportfrom, cookies2string, LoggerHandle, VideoInfo, FileTypeSniffer
from ..utils.cmd import MergeCCTVTsFilesFFmpegCommand, DownloadFromLocalTxtFileFFmpegCommand, DownloadWithFFmpegCommand, DownloadWithNM3U8DLRECommand, DownloadWithAria2cCommand, MergeVideoAudioAudioTranscodeFFmpegCommand, MergeVideoAudioCopyFFmpegCommand, MergeVideoAudioFullTranscodeFFmpegCommand


'''VideoAwareColumn'''
class VideoAwareColumn(ProgressColumn):
    def __init__(self):
        super(VideoAwareColumn, self).__init__()
        self._download_col = DownloadColumn()
    '''render'''
    def render(self, task: Task):
        kind = task.fields.get("kind", "download")
        if kind == "overall": total = int(task.total) if task.total is not None else 0; return Text(f"{int(task.completed)}/{total} videos")
        elif kind == 'm3u8download': total = int(task.total) if task.total is not None else 0; return Text(f"{int(task.completed)}/{total} ts")
        else: return self._download_col.render(task)


'''BaseVideoClient'''
class BaseVideoClient():
    source = 'BaseVideoClient'
    LESHI_BASE64_ENCODE_PATTERN = re.compile(r'data:[^;]+;base64,([A-Za-z0-9+/=]+)')
    BILIBILI_REFERENCE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}
    WEIBO_REFERENCE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Referer': 'https://weibo.com/'}
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, enable_parse_curl_cffi: bool = False, enable_search_curl_cffi: bool = False, enable_download_curl_cffi: bool = False,
                 max_retries: int = 5, maintain_session: bool = False, logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'videodl_outputs', freeproxy_settings: dict = None, 
                 default_search_cookies: dict = None, default_download_cookies: dict = None, default_parse_cookies: dict = None):
        # set up work dir
        touchdir(work_dir)
        # io attributes
        self.work_dir = work_dir
        # logging attributes
        self.disable_print = disable_print
        self.logger_handle = logger_handle if logger_handle else LoggerHandle()
        # http requests attributes
        self.max_retries = max_retries
        self.maintain_session = maintain_session
        # --proxies
        self.auto_set_proxies = auto_set_proxies
        self.freeproxy_settings = freeproxy_settings or {}
        freeproxy = optionalimportfrom('freeproxy', 'freeproxy')
        if TYPE_CHECKING: from freeproxy import freeproxy as freeproxy
        (default_freeproxy_settings := dict(disable_print=True, proxy_sources=['ProxiflyProxiedSession'], max_tries=20, init_proxied_session_cfg={})).update(self.freeproxy_settings)
        self.proxied_session_client = freeproxy.ProxiedSessionClient(**default_freeproxy_settings) if auto_set_proxies else None
        # --headers
        self.random_update_ua = random_update_ua
        self.default_search_headers = {'User-Agent': UserAgent().random}
        self.default_parse_headers = {'User-Agent': UserAgent().random}
        self.default_download_headers = {'User-Agent': UserAgent().random}
        self.default_headers = self.default_parse_headers
        # --cookies
        self.default_search_cookies = cookies2dict(default_search_cookies)
        self.default_download_cookies = cookies2dict(default_download_cookies)
        self.default_parse_cookies = cookies2dict(default_parse_cookies)
        self.default_cookies = self.default_parse_cookies
        # --curl-cffi
        self.enable_parse_curl_cffi = enable_parse_curl_cffi
        self.enable_search_curl_cffi = enable_search_curl_cffi
        self.enable_download_curl_cffi = enable_download_curl_cffi
        self.enable_curl_cffi = self.enable_parse_curl_cffi
        self.cc_impersonates = self._listccimpersonates() if (enable_parse_curl_cffi or enable_search_curl_cffi or enable_download_curl_cffi) else None
        # --init
        self._initsession()
    '''_listccimpersonates'''
    def _listccimpersonates(self):
        curl_cffi = optionalimport('curl_cffi')
        if TYPE_CHECKING: import curl_cffi as curl_cffi
        root, exts = Path(curl_cffi.__file__).resolve().parent, {".py", ".so", ".pyd", ".dll", ".dylib"}
        pat = re.compile(rb"\b(?:chrome|edge|safari|firefox|tor)(?:\d+[a-z_]*|_android|_ios)?\b")
        return sorted({m.decode("utf-8", "ignore") for p in root.rglob("*") if p.suffix in exts for m in pat.findall(p.read_bytes())})
    '''_initsession'''
    def _initsession(self):
        curl_cffi = optionalimport('curl_cffi')
        if TYPE_CHECKING: import curl_cffi as curl_cffi
        self.session = requests.Session() if not self.enable_curl_cffi else curl_cffi.requests.Session()
        self.session.headers = self.default_headers
    '''_ensureuniquefilepath'''
    def _ensureuniquefilepath(self, file_path: str):
        same_name_file_idx, unique_file_path = 1, sanitize_filepath(file_path)
        while os.path.exists(unique_file_path):
            directory, file_name = os.path.split(file_path); file_name_without_ext, ext = os.path.splitext(file_name)
            unique_file_path = os.path.join(directory, f"{file_name_without_ext} ({same_name_file_idx}){ext}"); same_name_file_idx += 1
        return unique_file_path
    '''_search'''
    @usesearchheaderscookies
    def _search(self):
        raise NotImplementedError()
    '''search'''
    @usesearchheaderscookies
    def search(self):
        raise NotImplementedError()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        raise NotImplementedError('not be implemented')
    '''_convertspecialdownloadurl'''
    def _convertspecialdownloadurl(self, download_url: str, tmp_file_name: str = None):
        # init
        is_converter_performed = False; touchdir(os.path.join(self.work_dir, self.source))
        # leshi base64 encoded url
        leshi_m = BaseVideoClient.LESHI_BASE64_ENCODE_PATTERN.match(download_url)
        if leshi_m and (not is_converter_performed):
            download_url, is_converter_performed = base64.b64decode(leshi_m.group(1)).decode("utf-8", errors="ignore"), True
            if not download_url.startswith('#EXTM3U'): return download_url, is_converter_performed
            tmp_file_path = os.path.join(self.work_dir, self.source, f'{tmp_file_name}.m3u8') if tmp_file_name else generateuniquetmppath(os.path.join(self.work_dir, self.source), ext='m3u8')
            with open(tmp_file_path, 'w') as fp: fp.write(download_url)
            return tmp_file_path, is_converter_performed
        # no matched known specifical urls
        return download_url, is_converter_performed
    '''_downloadfromyoutube'''
    @usedownloadheaderscookies
    def _downloadfromyoutube(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        assert isinstance(video_info.download_url, YouTubeStreamObj)
        # start to download
        try:
            content_length, chunk_size = int(float(video_info.download_url.filesize or 0)), video_info.chunk_size
            desc_name = f"[{video_info_index+1}] {os.path.basename(video_info.save_path)[:15] + '...'}" if len(os.path.basename(video_info.save_path)) > 15 else f"[{video_info_index+1}] {os.path.basename(video_info.save_path)[:15]}"
            total_bytes, downloaded_bytes = content_length if content_length > 0 else None, 0
            video_task_id = progress.add_task(desc_name, total=total_bytes, kind="download")
            with open(video_info.save_path, "wb") as fp:
                for chunk in video_info.download_url.iterchunks(chunk_size=chunk_size):
                    if chunk: fp.write(chunk); downloaded_bytes += len(chunk); total_bytes is None and progress.update(video_task_id, total=downloaded_bytes); progress.update(video_task_id, advance=len(chunk))
            downloaded_video_infos.append(video_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}._downloadfromyoutube >>> {video_info.identifier} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadfromcctv'''
    @usedownloadheaderscookies
    def _downloadfromcctv(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if not request_overrides.get('proxies'): request_overrides['proxies'] = self._autosetproxies()
        ts_work_dir = sanitize_filepath(os.path.join(os.path.dirname(video_info.save_path), str(video_info.identifier)))
        shutil.rmtree(ts_work_dir, ignore_errors=True); touchdir(ts_work_dir); video_info.identifier = sanitize_filename(str(video_info.identifier))
        node_script = Path(__file__).resolve().parents[2] / "modules" / "js" / "cctv" / "decrypt.js"
        # start to download
        loaded_m3u8_url, processed_files_fp = m3u8.load(video_info.download_url), open(os.path.join(ts_work_dir, f'{video_info.identifier}.txt'), 'w')
        desc_name = f"[{video_info_index+1}] {os.path.basename(video_info.save_path)[:15] + '...'}" if len(os.path.basename(video_info.save_path)) > 15 else f"[{video_info_index+1}] {os.path.basename(video_info.save_path)[:15]}"
        video_task_id = progress.add_task(desc_name, total=len(loaded_m3u8_url.segments), kind="m3u8download")
        for seg_idx, segment in enumerate(loaded_m3u8_url.segments):
            cmd = ["node", node_script, segment.absolute_uri, os.path.join(ts_work_dir, f"segment_{seg_idx:08d}.mp4")]
            try: subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore'); progress.update(video_task_id, advance=1); processed_files_fp.write(f"file 'segment_{seg_idx:08d}.mp4'\n")
            except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadfromcctv >>> {segment.absolute_uri} (Error: {err})', disable_print=self.disable_print); progress.update(video_task_id, advance=1)
        processed_files_fp.close(); merge_ts_files_cmd = MergeCCTVTsFilesFFmpegCommand().build(video_info=video_info, ts_work_dir=ts_work_dir, mods=video_info.ffmpeg_settings)
        try: subprocess.run(merge_ts_files_cmd, check=True, capture_output=(True if self.disable_print else False), text=True, encoding='utf-8', errors='ignore'); shutil.rmtree(ts_work_dir, ignore_errors=True); downloaded_video_infos.append(video_info)
        except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadfromcctv >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadfromlocaltxtfilewithffmpeg'''
    @usedownloadheaderscookies
    def _downloadfromlocaltxtfilewithffmpeg(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if not request_overrides.get('proxies'): request_overrides['proxies'] = self._autosetproxies()
        default_headers = copy.deepcopy(video_info.default_download_headers or request_overrides.get('headers') or self.default_headers or {})
        default_cookies = copy.deepcopy(video_info.default_download_cookies or request_overrides.get('cookies') or self.default_cookies or {})
        if default_cookies: default_headers['Cookie'] = cookies2string(default_cookies)
        # some pre-defined functions
        ffconcat_quote_func = lambda value: "'" + ("" if value is None else str(value)).replace("'", r"'\''") + "'"
        build_ffmpeg_headers_option_func = lambda default_headers: ("" if not default_headers else (lambda clean: "headers=" + r"\r\n".join(f"{clean(k)}: {clean(v)}" for k, v in default_headers.items()) + r"\r\n")(lambda x: str(x).replace("\r", "").replace("\n", "").strip()))
        # prepare txt file for ffmpeg to process
        header_opt = build_ffmpeg_headers_option_func(default_headers)
        with open(video_info.download_url, "r", encoding="utf-8") as fp: raw_urls = [line.strip() for line in fp if line.strip()]
        download_urls = [f"{url}|{header_opt}" if header_opt else url for url in raw_urls]
        original_file_path = video_info.download_url; video_info.download_url = video_info.download_url[:-4] + "_ffmpeg.txt"
        with open(video_info.download_url, "w", encoding="utf-8", newline="\n") as fp: fp.write("ffconcat version 1.0\n" + "".join(f"file {ffconcat_quote_func(download_url)}\n" for download_url in download_urls))
        # start to download
        cmd = DownloadFromLocalTxtFileFFmpegCommand().build(video_info=video_info, request_overrides=request_overrides, mods=video_info.ffmpeg_settings)
        try: subprocess.run(cmd, check=True, capture_output=(True if self.disable_print else False), text=True, encoding='utf-8', errors='ignore'); downloaded_video_infos.append(video_info); os.path.exists(video_info.download_url) and os.remove(video_info.download_url); os.path.exists(original_file_path) and os.remove(original_file_path)
        except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadfromlocaltxtfilewithffmpeg >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithffmpeg'''
    @usedownloadheaderscookies
    def _downloadwithffmpeg(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if not request_overrides.get('proxies'): request_overrides['proxies'] = self._autosetproxies()
        default_headers = copy.deepcopy(video_info.default_download_headers or request_overrides.get('headers') or self.default_headers or {})
        default_cookies = copy.deepcopy(video_info.default_download_cookies or request_overrides.get('cookies') or self.default_cookies or {})
        if default_cookies: default_headers['Cookie'] = cookies2string(default_cookies)
        audio_default_headers = copy.deepcopy(video_info.default_audio_download_headers or request_overrides.get('headers') or self.default_headers or {})
        audio_default_cookies = copy.deepcopy(video_info.default_audio_download_cookies or request_overrides.get('cookies') or self.default_cookies or {})
        if audio_default_cookies: audio_default_headers['Cookie'] = cookies2string(audio_default_cookies)
        # some pre-defined functions
        build_ffmpeg_headers_option_func = lambda headers: ("" if not headers else "\r\n".join(f"{k}: {v}" for k, v in headers.items() if k is not None and v is not None))
        # start to download
        header_opt, audio_header_opt = build_ffmpeg_headers_option_func(default_headers), build_ffmpeg_headers_option_func(audio_default_headers)
        cmd = DownloadWithFFmpegCommand().build(video_info=video_info, header_opt=header_opt, audio_header_opt=audio_header_opt, request_overrides=request_overrides, mods=video_info.ffmpeg_settings)
        try: subprocess.run(cmd, check=True, capture_output=(True if self.disable_print else False), text=True, encoding='utf-8', errors='ignore'); downloaded_video_infos.append(video_info)
        except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadwithffmpeg >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithnm3u8dlre'''
    @usedownloadheaderscookies
    def _downloadwithnm3u8dlre(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if not request_overrides.get('proxies'): request_overrides['proxies'] = self._autosetproxies()
        default_headers = copy.deepcopy(video_info.default_download_headers or request_overrides.get('headers') or self.default_headers or {})
        default_cookies = copy.deepcopy(video_info.default_download_cookies or request_overrides.get('cookies') or self.default_cookies or {})
        if default_cookies: default_headers['Cookie'] = cookies2string(default_cookies)
        # start to download
        log_file_path = generateuniquetmppath(dir=user_log_dir(appname='videodl', appauthor='zcjin'), ext='log')
        cmd = DownloadWithNM3U8DLRECommand().build(video_info=video_info, default_headers=default_headers, request_overrides=request_overrides, mods=video_info.nm3u8dlre_settings, log_file_path=log_file_path)
        try: subprocess.run(cmd, check=True, capture_output=(True if self.disable_print else False), text=True, encoding='utf-8', errors='ignore'); downloaded_video_infos.append(video_info); os.path.exists(video_info.download_url) and os.remove(video_info.download_url)
        except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadwithnm3u8dlre >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwitharia2c'''
    @usedownloadheaderscookies
    def _downloadwitharia2c(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if not request_overrides.get('proxies'): request_overrides['proxies'] = self._autosetproxies()
        default_headers = copy.deepcopy(video_info.default_download_headers or request_overrides.get('headers') or self.default_headers or {})
        default_cookies = copy.deepcopy(video_info.default_download_cookies or request_overrides.get('cookies') or self.default_cookies or {})
        if default_cookies: default_headers['Cookie'] = cookies2string(default_cookies)
        # start to download
        cmd = DownloadWithAria2cCommand().build(video_info=video_info, default_headers=default_headers, request_overrides=request_overrides, mods=video_info.aria2c_settings)
        try: subprocess.run(cmd, check=True, capture_output=(True if self.disable_print else False), text=True, encoding='utf-8', errors='ignore'); downloaded_video_infos.append(video_info); os.path.exists(video_info.download_url) and os.remove(video_info.download_url)
        except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadwitharia2c >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithnaiveallinone'''
    @usedownloadheaderscookies
    def _downloadwithnaiveallinone(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        if video_info.audio_save_path: video_info.audio_save_path = self._ensureuniquefilepath(video_info.audio_save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if video_info.audio_save_path: touchdir(os.path.dirname(video_info.audio_save_path))
        # download video
        audio_download_url = video_info.pop('audio_download_url'); audio_save_path = video_info.pop('audio_save_path'); audio_ext = video_info.pop('audio_ext'); guess_audio_ext_result = video_info.pop('guess_audio_ext_result')
        downloaded_video_infos: list[VideoInfo] = self._download(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        downloaded_video_info = [dvi for dvi in downloaded_video_infos if (dvi.identifier == video_info.identifier)]
        # download audio
        audio_info = VideoInfo(
            source=video_info.source, download_url=audio_download_url, save_path=audio_save_path, ext=audio_ext, identifier=f'audio-{video_info.identifier}', guess_video_ext_result=guess_audio_ext_result,
            default_download_headers=video_info.default_audio_download_headers, default_download_cookies=video_info.default_audio_download_cookies
        )
        downloaded_audio_infos = self._download(video_info=audio_info, video_info_index=video_info_index, downloaded_video_infos=[], request_overrides=request_overrides, progress=progress)
        # merge video and audio
        audio_save_path, audio_ext, video_save_path, ext = downloaded_audio_infos[0].save_path, downloaded_audio_infos[0].ext, downloaded_video_info[0].save_path, downloaded_video_info[0].ext
        file_path_for_merge_video_audio = generateuniquetmppath(dir=os.path.join(self.work_dir, self.source), ext=ext)
        for merge_factory in (MergeVideoAudioCopyFFmpegCommand, MergeVideoAudioAudioTranscodeFFmpegCommand, MergeVideoAudioFullTranscodeFFmpegCommand):
            cmd = merge_factory().build(video_file_path=video_save_path, audio_file_path=audio_save_path, output_file_path=file_path_for_merge_video_audio, mods=video_info.ffmpeg_settings)
            try: subprocess.run(cmd, check=True, capture_output=(True if self.disable_print else False), text=True, encoding='utf-8', errors='ignore')
            except subprocess.CalledProcessError as err: self.logger_handle.error(f'{self.source}._downloadwithnaiveallinone >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print); continue
            if MergeVideoAudioCopyFFmpegCommand.hasaudiostream(file_path_for_merge_video_audio): break
        shutil.move(file_path_for_merge_video_audio, video_save_path); os.path.exists(audio_save_path) and os.remove(audio_save_path)
        # return
        downloaded_video_info[0].audio_download_url, downloaded_video_info[0].audio_save_path = audio_download_url, audio_save_path
        downloaded_video_info[0].audio_ext, downloaded_video_info[0].guess_audio_ext_result = audio_ext, guess_audio_ext_result
        return downloaded_video_infos
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None) -> list[VideoInfo]:
        # init
        if not video_info.with_valid_download_url: return downloaded_video_infos
        if video_info.ext in {'m4s'}: video_info.update(dict(ext='mp4', save_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.mp4')))
        if video_info.audio_ext in {'m4s'}: video_info.update(dict(audio_ext='mp4', audio_save_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.audio.m4a')))
        judge_local_file_ext_func = lambda p: Path(str(p)).suffix[1:].lower() if p else ""
        # youtube video client
        if video_info.source in {'YouTubeVideoClient'} and isinstance(video_info.download_url, YouTubeStreamObj): return self._downloadfromyoutube(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # cctv video client
        if video_info.source in {'CCTVVideoClient'} and video_info.get('hls_key') in {'hls_h5e_url'}: return self._downloadfromcctv(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # all in one downloader for downlowning both video and audio
        if video_info.with_valid_audio_download_url: return self._downloadwithnaiveallinone(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # ffmpeg downloader for dealing with HLS urls / files
        valid_hls_exts_for_auto_set_ffpmeg, cannot_use_nm3u8dlre_sources = {'m3u8', 'm3u', 'mpd'}, {'XinpianchangVideoClient'}
        if any((video_info.ext.lower() in valid_hls_exts_for_auto_set_ffpmeg, FileTypeSniffer.pickextfromurl(video_info.download_url) in valid_hls_exts_for_auto_set_ffpmeg)): ext = video_info.ext if video_info.ext in {'mkv'} else 'mp4'; video_info.update(dict(ext=ext, download_with_ffmpeg=True, save_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.{ext}')))
        no_nm3u8dlre_warnings = ('"enable_nm3u8dlre" has been set to True, but N_m3u8DL-RE was not found in the environment variables.' 'Please visit https://github.com/nilaoda/N_m3u8DL-RE to download and install the version of N_m3u8DL-RE that matches your system,' 'and then add it to your environment variables. Now, we will switch "enable_nm3u8dlre" to False and try downloading again.')
        # --from url or local hls files except for .txt file
        if video_info.download_with_ffmpeg and ((not os.path.exists(video_info.download_url)) or (os.path.exists(video_info.download_url) and (judge_local_file_ext_func(video_info.download_url) not in {'txt'}))):
            video_info.enable_nm3u8dlre = True if (shutil.which('N_m3u8DL-RE') and (video_info.get('enable_nm3u8dlre') is None) and (video_info.source not in cannot_use_nm3u8dlre_sources)) else video_info.enable_nm3u8dlre
            if video_info.enable_nm3u8dlre and (not shutil.which('N_m3u8DL-RE')): video_info.enable_nm3u8dlre = False; self.logger_handle.warning(f'{self.source}._download >>> {video_info.download_url} (Warning: {no_nm3u8dlre_warnings})', disable_print=self.disable_print)
            ext = video_info.ext if video_info.ext in {'mkv'} else 'mp4'; video_info.update(dict(ext=ext, download_with_ffmpeg=True, save_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.{ext}')))
            return (self._downloadwithffmpeg(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress) if (not video_info.enable_nm3u8dlre) else self._downloadwithnm3u8dlre(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress))
        # --from local .txt file
        elif video_info.download_with_ffmpeg and os.path.exists(video_info.download_url) and (judge_local_file_ext_func(video_info.download_url) in {'txt'}):
            ext = video_info.ext if video_info.ext in {'mkv'} else 'mp4'; video_info.update(dict(ext=ext, download_with_ffmpeg=True, save_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.{ext}')))
            return self._downloadfromlocaltxtfilewithffmpeg(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # aria2c downloader for speeding up mp4 like files download
        if video_info.download_with_aria2c: return self._downloadwitharia2c(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # naive implementition of file downloader
        (video_info := copy.deepcopy(video_info)).save_path = self._ensureuniquefilepath(video_info.save_path)
        request_overrides = dict(request_overrides or {}); touchdir(os.path.dirname(video_info.save_path))
        if not request_overrides.get('proxies'): request_overrides['proxies'] = self._autosetproxies()
        request_overrides['headers'] = copy.deepcopy(video_info.default_download_headers or request_overrides.get('headers') or self.default_headers or {})
        request_overrides['cookies'] = copy.deepcopy(video_info.default_download_cookies or request_overrides.get('cookies') or self.default_cookies or {})
        try:
            try: (resp := self.get(video_info.download_url, stream=True, **request_overrides)).raise_for_status()
            except Exception: (resp := self.get(video_info.download_url, stream=True, verify=False, **request_overrides)).raise_for_status()
            content_length, chunk_size = int(float(resp.headers.get("Content-Length", 0) or 0)), video_info.chunk_size
            desc_name = f"[{video_info_index+1}] {os.path.basename(video_info.save_path)[:15] + '...'}" if len(os.path.basename(video_info.save_path)) > 15 else f"[{video_info_index+1}] {os.path.basename(video_info.save_path)[:15]}"
            total_bytes, downloaded_bytes = content_length if content_length > 0 else None, 0
            video_task_id = progress.add_task(desc_name, total=total_bytes, kind="download")
            with open(video_info.save_path, "wb") as fp:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk: fp.write(chunk); downloaded_bytes += len(chunk); total_bytes is None and progress.update(video_task_id, total=downloaded_bytes); progress.update(video_task_id, advance=len(chunk))
            downloaded_video_infos.append(video_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}._download >>> {video_info.download_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''download'''
    @usedownloadheaderscookies
    def download(self, video_infos: list[VideoInfo], num_threadings: int = 5, request_overrides: dict = None) -> list[VideoInfo]:
        # init
        if not (video_infos := [video_info for video_info in video_infos if video_info.with_valid_download_url]): return []
        request_overrides, downloaded_video_infos = dict(request_overrides or {}), []
        video_infos = shortenpathsinvideoinfos(video_infos, key='save_path'); video_infos = shortenpathsinvideoinfos(video_infos, key='audio_save_path')
        # logging
        self.logger_handle.info(f'Start to download videos using {self.source}.', disable_print=self.disable_print)
        # multi threadings for downloading videos
        with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), VideoAwareColumn(), TransferSpeedColumn(), TimeElapsedColumn(), TimeRemainingColumn()) as progress:
            overall_task_id = progress.add_task("[bold cyan]Overall videos", total=len(video_infos), kind="overall")
            with ThreadPoolExecutor(max_workers=num_threadings) as executor:
                futures = [executor.submit(self._download, video_info, vid, downloaded_video_infos, request_overrides, progress) for vid, video_info in enumerate(video_infos)]
                for fut in as_completed(futures): fut.result(); progress.update(overall_task_id, advance=1)
        # logging
        self.logger_handle.info(f'Finished downloading videos using {self.source}. Valid downloads: {len(downloaded_video_infos)}.', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        # set valid domains
        if valid_domains is None: valid_domains = {}
        # extract url domain
        domain = obtainhostname(url)
        # judge and return according to valid domains
        if not domain or not valid_domains: return False
        return hostmatchessuffix(domain, valid_domains)
    '''_autosetproxies'''
    def _autosetproxies(self):
        if not self.auto_set_proxies: return {}
        try: proxies = self.proxied_session_client.getrandomproxy()
        except Exception as err: self.logger_handle.error(f'{self.source}._autosetproxies >>> freeproxy lib failed to auto fetch proxies (Error: {err})', disable_print=self.disable_print); proxies = {}
        return proxies
    '''get'''
    def get(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            proxies = kwargs.pop('proxies', None) or self._autosetproxies()
            try: (resp := self.session.get(url, proxies=proxies, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''post'''
    def post(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            proxies = kwargs.pop('proxies', None) or self._autosetproxies()
            try: (resp := self.session.post(url, proxies=proxies, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp: pickle.dump(data, fp)