'''
Function:
    Implementation of EyepetizerVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, FileTypeSniffer, VideoInfo


'''EyepetizerVideoClient'''
class EyepetizerVideoClient(BaseVideoClient):
    source = 'EyepetizerVideoClient'
    def __init__(self, **kwargs):
        super(EyepetizerVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "x-thefair-appid": "xfpa44crf2p70lk8",
            "x-thefair-auth": "",
            "x-thefair-cid": "",
            "x-thefair-forward-host": "https://api.eyepetizer.net",
            "x-thefair-ua": "EYEPETIZER_UNIAPP_H5/100000 (android;android;OS_VERSION_UNKNOWN;zh-Hans-CN;h5;2.0.0;cn-bj;SOURCE_UNKNOWN;PHPSESSID;2560*1440;NETWORK_UNKNOWN) cardsystem/2.0"
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
        # try parse
        try:
            parsed_url = urlparse(url)
            parsed_url_qs = parse_qs(parsed_url.query, keep_blank_values=True)
            if 'video_id' in parsed_url_qs: vid = parsed_url_qs['video_id'][0]
            if 'vid' in parsed_url_qs: vid = parsed_url_qs['vid'][0]
            if 'resource_id' in parsed_url_qs: vid = parsed_url_qs['resource_id'][0]
            resp = self.post('https://proxy.eyepetizer.net/v1/content/item/get_item_detail_v2', data={'resource_type': 'pgc_video', 'resource_id': vid}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data["result"]["video"].get('title', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
            download_url = raw_data["result"]["video"]["play_url"]
            play_info = raw_data["result"]["video"]["play_info"]
            sorted_play_info = sorted(play_info, key=lambda x: (int(x["height"]), int(x["width"])), reverse=True)
            if sorted_play_info: download_url = sorted_play_info[0]['url']
            video_info.update(dict(download_url=download_url))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=vid,
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
            valid_domains = ["home.eyepetizer.net", "www.eyepetizer.net", "m.eyepetizer.net"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)