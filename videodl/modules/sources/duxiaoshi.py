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
            try:
                vid = parse_qs(parsed_url.query, keep_blank_values=True)['vid'][0]
            except:
                vid = parse_qs(parsed_url.query, keep_blank_values=True)['nid'][0]
                vid = vid.replace('sv_', '')
            resp = self.get(f"https://quanmin.hao222.com/wise/growth/api/sv/immerse?source=share-h5&pd=qm_share_mvideo&_format=json&vid={vid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            def _qualitykey(item: dict):
                w, h = int(item.get("width", 0)), int(item.get("height", 0))
                resolution = w * h
                bps = float(item.get("videoBps", 0))
                size = float(item.get("videoSize", 0))
                return (resolution, bps, size)
            candidate_urls = raw_data["data"]["meta"]["video_info"]["clarityUrl"]
            candidate_urls = [u for u in candidate_urls if u.get('url')]
            download_url = sorted(candidate_urls, key=_qualitykey, reverse=True)[0]['url']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'meta', 'title'], "") or safeextractfromdict(raw_data, ['data', 'shareInfo', 'title'], "") or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid
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
            valid_domains = ["quanmin.baidu.com", "mbd.baidu.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)