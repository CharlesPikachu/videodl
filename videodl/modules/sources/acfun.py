'''
Function:
    Implementation of AcFunVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import time
import subprocess
import json_repair
from datetime import datetime
from .base import BaseVideoClient
from ..utils import legalizestring, touchdir


'''AcFunVideoClient'''
class AcFunVideoClient(BaseVideoClient):
    source = 'AcFunVideoClient'
    def __init__(self, **kwargs):
        super(AcFunVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_download'''
    def _download(self, video_info: dict, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = {}):
        # not deal with video info with errors
        if not video_info.get('download_url') or video_info.get('download_url') == 'NULL': return downloaded_video_infos
        # prepare
        touchdir(os.path.dirname(video_info['file_path']))
        headers = []
        for k, v in self.default_download_headers.items():
            headers.append(f"{k}: {v}\r\n")
        headers_str = "".join(headers)
        file_path, same_name_file_idx = video_info['file_path'], 1
        while os.path.exists(file_path):
            directory, file_name = os.path.split(video_info['file_path'])
            file_name_without_ext = os.path.splitext(file_name)[0]
            file_path = os.path.join(directory, f"{file_name_without_ext}_{same_name_file_idx}.{video_info['ext']}")
            same_name_file_idx += 1
        # start to download
        cmd = ["ffmpeg", "-y", "-headers", headers_str, "-i", video_info["download_url"], "-c", "copy", "-bsf:a", "aac_adtstoasc"]
        for _, proxy_url in request_overrides.get('proxies', {}).items():
            cmd.extend(["-http_proxy", proxy_url])
        cmd.append(file_path)
        capture_output = True if self.disable_print else False
        ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
        if ret.returncode == 0:
            downloaded_video_infos.append(video_info)
        else:
            err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
            self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # return
        return downloaded_video_infos
    '''parsefromurl'''
    def parsefromurl(self, url: str, request_overrides: dict = {}):
        # prepare
        video_info = {'source': self.source, 'raw_data': 'NULL', 'download_url': 'NULL', 'video_title': 'NULL', 'file_path': 'NULL', 'ext': 'mp4'}
        if not self.belongto(url=url): return [video_info]
        # try parse
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            raw_data = json_repair.loads(re.findall('window.pageInfo =(.*?);', resp.text)[0].split('=', 1)[-1].strip())
            video_info.update(dict(raw_data=raw_data))
            try:
                download_url = json_repair.loads(raw_data['currentVideoInfo']['ksPlayJsonHevc'])['adaptationSet'][0]['representation'][0]['url']
            except:
                download_url = json_repair.loads(raw_data['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['url']
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H:%M:%S")
            video_title = legalizestring(raw_data.get('title', f'{self.source}_null_{date_str}'))
            video_info.update(dict(video_title=video_title, file_path=os.path.join(self.work_dir, video_title + f'.{video_info["ext"]}')))
        except Exception as err:
            self.logger_handle.error(f'{self.source}.parsefromurl >>> {url} (Error: {err})', disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["acfun.cn"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)