'''
Function:
    Implementation of VeedMateVideoClient: https://veedmate.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
import random
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, safeextractfromdict


'''VeedMateVideoClient'''
class VeedMateVideoClient(BaseVideoClient):
    source = 'VeedMateVideoClient'
    def __init__(self, **kwargs):
        super(VeedMateVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "accept": "*/*", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://veedmate.com", "priority": "u=1, i", "referer": "https://veedmate.com/", "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"', 
            "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "cross-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "sec-ch-ua-mobile": "?0",
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
            params = {'allow_extended_duration': '0', 'copyright': '0', 'format': '1080', 'url': url, 'no_merge': '0'}
            (resp := self.get('https://auralis-b5it.onrender.com/api/download?', params=params, headers=headers, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp)))); progress_url = raw_data['progress_url']
            while True:
                (resp := self.get(progress_url, **request_overrides)).raise_for_status(); raw_data['progress_resp'] = resp2json(resp=resp)
                if raw_data['progress_resp']['success'] in {1, '1'}: break
                time.sleep(0.5 + random.random())
            # --extract
            video_title = legalizestring(raw_data.get('title', null_backup_title) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(download_url=(download_url := raw_data['progress_resp']['download_url'])))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=safeextractfromdict(raw_data, ['info', 'image'], None))); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos