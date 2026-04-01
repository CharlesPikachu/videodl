'''
Function:
    Implementation of ArteTVVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''ArteTVVideoClient'''
class ArteTVVideoClient(BaseVideoClient):
    source = 'ArteTVVideoClient'
    def __init__(self, **kwargs):
        super(ArteTVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(download_with_ffmpeg=True, source=self.source), yieldtimerelatedtitle(self.source)
        quality_value_func = lambda stream: next((int(part) for part in str(safeextractfromdict(stream, ['mainQuality', 'label'], '')).split("p") if part.isdigit()), 0)
        # try parse
        try:
            vid = re.search(r"/videos/([^/]+)/", url).group(1); lang = re.search(r"\.tv/([^/]+)/videos/", url).group(1)
            (headers := copy.deepcopy(self.default_headers)).update({'Referer': url})
            (resp := self.get(f'https://api.arte.tv/api/player/v2/config/{lang}/{vid}', headers=headers, **request_overrides)).raise_for_status()
            video_title = legalizestring(safeextractfromdict((raw_data := resp2json(resp=resp)), ["data", "attributes", "metadata", "title"], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            sorted_streams: list[dict] = sorted(raw_data["data"]["attributes"]['streams'], key=quality_value_func, reverse=True)
            sorted_streams: list[dict] = [item for item in sorted_streams if item.get('url')]
            video_info.update(dict(download_url=(download_url := sorted_streams[0]['url'])))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(raw_data, ['data', 'attributes', 'metadata', 'images', 0, 'url'], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"arte.tv"}
        return BaseVideoClient.belongto(url, valid_domains)