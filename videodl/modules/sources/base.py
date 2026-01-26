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
from rich.progress import Task
from fake_useragent import UserAgent
from platformdirs import user_log_dir
from pathvalidate import sanitize_filepath
from ..utils.domains import obtainhostname, hostmatchessuffix
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, TimeElapsedColumn, ProgressColumn
from ..utils import touchdir, useparseheaderscookies, usedownloadheaderscookies, usesearchheaderscookies, cookies2dict, generateuniquetmppath, shortenpathsinvideoinfos, optionalimport, LoggerHandle, VideoInfo


'''VideoAwareColumn'''
class VideoAwareColumn(ProgressColumn):
    def __init__(self):
        super(VideoAwareColumn, self).__init__()
        self._download_col = DownloadColumn()
    '''render'''
    def render(self, task: Task):
        kind = task.fields.get("kind", "download")
        if kind == "overall":
            completed = int(task.completed)
            total = int(task.total) if task.total is not None else 0
            return Text(f"{completed}/{total} videos")
        elif kind == 'm3u8download':
            completed = int(task.completed)
            total = int(task.total) if task.total is not None else 0
            return Text(f"{completed}/{total} ts")
        else:
            return self._download_col.render(task)


'''BaseVideoClient'''
class BaseVideoClient():
    source = 'BaseVideoClient'
    LESHI_BASE64_ENCODE_PATTERN = re.compile(r'data:[^;]+;base64,([A-Za-z0-9+/=]+)')
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, enable_parse_curl_cffi: bool = False, enable_search_curl_cffi: bool = False, enable_download_curl_cffi: bool = False,
                 max_retries: int = 5, maintain_session: bool = False, logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'videodl_outputs', freeproxy_settings: dict = None, 
                 default_search_cookies: dict = None, default_download_cookies: dict = None, default_parse_cookies: dict = None):
        # set up work dir
        touchdir(work_dir)
        # set attributes
        self.work_dir = work_dir
        self.max_retries = max_retries
        self.disable_print = disable_print
        self.logger_handle = logger_handle if logger_handle else LoggerHandle()
        self.random_update_ua = random_update_ua
        self.enable_parse_curl_cffi = enable_parse_curl_cffi
        self.enable_search_curl_cffi = enable_search_curl_cffi
        self.enable_download_curl_cffi = enable_download_curl_cffi
        self.enable_curl_cffi = self.enable_parse_curl_cffi
        self.cc_impersonates = self._listccimpersonates() if (enable_parse_curl_cffi or enable_search_curl_cffi or enable_download_curl_cffi) else None
        self.maintain_session = maintain_session
        self.auto_set_proxies = auto_set_proxies
        self.freeproxy_settings = freeproxy_settings or {}
        self.default_search_cookies = cookies2dict(default_search_cookies)
        self.default_download_cookies = cookies2dict(default_download_cookies)
        self.default_parse_cookies = cookies2dict(default_parse_cookies)
        self.default_cookies = self.default_parse_cookies
        # init requests.Session
        self.default_search_headers = {'User-Agent': UserAgent().random}
        self.default_parse_headers = {'User-Agent': UserAgent().random}
        self.default_download_headers = {'User-Agent': UserAgent().random}
        self.default_headers = self.default_parse_headers
        self._initsession()
        # proxied_session_client
        self.proxied_session_client = None
        if auto_set_proxies:
            from freeproxy import freeproxy
            default_freeproxy_settings = dict(disable_print=True, proxy_sources=['ProxiflyProxiedSession'], max_tries=20, init_proxied_session_cfg={})
            default_freeproxy_settings.update(self.freeproxy_settings)
            self.proxied_session_client = freeproxy.ProxiedSessionClient(**default_freeproxy_settings)
    '''_listccimpersonates'''
    def _listccimpersonates(self):
        curl_cffi = optionalimport('curl_cffi')
        root = Path(curl_cffi.__file__).resolve().parent
        exts = {".py", ".so", ".pyd", ".dll", ".dylib"}
        pat = re.compile(rb"\b(?:chrome|edge|safari|firefox|tor)(?:\d+[a-z_]*|_android|_ios)?\b")
        return sorted({m.decode("utf-8", "ignore") for p in root.rglob("*") if p.suffix in exts for m in pat.findall(p.read_bytes())})
    '''_initsession'''
    def _initsession(self):
        curl_cffi = optionalimport('curl_cffi')
        self.session = requests.Session() if not self.enable_curl_cffi else curl_cffi.requests.Session()
        self.session.headers = self.default_headers
    '''_ensureuniquefilepath'''
    def _ensureuniquefilepath(self, file_path: str):
        same_name_file_idx, unique_file_path = 1, file_path
        while os.path.exists(unique_file_path):
            directory, file_name = os.path.split(file_path)
            file_name_without_ext, ext = os.path.splitext(file_name)
            unique_file_path = os.path.join(directory, f"{file_name_without_ext} ({same_name_file_idx}){ext}")
            same_name_file_idx += 1
        return unique_file_path
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        raise NotImplementedError('not be implemented')
    '''_search'''
    @usesearchheaderscookies
    def _search(self):
        raise NotImplementedError()
    '''search'''
    @usesearchheaderscookies
    def search(self):
        raise NotImplementedError()
    '''_convertspecialdownloadurl'''
    def _convertspecialdownloadurl(self, download_url: str, tmp_file_name: str = None):
        # init
        is_converter_performed = False
        # leshi base64 encoded url
        leshi_m = self.LESHI_BASE64_ENCODE_PATTERN.match(download_url)
        if leshi_m:
            download_url, is_converter_performed = base64.b64decode(leshi_m.group(1)).decode("utf-8", errors="ignore"), True
            if not download_url.startswith('#EXTM3U'): return download_url, is_converter_performed
            touchdir(os.path.join(self.work_dir, self.source))
            tmp_file_path = os.path.join(self.work_dir, self.source, f'{tmp_file_name}.m3u8') if tmp_file_name else generateuniquetmppath(os.path.join(self.work_dir, self.source), ext='m3u8')
            with open(tmp_file_path, 'w') as fp: fp.write(download_url)
            return tmp_file_path, is_converter_performed
        # no matched known specifical urls
        return download_url, is_converter_performed
    '''_downloadyoutube'''
    @usedownloadheaderscookies
    def _downloadyoutube(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        # start to download
        try:
            content_length = int(float(video_info['download_url'].filesize or 0))
            chunk_size = video_info.get('chunk_size', 1024 * 1024)
            if len(os.path.basename(video_info['file_path'])) > 10:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10] + '...'}"
            else:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10]}"
            total_bytes = content_length if content_length > 0 else None
            video_task_id, downloaded_bytes = progress.add_task(desc_name, total=total_bytes, kind="download"), 0
            with open(video_info['file_path'], "wb") as fp:
                for chunk in video_info['download_url'].iterchunks(chunk_size=chunk_size):
                    if not chunk: continue
                    fp.write(chunk)
                    downloaded_bytes += len(chunk)
                    if total_bytes is None: progress.update(video_task_id, total=downloaded_bytes)
                    progress.update(video_task_id, advance=len(chunk))
            downloaded_video_infos.append(video_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}._download >>> {video_info["identifier"]} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadcctv'''
    @usedownloadheaderscookies
    def _downloadcctv(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        ts_work_dir = os.path.join(os.path.dirname(video_info['file_path']), video_info['identifier'])
        touchdir(ts_work_dir)
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        node_script = Path(__file__).resolve().parents[2] / "modules" / "js" / "cctv" / "decrypt.js"
        # start to download
        loaded_m3u8_url, processed_files_fp = m3u8.load(video_info['download_url']), open(os.path.join(ts_work_dir, f'{video_info.identifier}.txt'), 'w')
        if len(os.path.basename(video_info['file_path'])) > 10:
            desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10] + '...'}"
        else:
            desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10]}"
        video_task_id = progress.add_task(desc_name, total=len(loaded_m3u8_url.segments), kind="m3u8download")
        for seg_idx, segment in enumerate(loaded_m3u8_url.segments):
            cmd = ["node", node_script, segment.absolute_uri, os.path.join(ts_work_dir, f"segment_{seg_idx:08d}.mp4")]
            ret = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if ret.returncode != 0:
                err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}'
                self.logger_handle.error(f'{self.source}._download >>> {segment.absolute_uri} (Error{err_msg})', disable_print=self.disable_print)
            progress.update(video_task_id, advance=1)
            processed_files_fp.write(f"file 'segment_{seg_idx:08d}.mp4'\n")
        processed_files_fp.close()
        merge_cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", processed_files_fp, "-c", "copy", "-movflags", "+faststart", video_info["file_path"]]
        capture_output = True if self.disable_print else False
        ret = subprocess.run(merge_cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            shutil.rmtree(ts_work_dir, ignore_errors=True)
            downloaded_video_infos.append(video_info)
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithffmpegfromlocalfile'''
    @usedownloadheaderscookies
    def _downloadwithffmpegfromlocalfile(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        default_headers = video_info.get('default_download_headers') or request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = video_info.get('default_download_cookies') or request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        headers = []
        for k, v in default_headers.items(): headers.append(f"{k}: {v}")
        header_str = r"\r\n".join(headers) + r"\r\n"
        header_str = header_str.replace("\\", "\\\\").replace("'", "\\'")
        header_str = f"headers={header_str}"
        # append headers to text file
        download_urls = []
        with open(video_info["download_url"], "r", encoding="utf-8") as fp: download_urls.extend([f"{s}|{header_str}".replace("\\", "\\\\").replace("'", "\\'") for line in fp if (s := line.strip())])
        video_info["download_url"] = video_info["download_url"][:-4] + '_ffmpeg.txt'
        with open(video_info["download_url"], 'w', encoding='utf-8') as fp:
            for download_url in download_urls: fp.write(f"file '{download_url}'\n")
        # start to download
        cmd = ["ffmpeg", "-y", "-protocol_whitelist", 'file,http,https,tcp,tls']
        for _, proxy_url in request_overrides.get('proxies', {}).items(): cmd.extend(["-http_proxy", proxy_url]); break
        cmd.extend(["-f", "concat", "-safe", "0", "-i", video_info["download_url"], "-c", "copy", video_info["file_path"]])
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
            if os.path.exists(video_info["download_url"]): os.remove(video_info["download_url"])
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithffmpeg'''
    @usedownloadheaderscookies
    def _downloadwithffmpeg(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        default_headers = video_info.get('default_download_headers') or request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = video_info.get('default_download_cookies') or request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        headers = []
        for k, v in default_headers.items(): headers.append(f"{k}: {v}")
        headers_str = "\r\n".join(headers)
        # start to download
        cmd = ["ffmpeg", "-y", "-protocol_whitelist", 'file,http,https,tcp,tls']
        for _, proxy_url in request_overrides.get("proxies", {}).items(): cmd.extend(["-http_proxy", proxy_url]); break
        # --with audio
        if video_info.get('audio_download_url') and video_info['audio_download_url'] != 'NULL':
            if headers_str: cmd.extend(["-headers", headers_str])
            cmd.extend(["-i", video_info["download_url"]])
            if headers_str: cmd.extend(["-headers", headers_str])
            cmd.extend(["-i", video_info['audio_download_url']])
            cmd.extend(["-c:v", "copy", "-c:a", "copy", "-map", "0:v:0", "-map", "1:a:0", "-shortest", "-bsf:a", "aac_adtstoasc"])
        # --without audio
        else:
            if headers_str: cmd.extend(["-headers", headers_str])
            cmd.extend(["-i", video_info["download_url"], "-c", "copy", "-bsf:a", "aac_adtstoasc"])
        cmd.append(video_info['file_path'])
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
            if os.path.exists(video_info["download_url"]): os.remove(video_info["download_url"])
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithnm3u8dlre'''
    @usedownloadheaderscookies
    def _downloadwithnm3u8dlre(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        default_headers = video_info.get('default_download_headers') or request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = video_info.get('default_download_cookies') or request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        header_args: list[str] = []
        for k, v in default_headers.items(): header_args.extend(["-H", f"{k}: {v}"])
        proxy_url = None
        for _, p in request_overrides.get("proxies", {}).items(): proxy_url = p; break
        # start to download
        default_nm3u8dlre_settings = {'thread_count': '8', 'download_retry_count': '3', 'check_segments_count': False if video_info['source'] in ['XMFlvVideoClient'] else True, 'key': None, 'extra_options': None}
        nm3u8dlre_settings = video_info.get('nm3u8dlre_settings', {}) or {}
        default_nm3u8dlre_settings.update(nm3u8dlre_settings)
        log_dir = user_log_dir(appname='videodl', appauthor='zcjin')
        log_file_path = generateuniquetmppath(dir=log_dir, ext='log')
        cmd = [
            'N_m3u8DL-RE', video_info["download_url"], "--auto-select", "--save-dir", os.path.dirname(video_info["file_path"]), "--save-name", os.path.basename(video_info["file_path"]),
            "--thread-count", default_nm3u8dlre_settings['thread_count'], "--download-retry-count", default_nm3u8dlre_settings['download_retry_count'], 
        ]
        if default_nm3u8dlre_settings['key']: cmd.extend(["--key", default_nm3u8dlre_settings['key']])
        if default_nm3u8dlre_settings['check_segments_count']: cmd.extend(["--check-segments-count", "--del-after-done", "-M", f"format={video_info['ext']}", '--log-file-path', log_file_path])
        else: cmd.extend(["--check-segments-count", "false", "--del-after-done", "-M", f"format={video_info['ext']}", '--log-file-path', log_file_path])
        cmd.extend(header_args)
        if proxy_url: cmd.extend(["--custom-proxy", proxy_url])
        if default_nm3u8dlre_settings['extra_options'] and isinstance(default_nm3u8dlre_settings['extra_options'], (list, tuple)): cmd.extend(list(default_nm3u8dlre_settings['extra_options']))
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
            if os.path.exists(video_info["download_url"]): os.remove(video_info["download_url"])
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwitharia2c'''
    @usedownloadheaderscookies
    def _downloadwitharia2c(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        default_headers = video_info.get('default_download_headers') or request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = video_info.get('default_download_cookies') or request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        default_aria2c_settings = {
            'max_connection_per_server': 16, 'split': 16, 'piece_size': '1M', 'max_tries': 5, 'file_allocation': 'none', 'max_concurrent_downloads': 1, 'extra_options': []
        }
        aria2c_settings = video_info.get('aria2c_settings', {}) or {}
        default_aria2c_settings.update(aria2c_settings)
        # construct cmd
        cmd = [
            "aria2c", "-c", "-x", str(default_aria2c_settings['max_connection_per_server']), "-s", str(default_aria2c_settings['split']),
            "-k", str(default_aria2c_settings['piece_size']), f"--file-allocation={default_aria2c_settings['file_allocation']}",
            f"--max-tries={default_aria2c_settings['max_tries']}", f"--max-concurrent-downloads={default_aria2c_settings['max_concurrent_downloads']}",
            "-o", os.path.basename(video_info["file_path"]), "-d", os.path.dirname(video_info["file_path"]),
        ]
        for k, v in default_headers.items(): cmd.extend(["--header", f"{k}: {v}"])
        proxies = request_overrides.get("proxies", {}) or {}
        for _, proxy_url in proxies.items(): cmd.extend(["--all-proxy", proxy_url]); break
        extra_aria2c_opts = default_aria2c_settings.get('extra_options', []) or []
        if isinstance(extra_aria2c_opts, (list, tuple)): cmd.extend(list(extra_aria2c_opts))
        cmd.append(video_info["download_url"])
        # conduct
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_naivedownloadvideoaudiothenmerge'''
    @usedownloadheaderscookies
    def _naivedownloadvideoaudiothenmerge(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        video_info = copy.deepcopy(video_info)
        # avoid calling ffmpeg to download audios
        audio_download_url = video_info.pop('audio_download_url')
        audio_file_path = video_info.pop('audio_file_path')
        audio_ext = video_info.pop('audio_ext')
        guess_audio_ext_result = video_info.pop('guess_audio_ext_result')
        # download videos
        self._download(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # download audios
        audio_info = VideoInfo(
            source=self.source, download_url=audio_download_url, file_path=audio_file_path, ext=audio_ext, identifier=f'audio-{video_info["identifier"]}', guess_video_ext_result=guess_audio_ext_result,
            default_download_headers=video_info.get('default_download_headers'), default_download_cookies=video_info.get('default_download_cookies')
        )
        downloaded_audio_infos = self._download(video_info=audio_info, video_info_index=video_info_index, downloaded_video_infos=[], request_overrides=request_overrides, progress=progress)
        assert len(downloaded_audio_infos) == 1
        # merge videos and audios
        audio_file_path = downloaded_audio_infos[0]['file_path']
        audio_ext = downloaded_audio_infos[0]['ext']
        tgt_dvi = [dvi for dvi in downloaded_video_infos if dvi['identifier'] == video_info["identifier"]]
        video_file_path = tgt_dvi[0]['file_path']
        tmp_merged_file_path = generateuniquetmppath(dir=os.path.join(self.work_dir, self.source), ext=tgt_dvi[0]["ext"])
        cmd = ['ffmpeg', '-y', '-i', video_file_path, '-i', audio_file_path, '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', tmp_merged_file_path]
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            shutil.move(tmp_merged_file_path, video_file_path)
            if os.path.exists(audio_file_path): os.remove(audio_file_path)
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # recover audio information 
        for dvi in downloaded_video_infos:
            if dvi['identifier'] != video_info["identifier"]: continue
            dvi['audio_download_url'] = audio_download_url
            dvi['audio_file_path'] = audio_file_path
            dvi['audio_ext'] = audio_ext
            dvi['guess_audio_ext_result'] = guess_audio_ext_result
        # return
        return downloaded_video_infos
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # some formats maybe incorrect, auto correct
        if video_info.get('ext') in ['m4s']: video_info.update(dict(ext='mp4', file_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.mp4')))
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # YouTubeVideoClient use specific downloader (highest-priority)
        if video_info.get('source') in ['YouTubeVideoClient']: return self._downloadyoutube(
            video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
        )
        # CCTVVideoClient use specific downloader (highest-priority)
        if video_info.get('source') in ['CCTVVideoClient'] and video_info.get('hls_key') in ['hls_h5e_url']: return self._downloadcctv(
            video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
        )
        # requires merging videos and audios like some third-part video clients and bilibili (highest-priority)
        if video_info.get('audio_download_url') and video_info.get('audio_download_url') != 'NULL' and video_info.get('audio_ext') in ['m4a', 'mp3', 'aac', 'weba', 'webm']: return self._naivedownloadvideoaudiothenmerge(
            video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
        )
        # use ffmpeg to deal with m3u8 likes, auto set according to video_info cues, a naive judgement is applied (high-priority)
        if any((video_info.get('ext', '').lower() in {'m3u8', 'm3u', 'mpd'}, video_info.get('download_url', '').split('?', 1)[0].lower().endswith(('.m3u8', '.m3u', '.mpd')))):
            ext = video_info.get('ext') if video_info.get('ext') in ('mkv',) else 'mp4'
            video_info.update(dict(ext=ext, download_with_ffmpeg=True, file_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.{ext}')))
        if video_info.get('download_with_ffmpeg') and not ({video_info.get('ext', ''), video_info.get('download_url', '').split('?', 1)[0].rsplit('.', 1)[-1]} & {'txt'}):
            if shutil.which('N_m3u8DL-RE') and video_info.source not in ['TedVideoClient', 'XinpianchangVideoClient']: video_info['enable_nm3u8dlre'] = True
            elif video_info['enable_nm3u8dlre'] and (not shutil.which('N_m3u8DL-RE')):
                warning_msg = ('"enable_nm3u8dlre" has been set to True, but N_m3u8DL-RE was not found in the environment variables.' 
                               'Please visit https://github.com/nilaoda/N_m3u8DL-RE to download and install the version of N_m3u8DL-RE that matches your system,'
                               'and then add it to your environment variables. Now, we will switch "enable_nm3u8dlre" to False and try downloading again.')
                video_info['enable_nm3u8dlre'] = False
                self.logger_handle.warning(f'{self.source}._download >>> {video_info["download_url"]} (Warning: {warning_msg})', disable_print=self.disable_print)
            if video_info.get('enable_nm3u8dlre', False):
                return self._downloadwithnm3u8dlre(
                    video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
                )
            else:
                return self._downloadwithffmpeg(
                    video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
                )
        # use ffmpeg to deal with .txt files which contain video links (high-priority)
        if (video_info.get('ext') in ['txt'] or video_info.get('download_url').endswith('.txt')) and video_info.get('download_with_ffmpeg', False): 
            video_info.update(dict(ext='mp4', download_with_ffmpeg=True, file_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.mp4')))
            return self._downloadwithffmpegfromlocalfile(
                video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
            )
        # use aria2c to speed up downloading video files, requires manually set in video_info (medium-priority)
        if video_info.get('download_with_aria2c', False): return self._downloadwitharia2c(
            video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides
        )
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        if video_info.get('default_download_headers'): request_overrides['headers'] = video_info.get('default_download_headers')
        if video_info.get('default_download_cookies'): request_overrides['cookies'] = video_info.get('default_download_cookies')
        # start to download
        try:
            try: resp = self.get(video_info['download_url'], stream=True, **request_overrides)
            except: resp = self.get(video_info['download_url'], stream=True, verify=False, **request_overrides)
            resp.raise_for_status()
            content_length = int(float(resp.headers.get("Content-Length", 0) or 0))
            chunk_size = video_info.get('chunk_size', 1024 * 1024)
            if len(os.path.basename(video_info['file_path'])) > 10:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10] + '...'}"
            else:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10]}"
            total_bytes = content_length if content_length > 0 else None
            video_task_id, downloaded_bytes = progress.add_task(desc_name, total=total_bytes, kind="download"), 0
            with open(video_info['file_path'], "wb") as fp:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if not chunk: continue
                    fp.write(chunk)
                    downloaded_bytes += len(chunk)
                    if total_bytes is None: progress.update(video_task_id, total=downloaded_bytes)
                    progress.update(video_task_id, advance=len(chunk))
            downloaded_video_infos.append(video_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''download'''
    @usedownloadheaderscookies
    def download(self, video_infos: list, num_threadings: int = 5, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        # filter
        video_infos = [video_info for video_info in video_infos if video_info['download_url'] and video_info['download_url'] != 'NULL']
        if not video_infos: return []
        video_infos = shortenpathsinvideoinfos(video_infos, key='file_path')
        video_infos = shortenpathsinvideoinfos(video_infos, key='audio_file_path')
        # logging
        self.logger_handle.info(f'Start to download videos using {self.source}.', disable_print=self.disable_print)
        # multi threadings for downloading videos
        downloaded_video_infos = []
        with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), VideoAwareColumn(), TransferSpeedColumn(), TimeElapsedColumn(), TimeRemainingColumn()) as progress:
            overall_task_id = progress.add_task("[bold cyan]Overall videos", total=len(video_infos), kind="overall")
            with ThreadPoolExecutor(max_workers=num_threadings) as executor:
                futures = [executor.submit(self._download, video_info, vid, downloaded_video_infos, request_overrides, progress) for vid, video_info in enumerate(video_infos)]
                for _ in as_completed(futures):
                    progress.update(overall_task_id, advance=1)
        # logging
        self.logger_handle.info(f'Finished downloading videos using {self.source}. Valid downloads: {len(downloaded_video_infos)}.', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        # set valid domains
        if valid_domains is None: valid_domains = []
        # extract url domain
        domain = obtainhostname(url)
        # judge and return according to valid domains
        if not domain or not valid_domains: return False
        return hostmatchessuffix(domain, valid_domains)
    '''get'''
    def get(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except Exception as err:
                    self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err})', disable_print=self.disable_print)
                    self.session.proxies = {}
            else:
                self.session.proxies = {}
            proxies = kwargs.pop('proxies', None) or self.session.proxies
            try:
                resp = self.session.get(url, proxies=proxies, **kwargs)
                resp.raise_for_status()
            except Exception as err:
                self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err})', disable_print=self.disable_print)
                continue
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
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except Exception as err:
                    self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err})', disable_print=self.disable_print)
                    self.session.proxies = {}
            else:
                self.session.proxies = {}
            proxies = kwargs.pop('proxies', None) or self.session.proxies
            try:
                resp = self.session.post(url, proxies=proxies, **kwargs)
                resp.raise_for_status()
            except Exception as err:
                self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err})', disable_print=self.disable_print)
                continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp: pickle.dump(data, fp)