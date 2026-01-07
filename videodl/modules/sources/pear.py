'''
Function:
    Implementation of PearVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import random
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''PearVideoClient'''
class PearVideoClient(BaseVideoClient):
    source = 'PearVideoClient'
    def __init__(self, **kwargs):
        super(PearVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'https://www.pearvideo.com/',
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
            video_id = parsed_url.path.split('/')[-1].replace("video_", "")
            headers = copy.deepcopy(self.default_headers)
            headers['Referer'] = f"https://www.pearvideo.com/detail_{video_id}"
            resp = self.get(f"https://www.pearvideo.com/videoStatus.jsp?contId={video_id}&mrd={random.random()}", headers=headers, **request_overrides)
            self.default_headers.pop('Referer')
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            for quality in ['srcUrl', 'hdUrl', 'hdflvUrl', 'sdUrl', 'sdflvUrl']:
                download_url = raw_data["videoInfo"]["videos"][quality]
                if download_url: break
            timestamp = urlparse(download_url).path.strip('/').split('/')[-1].split('-')[0]
            download_url = download_url.replace(f'/{timestamp}-', f'/cont-{video_id}-')
            video_info.update(dict(download_url=download_url))
            try:
                video_title = BeautifulSoup(self.get(url, headers=headers, **request_overrides).text, "html.parser").title.get_text(strip=True)
            except:
                video_title = null_backup_title
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_id
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
            valid_domains = ["www.pearvideo.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)