'''
Function:
    Implementation of ABCVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, searchdictbykey, safeextractfromdict, VideoInfo, FileTypeSniffer


'''ABCVideoClient'''
class ABCVideoClient(BaseVideoClient):
    source = 'ABCVideoClient'
    def __init__(self, **kwargs):
        super(ABCVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlwithabcie'''
    @useparseheaderscookies
    def _parsefromurlwithabcie(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = re.compile(r'https?://(?:www\.)?abc\.net\.au/(?:news|btn|listen)/(?:[^/?#]+/){1,4}(?P<id>\d{5,})').match(url).group('id')
            (resp := self.get(url, **request_overrides)).raise_for_status()
            tag = BeautifulSoup(resp.text, "lxml").find("script", id="__NEXT_DATA__", type="application/json")
            assert (raw_data := json_repair.loads(tag.get_text()) if tag is not None else None) is not None
            video_info.update(dict(raw_data=raw_data))
            renditions: list[dict] = renditions if isinstance((renditions := searchdictbykey(raw_data, 'renditions')[0]), list) else renditions['files']
            renditions: list[dict] = sorted(renditions, key=lambda item: (item.get('size', 0) or item.get('fileSize', 0), item.get('height', 0), item.get('bitrate', 0) or item.get('bitRate', 0)), reverse=True)
            video_info.update(dict(download_url=(download_url := [r for r in renditions if r.get('url') and str(r.get('url')).startswith('http')][0]['url'])))
            video_title = legalizestring(safeextractfromdict(head_tags, [0, 'title'], None) if (head_tags := searchdictbykey(raw_data, 'headTagsSocialPrepared')) else null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(head_tags, [0, 'image'], None) if (head_tags := searchdictbykey(raw_data, 'headTagsSocialPrepared')) else None
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlwithabcie]:
            video_infos = parser(url, request_overrides)
            if any(((info.get("download_url") or "").upper() not in ("", "NULL")) for info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"abc.net.au"}
        return BaseVideoClient.belongto(url, valid_domains)