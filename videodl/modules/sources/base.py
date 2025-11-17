'''
Function:
    Implementation of BaseVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import math
import pickle
import requests
import subprocess
from tqdm import tqdm
from freeproxy import freeproxy
from urllib.parse import urlparse
from fake_useragent import UserAgent
from alive_progress import alive_bar
from pathvalidate import sanitize_filepath
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils import touchdir, LoggerHandle, useparseheaderscookies, usedownloadheaderscookies, usesearchheaderscookies
tqdm.__del__ = lambda self: None # some versions have bugs for tqdm.__del__


'''BaseVideoClient'''
class BaseVideoClient():
    source = 'BaseVideoClient'
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, max_retries: int = 5, maintain_session: bool = False, 
                 logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'videodl_outputs', proxy_sources: list = None):
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
        # init requests.Session
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
    def parsefromurl(self, url: str, request_overrides: dict = {}):
        raise NotImplementedError('not be implemented')
    '''_search'''
    @usesearchheaderscookies
    def _search(self):
        raise NotImplementedError()
    '''search'''
    @usesearchheaderscookies
    def search(self):
        raise NotImplementedError()
    '''_downloadwithffmpeg'''
    @usedownloadheaderscookies
    def _downloadwithffmpeg(self, video_info: dict, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = {}):
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        video_info = copy.deepcopy(video_info)
        video_info['file_path'] = self._ensureuniquefilepath(video_info['file_path'])
        headers = []
        for k, v in self.default_headers.items():
            headers.append(f"{k}: {v}\r\n")
        headers_str = "".join(headers)
        # start to download
        cmd = ["ffmpeg", "-y", "-headers", headers_str, "-i", video_info["download_url"], "-c", "copy", "-bsf:a", "aac_adtstoasc"]
        for _, proxy_url in request_overrides.get('proxies', {}).items():
            cmd.extend(["-http_proxy", proxy_url])
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
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, video_info, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = {}):
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # use ffmpeg to deal with m3u8 like files
        if video_info.get('download_with_ffmpeg', False): return self._downloadwithffmpeg(
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
            chunk_size = 1024 * 1024
            total_chunks = max(1, math.ceil(content_length / chunk_size))
            video_total_mb = content_length / (1024 * 1024)
            if len(os.path.basename(video_info['file_path'])) > 10:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10] + '...'}"
            else:
                desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:10]}"
            with alive_bar(total_chunks, title=desc_name, bar='blocks', stats='[{rate}, {eta}]') as bar:
                downloaded_bytes = 0
                with open(video_info['file_path'], "wb") as fp:
                    for chunk in resp.iter_content(chunk_size=chunk_size):
                        if not chunk: continue
                        fp.write(chunk)
                        downloaded_bytes += len(chunk)
                        bar()
                        bar.text = f"{downloaded_bytes/1024/1024:.1f}/{video_total_mb:.1f} MB"
            downloaded_video_infos.append(video_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''download'''
    @usedownloadheaderscookies
    def download(self, video_infos: list, num_threadings: int = 5, request_overrides: dict = {}):
        video_infos = [video_info for video_info in video_infos if video_info['download_url'] and video_info['download_url'] != 'NULL']
        if not video_infos: return []
        # logging
        self.logger_handle.info(f'Start to download videos using {self.source}.', disable_print=self.disable_print)
        # multi threadings for downloading videos
        downloaded_video_infos = []
        with tqdm(
            total=len(video_infos), desc="Overall videos", position=0, dynamic_ncols=True, unit="video", 
            bar_format="{l_bar}{bar}| {n}/{total} {unit}s",
        ) as overall_pbar:
            with ThreadPoolExecutor(max_workers=num_threadings) as executor:
                futures = [executor.submit(self._download, video_info, vid, downloaded_video_infos, request_overrides) for vid, video_info in enumerate(video_infos)]
                for feat in as_completed(futures):
                    overall_pbar.update(1)
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