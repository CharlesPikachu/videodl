'''
Function:
    Implementation of BeaconVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, searchdictbykey, safeextractfromdict, resp2json, VideoInfo


'''BeaconVideoClient'''
class BeaconVideoClient(BaseVideoClient):
    source = 'BeaconVideoClient'
    def __init__(self, **kwargs):
        super(BeaconVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
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
            vid = urlparse(url).path.strip('/').split('/')[-1]
            (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(BeautifulSoup(resp.text, "lxml").select_one("script#__NEXT_DATA__").string))))
            content_data = safeextractfromdict(raw_data, ('props', 'pageProps', '__APOLLO_STATE__')); video_data = searchdictbykey(content_data, 'contentVideo')[0]
            (resp := self.get(searchdictbykey(video_data, 'playlistUrl')[0], **request_overrides)).raise_for_status(); raw_data['playlist_result'] = resp2json(resp=resp)
            download_urls = sorted(raw_data['playlist_result']['playlist'][0]['sources'], key=lambda item: (item.get('filesize', 0), item.get('bitrate', 0), item.get('width', 0) * item.get('height', 0)), reverse=True)
            download_url = download_urls[0]['file']; video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data['playlist_result'], ['playlist', 0, 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            cover_url = safeextractfromdict(raw_data['playlist_result'], ['playlist', 0, 'images', -1, 'src'], None)
            vid = safeextractfromdict(raw_data['playlist_result'], ['playlist', 0, 'mediaid'], None) or vid
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info.ext}'), identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"beacon.tv"}
        return BaseVideoClient.belongto(url, valid_domains)