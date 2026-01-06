'''
Function:
    Implementation of CCTVVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import shutil
import hashlib
from .base import BaseVideoClient
from urllib.parse import urlsplit
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''CCTVVideoClient'''
class CCTVVideoClient(BaseVideoClient):
    source = 'CCTVVideoClient'
    def __init__(self, **kwargs):
        super(CCTVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            # --fetch raw data
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            rules = [
                r'var\s+guid\s*=\s*["\']([\da-fA-F]+)', r'videoCenterId(?:["\']\s*,|:)\s*["\']([\da-fA-F]+)', r'changePlayer\s*\(\s*["\']([\da-fA-F]+)',
                r'load[Vv]ideo\s*\(\s*["\']([\da-fA-F]+)', r'var\s+initMyAray\s*=\s*["\']([\da-fA-F]+)', r'var\s+ids\s*=\s*\[["\']([\da-fA-F]+)'
            ]
            for rule in rules:
                try:
                    pid = re.findall(rule, resp.text)[0]
                    break
                except:
                    continue
            md5 = lambda value: hashlib.md5(value.encode('utf-8')).hexdigest()
            params = {
                'pid': pid, 'client': 'flash', 'im': '0', 'tsp': str(int(time.time())), 'vn': '2049', 'vc': None, 'uid': '826D8646DEBBFD97A82D23CAE45A55BE', 'wlan': '',
            }
            params['vc'] = md5((params['tsp'] + params['vn'] + "47899B86370B879139C08EA3B5E88267" + params['uid']))
            resp = self.get('https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --parse urls
            manifest, download_urls = raw_data.get('manifest'), []
            hls_candidates = ['hls_enc2_url', 'hls_url'] if shutil.which('cbox') else ['hls_url']
            for hls_key in hls_candidates:
                if raw_data.get(hls_key) or manifest.get(hls_key):
                    download_urls.append([hls_key, raw_data.get(hls_key) or manifest.get(hls_key)])
            hls_key, download_url = download_urls[0]
            if hls_key not in ['hls_url']: download_url = re.sub(r"https://[^/]+/asp/enc2/", 'https://drm.cntv.vod.dnsv1.com/asp/enc2/', download_url)
            video_info.update(dict(download_url=download_url, download_with_ffmpeg_cctv=True if hls_key not in ['hls_url'] else False, pid=pid))
            # --create video info's extra entries
            video_title = legalizestring(raw_data.get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=pid,
            ))
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        # set valid domains
        if valid_domains is None:
            valid_domains = []
        # extract domain
        parsed_url = urlsplit(url)
        domain = parsed_url.netloc
        # judge and return according to domain
        is_valid = (domain in valid_domains) or domain.endswith('cctv.com') or domain.endswith('cctv.cn')
        return is_valid