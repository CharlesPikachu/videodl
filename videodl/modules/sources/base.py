'''
Function:
    Implementation of BaseVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import pickle
import requests
import tldextract
from tqdm import tqdm
from freeproxy import freeproxy
from fake_useragent import UserAgent
from pathvalidate import sanitize_filepath
from ..utils import touchdir, byte2mb, LoggerHandle
from concurrent.futures import ThreadPoolExecutor, as_completed


'''BaseVideoClient'''
class BaseVideoClient():
    source = 'BaseVideoClient'
    def __init__(self, auto_set_proxies: bool = True, random_update_ua: bool = False, max_retries: int = 5, maintain_session: bool = False, 
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
    '''parsefromurl'''
    def parsefromurl(self, url: str, request_overrides: dict = {}):
        raise NotImplementedError('not be implemented')
    '''_search'''
    def _search(self):
        raise NotImplementedError()
    '''search'''
    def search(self):
        raise NotImplementedError()
    '''_download'''
    def _download(self, video_info, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = {}):
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        pbar = None
        # start to download
        try:
            resp = self.get(video_info['download_url'], stream=True, **request_overrides)
            resp.raise_for_status()
            content_length = resp.headers.get("Content-Length", 0)
            video_total_mb = byte2mb(content_length)
            desc_name = f"[{video_info_index+1}] {os.path.basename(video_info['file_path'])[:30]}"
            pbar = tqdm(
                total=video_total_mb, bar_format="{l_bar}{bar}| {n:.1f}/{total:.1f} {unit}", desc=desc_name, position=video_info_index + 1, 
                unit="MB", unit_scale=False, dynamic_ncols=True, leave=True, ascii="░█", 
            )
            chunk_size = 1024 * 1024
            with open(video_info['file_path'], "wb") as fp:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if not chunk: continue
                    fp.write(chunk)
                    pbar.update(len(chunk) / (1024 * 1024))
            downloaded_video_infos.append(video_info)
        except Exception as err:
            if pbar is not None: pbar.close()
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error: {err})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''download'''
    def download(self, video_infos: list, num_threadings: int = 5, request_overrides: dict = {}):
        if not video_infos: return []
        # logging
        self.logger_handle.info(f'Start to download videos using {self.source}.', disable_print=self.disable_print)
        # multi threadings for downloading videos
        self.default_headers = self.default_download_headers
        self._initsession()
        downloaded_video_infos = []
        with tqdm(
            total=len(video_infos), desc="Overall videos", position=0, dynamic_ncols=True, ascii="░█", unit="video", 
            bar_format="{l_bar}{bar}| {n}/{total} {unit}s",
        ) as overall_pbar:
            with ThreadPoolExecutor(max_workers=num_threadings) as executor:
                futures = [executor.submit(self._download, video_info, vid, downloaded_video_infos, request_overrides) for vid, video_info in enumerate(video_infos)]
                for _ in as_completed(futures):
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
        try:
            ext = tldextract.extract(url)
        except Exception:
            return False
        domain = ext.registered_domain
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