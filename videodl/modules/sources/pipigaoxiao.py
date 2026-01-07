'''
Function:
    Implementation of PipigaoxiaoVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json
import copy
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''PipigaoxiaoVideoClient'''
class PipigaoxiaoVideoClient(BaseVideoClient):
    source = 'PipigaoxiaoVideoClient'
    def __init__(self, **kwargs):
        super(PipigaoxiaoVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'Host': 'share.ippzone.com',
            'Origin': 'http://share.ippzone.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
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
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
            url = re.findall(pattern, url)[0]
            headers = copy.deepcopy(self.default_headers)
            headers['Referer'] = url
            try:
                mid, pid = re.findall('mid=(\d+)', url, re.S)[0], re.findall('pid=(\d+)', url, re.S)[0]
            except:
                mid, pid = '', urlparse(url).path.replace("/pp/post/", "")
            data = {'mid': int(mid) if mid else 'null', 'pid': int(pid), 'type': 'post'}
            resp = self.post('https://h5.ippzone.com/ppapi/share/fetch_content', data=json.dumps(data), headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp)
            video_info.update(dict(raw_data=raw_data))
            for candidate_key in ['url', 'urlwm', 'h5url']:
                download_url = raw_data['data']['post']['videos'][str(raw_data['data']['post']['imgs'][0]['id'])].get(candidate_key, '')
                if download_url: break
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data['data']['post'].get('content', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=pid
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
        if valid_domains is None:
            valid_domains = ['h5.ippzone.com', 'share.ippzone.com']
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)