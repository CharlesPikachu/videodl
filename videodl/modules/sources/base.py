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
import time
import pickle
import shutil
import requests
import subprocess
from pathlib import Path
from freeproxy import freeproxy
from urllib.parse import urlparse
from fake_useragent import UserAgent
from pathvalidate import sanitize_filepath
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils import touchdir, useparseheaderscookies, usedownloadheaderscookies, usesearchheaderscookies, LoggerHandle, VideoInfo
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, TimeElapsedColumn


'''BaseVideoClient'''
class BaseVideoClient():
    source = 'BaseVideoClient'
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, max_retries: int = 5, maintain_session: bool = False, 
                 logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'videodl_outputs', proxy_sources: list = None,
                 default_search_cookies: dict = None, default_download_cookies: dict = None, default_parse_cookies: dict = None):
        # set up work dir
        touchdir(work_dir)
        # set attributes
        self.work_dir = work_dir
        self.max_retries = max_retries
        self.disable_print = disable_print
        self.logger_handle = logger_handle if logger_handle else LoggerHandle()
        self.random_update_ua = random_update_ua
        self.maintain_session = maintain_session
        self.auto_set_proxies = auto_set_proxies
        self.default_search_cookies = default_search_cookies or {}
        self.default_download_cookies = default_download_cookies or {}
        self.default_parse_cookies = default_parse_cookies or {}
        self.default_cookies = self.default_parse_cookies
        # init requests.Session
        self.default_search_headers = {'User-Agent': UserAgent().random}
        self.default_parse_headers = {'User-Agent': UserAgent().random}
        self.default_download_headers = {'User-Agent': UserAgent().random}
        self.default_headers = self.default_parse_headers
        self._initsession()
        # proxied_session_client
        self.proxied_session_client = freeproxy.ProxiedSessionClient(
            proxy_sources=['KuaidailiProxiedSession', 'IP3366ProxiedSession', 'QiyunipProxiedSession', 'ProxyhubProxiedSession', 'ProxydbProxiedSession'] if proxy_sources is None else proxy_sources, 
            disable_print=True
        ) if auto_set_proxies else None
    '''_initsession'''
    def _initsession(self):
        self.session = requests.Session()
        self.session.headers = self.default_headers
    '''_ensureuniquefilepath'''
    def _ensureuniquefilepath(self, file_path):
        same_name_file_idx = 1
        while os.path.exists(file_path):
            directory, file_name = os.path.split(file_path)
            file_name_without_ext, ext = os.path.splitext(file_name)
            file_path = os.path.join(directory, f"{file_name_without_ext}_{same_name_file_idx}{ext}")
            same_name_file_idx += 1
        return file_path
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
            video_task_id, downloaded_bytes = progress.add_task(desc_name, total=total_bytes), 0
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
        default_headers = request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        headers = []
        for k, v in default_headers.items():
            headers.append(f"{k}: {v}")
        header_str = r"\r\n".join(headers) + r"\r\n"
        header_str = header_str.replace("\\", "\\\\").replace("'", "\\'")
        header_str = f"headers={header_str}"
        # append headers to text file
        download_urls = []
        with open(video_info["download_url"], 'r', encoding='utf-8') as fp:
            for line in fp.readlines():
                line = line.strip()
                if not line: continue
                download_url = f"{line}|{header_str}"
                download_url = download_url.replace("\\", "\\\\").replace("'", "\\'")
                download_urls.append(download_url)
        video_info["download_url"] = video_info["download_url"][:-4] + '_ffmpeg.txt'
        with open(video_info["download_url"], 'w', encoding='utf-8') as fp:
            for download_url in download_urls:
                fp.write(f"file '{download_url}'\n")
        # start to download
        cmd = ["ffmpeg", "-y", "-protocol_whitelist", 'file,http,https,tcp,tls']
        for _, proxy_url in request_overrides.get('proxies', {}).items():
            cmd.extend(["-http_proxy", proxy_url])
            break
        cmd.extend(["-f", "concat", "-safe", "0", "-i", video_info["download_url"], "-c", "copy", video_info["file_path"]])
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''_downloadwithffmpegcctv'''
    @usedownloadheaderscookies
    def _downloadwithffmpegcctv(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        work_dir = os.path.dirname(video_info['file_path'])
        video_info = copy.deepcopy(video_info)
        video_info['ext'] = 'mp4'
        video_info['file_path'] = os.path.join(work_dir, f'{video_info["title"]}.{video_info["ext"]}')
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        # download m3u8 files with N_m3u8DL-CLI
        cli = shutil.which("N_m3u8DL-CLI.exe")
        pid = video_info['pid']
        video_info['download_url'] = f'https://dhls2.cntv.qcloudcdn.com/asp/enc2/hls/main/0303000a/3/default/{pid}/main.m3u8' # match to cbox's version
        tmp_dir = Path(os.path.join(work_dir, str(pid))).expanduser().resolve()
        default_headers = request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        headers = []
        for k, v in default_headers.items():
            headers.append(f"{k}:{v}")
        headers_str = "|".join(headers)
        cmd = [cli, video_info["download_url"], "--headers", headers_str, "--workDir", str(tmp_dir.parent), "--saveName", pid, "--noMerge"]
        for _, proxy_url in request_overrides.get('proxies', {}).items():
            cmd.extend(["-proxyAddress", proxy_url])
            break
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode not in [0]:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return downloaded_video_infos
        # decrypt
        def _naturalkey(p: Path):
            s = p.stem
            return [int(t) if t.isdigit() else t for t in re.findall(r"\d+|\D+", s)]
        cbox = shutil.which("cbox.exe")
        tmp_part_dir = tmp_dir / "Part_0"
        ts_files = sorted([p for p in tmp_part_dir.glob("*.ts") if not p.name.endswith("_output.ts")], key=_naturalkey)
        output_ts_files: list[Path] = []
        for _, ts_file in enumerate(ts_files, 1):
            out_ts_file = ts_file.with_name(ts_file.stem + "_output.ts")
            cmd = [cbox, str(ts_file), str(out_ts_file)]
            ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
            if ret.returncode == 0 and out_ts_file.exists():
                output_ts_files.append(out_ts_file)
            else:
                err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
                self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
                shutil.rmtree(tmp_dir, ignore_errors=True)
                return downloaded_video_infos
        # merge with ffmpeg
        ffmpeg = shutil.which("ffmpeg")
        output_ts_files_txt_path = tmp_dir / f'{pid}_{int(time.time())}.txt'
        with open(output_ts_files_txt_path, "w", encoding="utf-8") as fp:
            for p in output_ts_files: fp.write(f"file '{p.as_posix()}'\n")
        cmd = [ffmpeg, "-hide_banner", "-f", "concat", "-safe", "0", "-i", str(output_ts_files_txt_path), "-c", "copy", "-movflags", "+faststart", Path(video_info['file_path']).resolve()]
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0 and Path(video_info['file_path']).resolve().exists():
            downloaded_video_infos.append(video_info)
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # del useless files auto
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if os.path.exists('output.txt') and not open('output.txt', 'r').read().strip():
            os.remove('output.txt')
            os.remove('UDRM_LICENSE.v1.0')
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
        default_headers = request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = request_overrides.get('cookies', {}) or self.default_cookies or {}
        if default_cookies: default_headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in default_cookies.items()])
        headers = []
        for k, v in default_headers.items():
            headers.append(f"{k}: {v}\r\n")
        headers_str = "".join(headers)
        # start to download
        cmd = ["ffmpeg", "-y", "-headers", headers_str]
        for _, proxy_url in request_overrides.get('proxies', {}).items():
            cmd.extend(["-http_proxy", proxy_url])
            break
        cmd.extend(["-i", video_info["download_url"], "-c", "copy", "-bsf:a", "aac_adtstoasc"])
        cmd.append(video_info['file_path'])
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
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
        default_headers = request_overrides.get('headers', {}) or copy.deepcopy(self.default_headers)
        default_cookies = request_overrides.get('cookies', {}) or self.default_cookies or {}
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
        for k, v in default_headers.items():
            cmd.extend(["--header", f"{k}: {v}"])
        proxies = request_overrides.get("proxies", {}) or {}
        for _, proxy_url in proxies.items():
            cmd.extend(["--all-proxy", proxy_url])
            break
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
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        # init
        request_overrides = request_overrides or {}
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # YouTubeVideoClient use specific downloader (highest-priority)
        if video_info.get('source') in ['YouTubeVideoClient']: return self._downloadyoutube(
            video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
        )
        # CCTVVideoClient use specific downloader for high-quality video files (highest-priority)
        if video_info.get('source') in ['CCTVVideoClient'] and video_info.get('download_with_ffmpeg_cctv', False): return self._downloadwithffmpegcctv(
            video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress
        )
        # use ffmpeg to deal with m3u8 likes, auto set according to video_info cues, a naive judgement is applied (high-priority)
        if video_info.get('ext') in ['m3u8', 'm3u'] or video_info['download_url'].split('?')[0].endswith('.m3u8') or video_info['download_url'].split('?')[0].endswith('m3u'):
            video_info.update(dict(ext='mp4', download_with_ffmpeg=True, file_path=os.path.join(self.work_dir, self.source, f'{video_info.title}.mp4')))
        if video_info.get('download_with_ffmpeg', False): return self._downloadwithffmpeg(
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
        # start to download
        try:
            resp = self.get(video_info['download_url'], stream=True, **request_overrides)
            resp.raise_for_status()
            content_length = int(float(resp.headers.get("Content-Length", 0) or 0))
            chunk_size = video_info.get('chunk_size', 1024 * 1024)
            if len(os.path.basename(video_info['file_path'])) > 10:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10] + '...'}"
            else:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10]}"
            total_bytes = content_length if content_length > 0 else None
            video_task_id, downloaded_bytes = progress.add_task(desc_name, total=total_bytes), 0
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
        # logging
        self.logger_handle.info(f'Start to download videos using {self.source}.', disable_print=self.disable_print)
        # multi threadings for downloading videos
        downloaded_video_infos = []
        with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), DownloadColumn(), TransferSpeedColumn(), TimeElapsedColumn(), TimeRemainingColumn()) as progress:
            overall_task_id = progress.add_task("[bold cyan]Overall videos", total=len(video_infos))
            with ThreadPoolExecutor(max_workers=num_threadings) as executor:
                futures = [executor.submit(self._download, video_info, vid, downloaded_video_infos, request_overrides, progress) for vid, video_info in enumerate(video_infos)]
                for feat in as_completed(futures):
                    progress.update(overall_task_id, advance=1)
        # logging
        self.logger_handle.info(f'Finished downloading videos using {self.source}. Valid downloads: {len(downloaded_video_infos)}.', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        # set valid domains
        if valid_domains is None:
            valid_domains = []
        # extract domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # judge and return according to domain
        if not domain: return False
        return domain in valid_domains
    '''get'''
    def get(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
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
            try:
                resp = self.session.get(url, **kwargs)
            except Exception as err:
                self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err})', disable_print=self.disable_print)
                continue
            if resp.status_code != 200: continue
            return resp
        return resp
    '''post'''
    def post(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
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
            try:
                resp = self.session.post(url, **kwargs)
            except Exception as err:
                self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err})', disable_print=self.disable_print)
                continue
            if resp.status_code != 200: continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp)