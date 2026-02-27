'''
Function:
    Implementation of XiguaVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''XiguaVideoClient'''
class XiguaVideoClient(BaseVideoClient):
    source = 'XiguaVideoClient'
    def __init__(self, **kwargs):
        super(XiguaVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlwithmixiguadouyin'''
    @useparseheaderscookies
    def _parsefromurlwithmixiguadouyin(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            (resp := self.get(f"https://m.ixigua.com/douyin/share/video/{vid}?aweme_type=107&schema_type=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme", **request_overrides)).raise_for_status()
            raw_data = re.findall(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>", resp.text)[0]
            raw_data = json_repair.loads(raw_data)
            video_info.update(dict(raw_data=raw_data))
            download_url = raw_data["loaderData"]["video_(id)/page"]['videoInfoRes']["item_list"][0]["video"]["play_addr"]["url_list"][0]
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data["loaderData"]["video_(id)/page"]['videoInfoRes']["item_list"][0].get('desc', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['loaderData', 'video_(id)/page', 'videoInfoRes', 'item_list', 0, 'video', 'cover', 'url_list', 0], None)
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlwithmixiguadouyin >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlwithmixiguadouyin]:
            video_infos = parser(url, request_overrides)
            if any(((info.get("download_url") or "").upper() not in ("", "NULL")) for info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"ixigua.com"}
        return BaseVideoClient.belongto(url, valid_domains)