'''
Function:
    Implementation of C56VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import json_repair
from datetime import datetime
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from .sohu import SohuVideoClient
from ..utils import legalizestring, useparseheaderscookies, VideoInfo


'''C56VideoClient'''
class C56VideoClient(BaseVideoClient):
    source = 'C56VideoClient'
    def __init__(self, **kwargs):
        super(C56VideoClient, self).__init__(**kwargs)
        self.sohu_parser = SohuVideoClient(**kwargs)
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
        # try parse
        try:
            vid = re.search(r'https?://(?:(?:www|player)\.)?56\.com/(?:.+?/)?(?:v_|(?:play_album.+-))(?P<textid>.+?)\.(?:html|swf)', url).group(1)
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            script_tag = soup.find("script", string=re.compile(r"var\s+videoInfo\s*="))
            script_text: str = script_tag.string
            m = re.search(r"var\s+videoInfo\s*=\s*({.*?});", script_text, re.S)
            raw_data = json_repair.loads(m.group(1))
            sohu_video_url = raw_data['sohu']['video_url']
            video_info: VideoInfo = self.sohu_parser.parsefromurl(sohu_video_url, request_overrides=request_overrides)
            assert len(video_info) == 1
            video_info = video_info[0]
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(raw_data.get('Subject', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            video_info.update(dict(
                identifier=vid, raw_data=raw_data, title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info["ext"]}'),
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
            valid_domains = ["www.56.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)