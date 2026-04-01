'''
Function:
    Implementation of WWEVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''WWEVideoClient'''
class WWEVideoClient(BaseVideoClient):
    source = 'WWEVideoClient'
    def __init__(self, **kwargs):
        super(WWEVideoClient, self).__init__(**kwargs)
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
            (resp := self.get(url, **request_overrides)).raise_for_status()
            tag = BeautifulSoup(resp.text, "html.parser").select_one('script[type="application/json"][data-drupal-selector="drupal-settings-json"]')
            if not tag or not tag.string: raise Exception
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(tag.string))))
            vid = raw_data['WWEVideoLanding']['initialVideoId']; download_url = raw_data['WWEVideoLanding']['initialVideo']['playlist'][0]['file']
            video_info.update(dict(download_url=(download_url := f'https:{download_url}' if not download_url.startswith('https') else download_url)))
            video_title = legalizestring(safeextractfromdict(raw_data, ['WWEVideoLanding', 'initialVideo', 'playlist', 0, 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['videoPlayer', 'videoImageuri'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"wwe.com"}
        return BaseVideoClient.belongto(url, valid_domains)