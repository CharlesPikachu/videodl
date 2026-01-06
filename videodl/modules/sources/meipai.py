'''
Function:
    Implementation of MeipaiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import base64
import urllib.parse
from parsel import Selector
from urllib.parse import urlparse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''MeipaiVideoClient'''
class MeipaiVideoClient(BaseVideoClient):
    source = 'MeipaiVideoClient'
    def __init__(self, **kwargs):
        super(MeipaiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_decodedownloadurl'''
    def _decodedownloadurl(self, download_url_bs64: str):
        hex_val, str_val = download_url_bs64[:4], download_url_bs64[4:]
        hex_1 = hex_val[::-1]
        str_n = str(int(hex_1, 16))
        length = len(str_n)
        pre = [int(str_n[i]) for i in range(length) if i < length - 2]
        tail = [int(str_n[i]) for i in range(length) if i >= length - 2]
        index_1, index_2 = pre[0], pre[0] + pre[1]
        c, d = str_val[:index_1], str_val[index_1:index_2]
        temp = str_val[index_2:].replace(d, "")
        d_val = c + temp
        tail[0] = len(d_val) - tail[0] - tail[1]
        p_val = tail
        index_1 = p_val[0]
        index_2 = p_val[0] + p_val[1]
        c2 = d_val[:index_1]
        d2 = d_val[index_1:index_2]
        temp2 = d_val[index_2:].replace(d2, "")
        kk_val = c2 + temp2
        decode_bs64 = base64.b64decode(kk_val)
        download_url = "https:" + decode_bs64.decode("utf-8")
        return download_url
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
            vid = urlparse(url).path.strip('/').split('/')[-1]
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            raw_data = resp.text
            video_info.update(dict(raw_data=raw_data))
            resp_selector = Selector(raw_data)
            download_url_bs64 = resp_selector.css("#shareMediaBtn::attr(data-video)").get(default="")
            download_url = self._decodedownloadurl(download_url_bs64=download_url_bs64)
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(
                urllib.parse.unquote(resp_selector.css("#shareMediaBtn::attr(data-title)").get(default="").strip(), encoding="utf-8") or null_backup_title, replace_null_string=null_backup_title,
            ).removesuffix('.')
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
            valid_domains = ["www.meipai.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)