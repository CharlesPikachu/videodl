'''
Function:
    Implementation of DuxiaoshiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''DuxiaoshiVideoClient'''
class DuxiaoshiVideoClient(BaseVideoClient):
    source = 'DuxiaoshiVideoClient'
    def __init__(self, **kwargs):
        super(DuxiaoshiVideoClient, self).__init__(**kwargs)
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
        quality_key_func = lambda item: (int(item.get("width", 0)) * int(item.get("height", 0)), float(item.get("videoBps", 0)), float(item.get("videoSize", 0)))
        # try parse
        try:
            try: vid = parse_qs(urlparse(url).query, keep_blank_values=True)['vid'][0]
            except: vid = parse_qs(urlparse(url).query, keep_blank_values=True)['nid'][0]; vid = vid.removeprefix('sv_')
            (resp := self.get(f"https://quanmin.hao222.com/wise/growth/api/sv/immerse?source=share-h5&pd=qm_share_mvideo&_format=json&vid={vid}", **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            candidate_urls: list[dict] = raw_data["data"]["meta"]["video_info"]["clarityUrl"]
            candidate_urls = [u for u in candidate_urls if u.get('url')]
            download_url = sorted(candidate_urls, key=quality_key_func, reverse=True)[0]['url']; video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'meta', 'title'], "") or safeextractfromdict(raw_data, ['data', 'shareInfo', 'title'], "") or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['data', 'meta', 'image'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"quanmin.baidu.com", "mbd.baidu.com"}
        return BaseVideoClient.belongto(url, valid_domains)