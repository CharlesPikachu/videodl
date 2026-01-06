'''
Function:
    Implementation of HaokanVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''HaokanVideoClient'''
class HaokanVideoClient(BaseVideoClient):
    source = 'HaokanVideoClient'
    def __init__(self, **kwargs):
        super(HaokanVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Cookie': 'BAIDUID=299CB9BD602F22B0730A5281C20D9EC4:FG=1; PC_TAB_LOG=haokan_website_page; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1591580053; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1591580666;',
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
            vid = parse_qs(parsed_url.query, keep_blank_values=True)['vid'][0]
            resp = self.get(f"https://haokan.baidu.com/v?_format=json&vid={vid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp.json()
            video_info.update(dict(raw_data=raw_data))
            for rate in sorted(raw_data["data"]["apiData"]["curVideoMeta"]['clarityUrl'], key=lambda x: float(x['videoSize']), reverse=True):
                download_url = rate.get('url', '')
                if download_url: break
            if not download_url: download_url = raw_data["data"]["apiData"]["curVideoMeta"]['playurl']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data["data"]["apiData"]["curVideoMeta"].get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
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
            valid_domains = ["haokan.baidu.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)