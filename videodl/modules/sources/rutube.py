'''
Function:
    Implementation of RutubeVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import urllib.parse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, FileTypeSniffer, VideoInfo


'''RutubeVideoClient'''
class RutubeVideoClient(BaseVideoClient):
    source = 'RutubeVideoClient'
    def __init__(self, **kwargs):
        super(RutubeVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
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
            vid = re.search(r'https?://rutube\.ru/(?:(?:live/)?video(?:/private)?|(?:play/)?embed)/(?P<id>[\da-z]{32})', url).group('id')
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            query_dict = {'format': 'json', 'p': query_params['p'][0]} if 'p' in query_params else {'format': 'json'}
            api_url = f"https://rutube.ru/api/video/{vid}/?{urllib.parse.urlencode(query_dict)}"
            (resp := self.get(api_url, **request_overrides)).raise_for_status(); video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            api_url = f"https://rutube.ru/api/play/options/{vid}/?{urllib.parse.urlencode(query_dict)}"
            (resp := self.get(api_url, **request_overrides)).raise_for_status(); options = resp2json(resp=resp)
            download_url = safeextractfromdict(options, ['video_balancer', 'm3u8'], None) or safeextractfromdict(options, ['video_balancer', 'default'], None) or safeextractfromdict(options, ['live_streams', 'hls'], None)
            video_info.update(dict(download_url=(download_url := download_url[0]['url'] if isinstance(download_url, list) and len(download_url) > 0 else download_url)))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_title = legalizestring(safeextractfromdict(raw_data, ['title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(raw_data, ['thumbnail_url'], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"rutube.ru"}
        return BaseVideoClient.belongto(url, valid_domains)