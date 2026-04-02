'''
Function:
    Implementation of DouyinVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''DouyinVideoClient'''
class DouyinVideoClient(BaseVideoClient):
    source = 'DouyinVideoClient'
    ROUTER_DATA_RE = re.compile(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>", re.S | re.I)
    def __init__(self, **kwargs):
        super(DouyinVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
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
            (resp := self.get(url, allow_redirects=False, **request_overrides)).raise_for_status(); location = resp.headers.get("Location")
            if not location: (resp := self.get(url, allow_redirects=True, **request_overrides)).raise_for_status(); location = resp.url
            vid = re.search(r"\d+", location).group(0)
            (resp := self.get(f"https://www.iesdouyin.com/share/video/{vid}", **request_overrides)).raise_for_status()
            raw_data = DouyinVideoClient.ROUTER_DATA_RE.search(resp.text).group(1).strip().rstrip("; \n\r\t")
            if not raw_data.startswith("{"): raw_data = raw_data[raw_data.find("{"):].rstrip("; \n\r\t") if raw_data.find("{") != -1 else raw_data
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(raw_data))))
            video_detail = safeextractfromdict(raw_data, ['loaderData', 'video_(id)/page', 'videoInfoRes', 'item_list', 0], {})
            video_info.update(dict(download_url=(download_url := f"http://www.iesdouyin.com/aweme/v1/play/?video_id={video_detail['video']['play_addr']['uri']}&ratio=1080p&line=0")))
            video_title = legalizestring(video_detail.get('desc') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(video_detail, ['video', 'cover', 'url_list', 0], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"douyin.com"}
        return BaseVideoClient.belongto(url, valid_domains)