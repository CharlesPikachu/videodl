'''
Function:
    Implementation of KugouMVVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import json
import uuid
import hashlib
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, safeextractfromdict, FileTypeSniffer, VideoInfo


'''KugouMVVideoClient'''
class KugouMVVideoClient(BaseVideoClient):
    source = 'KugouMVVideoClient'
    UUID = uuid.uuid4().hex
    def __init__(self, **kwargs):
        super(KugouMVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_calcsignature'''
    def _calcsignature(self, params: dict, post_data: dict = None, post_type: str = "json"):
        salt, all_params = "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt", params.copy()
        keys, kv_pairs = sorted(all_params.keys()), []
        for k in keys: kv_pairs.append(f"{k}={all_params[k]}")
        if post_data:
            if post_type == "json": kv_pairs.append(json.dumps(post_data, separators=(',', ':')))
            else: post_str = "&".join([f"{k}={v}" for k, v in post_data.items()]); kv_pairs.append(post_str)
        sign_content = salt + "".join(kv_pairs) + salt
        return hashlib.md5(sign_content.encode('utf-8')).hexdigest()
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
            vid = urlparse(url).path.strip('/').split('/')[-1]
            params = {'srcappid': '2919', 'clientver': '1000', 'clienttime': str(int(time.time() * 1000)), 'mid': KugouMVVideoClient.UUID, 'uuid': KugouMVVideoClient.UUID, 'dfid': '1u0Qpt0FTdFC2BtwCF2hRvQ1', 'appid': '1014', 'id': vid}
            params['signature'] = self._calcsignature(params=params)
            (resp := self.get(f"https://wwwapi.kugou.com/play/mv", params=params, **request_overrides)).raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            play_info = [(k, v) for k, v in dict(raw_data['data']['play']).items() if (v['downurl'] or v['backupdownurl'][0]) and (str(v['downurl']).startswith('http') or str(v['backupdownurl'][0]).startswith('http'))]
            play_info = sorted(play_info, key=lambda item: int(float((item[1]["filesize"]))), reverse=True)
            download_url = play_info[0][1]['downurl'] or play_info[0][1]['backupdownurl']
            if download_url and isinstance(download_url, list): download_url = download_url[0]
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'info', 'base', 'mv_name'], None), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['data', 'info', 'base', 'hdpic'], None)
            if cover_url and '{size}' in cover_url: cover_url = cover_url.replace('{size}', '480')
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
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
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"kugou.com"}
        return BaseVideoClient.belongto(url, valid_domains)