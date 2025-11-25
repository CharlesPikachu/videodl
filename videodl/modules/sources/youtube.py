'''
Function:
    Implementation of YouTubeVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
from datetime import datetime
from .base import BaseVideoClient
from ..utils.youtubeutils import YouTube
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, VideoInfo


'''YouTubeVideoClient'''
class YouTubeVideoClient(BaseVideoClient):
    source = 'YouTubeVideoClient'
    def __init__(self, **kwargs):
        super(YouTubeVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {}
        self.default_download_headers = {}
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
            vid = parse_qs(parsed_url.query, keep_blank_values=True)['v'][0]
            yt = YouTube(video_id=vid)
            raw_data = yt.vid_info
            video_info.update(dict(raw_data=raw_data))
            download_url = yt.streams.gethighestresolution()
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(yt.title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            ext = 'mp4'
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, identifier=vid))
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
            valid_domains = ["www.youtube.com", "music.youtube.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)