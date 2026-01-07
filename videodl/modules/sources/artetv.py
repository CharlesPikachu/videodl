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
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''ArteTVVideoClient'''
class ArteTVVideoClient(BaseVideoClient):
    source = 'ArteTVVideoClient'
    def __init__(self, **kwargs):
        super(ArteTVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
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
            vid = re.search(r"/videos/([^/]+)/", url).group(1)
            lang = re.search(r"\.tv/([^/]+)/videos/", url).group(1)
            headers = copy.deepcopy(self.default_headers)
            headers.update({'Referer': url})
            resp = self.get(f'https://api.arte.tv/api/player/v2/config/{lang}/{vid}', headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_title = legalizestring(raw_data["data"]["attributes"]['metadata'].get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            streams = raw_data["data"]["attributes"]['streams']
            def _qualityvalue(stream: dict):
                label: str = stream.get("mainQuality", {}).get("label", "")
                for part in label.split("p"):
                    if part.isdigit(): return int(part)
                return 0
            sorted_streams: list[dict] = sorted(streams, key=_qualityvalue, reverse=True)
            sorted_streams: list[dict] = [item for item in sorted_streams if item.get('url')]
            download_url = sorted_streams[0]['url']
            video_info.update(dict(download_url=download_url))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True,
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
            valid_domains = ["www.arte.tv"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)