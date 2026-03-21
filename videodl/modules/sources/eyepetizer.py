'''
Function:
    Implementation of EyepetizerVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''EyepetizerVideoClient'''
class EyepetizerVideoClient(BaseVideoClient):
    source = 'EyepetizerVideoClient'
    def __init__(self, **kwargs):
        super(EyepetizerVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "x-thefair-appid": "xfpa44crf2p70lk8", "x-thefair-forward-host": "https://api.eyepetizer.net",
            "x-thefair-ua": "EYEPETIZER_UNIAPP_H5/100000 (android;android;OS_VERSION_UNKNOWN;zh-Hans-CN;h5;2.0.0;cn-bj;SOURCE_UNKNOWN;PHPSESSID;2560*1440;NETWORK_UNKNOWN) cardsystem/2.0", "x-thefair-cid": "", "x-thefair-auth": "", 
        }
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            parsed_url_qs = parse_qs(urlparse(url).query, keep_blank_values=True)
            vid = next((parsed_url_qs[k][0] for k in ('resource_id', 'vid', 'video_id') if k in parsed_url_qs), None)
            (resp := self.post('https://proxy.eyepetizer.net/v1/content/item/get_item_detail_v2', data={'resource_type': 'pgc_video', 'resource_id': vid}, **request_overrides)).raise_for_status()
            video_title = legalizestring(safeextractfromdict((raw_data := resp2json(resp=resp)), ['result', 'video', 'title'], null_backup_title) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            download_url = raw_data["result"]["video"]["play_url"]; play_info = safeextractfromdict(raw_data, ['result', 'video', 'play_info'], {}) or {}
            sorted_play_info: list[dict] = sorted(play_info, key=lambda x: (int(x["height"]), int(x["width"])), reverse=True)
            sorted_play_info: list[dict] = [item for item in sorted_play_info if item.get('url')]
            video_info.update(dict(download_url=(download_url := sorted_play_info[0]['url'] if sorted_play_info else download_url)))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['result', 'video', 'cover', 'url'], None)
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"eyepetizer.net"}
        return BaseVideoClient.belongto(url, valid_domains)