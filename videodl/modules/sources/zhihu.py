'''
Function:
    Implementation of ZhihuVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''ZhihuVideoClient'''
class ZhihuVideoClient(BaseVideoClient):
    source = 'ZhihuVideoClient'
    def __init__(self, **kwargs):
        super(ZhihuVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
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
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            resp = self.get(f'https://www.zhihu.com/api/v4/zvideos/{vid}', **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            playlist = raw_data["video"]["playlist"]
            def _qualityscore(info: dict):
                w, h, bitrate, size = info.get("width") or 0, info.get("height") or 0, info.get("bitrate") or 0.0, info.get("size") or 0
                return (w * h, bitrate, size)
            sorted_playlist = sorted(playlist.items(), key=lambda kv: _qualityscore(kv[1]), reverse=True)
            sorted_playlist = [s for s in sorted_playlist if s[1].get('url')]
            download_url = sorted_playlist[0][1]['url']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data.get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid,
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
            valid_domains = ["www.zhihu.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)