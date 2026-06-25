'''
Function:
    Implementation of VeedMateVideoClient: https://veedmate.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import time
import base64
import random
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''VeedMateVideoClient'''
class VeedMateVideoClient(BaseVideoClient):
    source = 'VeedMateVideoClient'
    def __init__(self, **kwargs):
        super(VeedMateVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
            "accept": "*/*", "origin": "https://veedmate.com", "referer": "https://veedmate.com/",
        }
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        request_overrides, null_backup_title, video_infos = request_overrides or {}, yieldtimerelatedtitle(self.source), []
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers=self.BILIBILI_REFERENCE_HEADERS, default_audio_download_headers=self.BILIBILI_REFERENCE_HEADERS))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers=self.WEIBO_REFERENCE_HEADERS, default_audio_download_headers=self.WEIBO_REFERENCE_HEADERS))
        # try parse
        try:
            # --get request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            (resp := self.get('https://veedmate.com/', headers=headers, **request_overrides)).raise_for_status()
            config_text = '\n'.join([base64.b64decode(x).decode('utf-8', 'ignore') for x in re.findall(r'data:text/javascript;base64,([^"\']+)', resp.text)])
            ajax_url = re.findall(r'ajaxUrl:"([^"]+)"', config_text)[0]; nonce = re.findall(r'nonce:"([^"]+)"', config_text)[0]
            post_data = {'action': 'vd_download', 'nonce': nonce, 'url': url, 'resolution': '1080p'}
            (resp := self.post(ajax_url, data=post_data, headers=headers, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp)))); status_params = {'action': 'vd_status', 'job_id': raw_data['job_id']}
            if raw_data.get('_server'): status_params.update(dict(server=raw_data['_server']))
            while True:
                (resp := self.get(ajax_url, params=status_params, headers=headers, **request_overrides)).raise_for_status(); raw_data['progress_resp'] = resp2json(resp=resp)
                if raw_data['progress_resp'].get('status') == 'completed' and raw_data['progress_resp'].get('download_url'): break
                if raw_data['progress_resp'].get('status') == 'failed' or raw_data['progress_resp'].get('error'): raise RuntimeError(raw_data['progress_resp'])
                time.sleep(0.5 + random.random())
            # --extract
            video_title = legalizestring((progress_resp := raw_data['progress_resp']).get('title', null_backup_title) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(download_url=(download_url := progress_resp['download_url'])))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=progress_resp.get('job_id') or video_title, cover_url=progress_resp.get('thumbnail'))); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos