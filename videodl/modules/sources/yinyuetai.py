'''
Function:
    Implementation of YinyuetaiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''YinyuetaiVideoClient'''
class YinyuetaiVideoClient(BaseVideoClient):
    source = 'YinyuetaiVideoClient'
    def __init__(self, **kwargs):
        super(YinyuetaiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        sortkey_func = lambda s: ((("MP3" in (disp := s.get("display", "")).upper()) or (s.get("streamType") == 5)), -(int(m.group(1)) if (m := re.search(r"(\d+)", disp)) else 0))
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            (resp := self.get(f'https://video-api.yinyuetai.com/video/get?id={vid}', verify=False, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            candidate_urls: list[dict] = raw_data["data"]["fullClip"]["urls"]; candidate_urls = [u for u in candidate_urls if u.get('url')]
            candidate_urls = sorted(candidate_urls, key=sortkey_func); download_url = candidate_urls[0]['url']; video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            cover_url = safeextractfromdict(raw_data, ['data', 'fullClip', 'cover'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"yinyuetai.com"}
        return BaseVideoClient.belongto(url, valid_domains)