'''
Function:
    Implementation of XinpianchangVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''XinpianchangVideoClient'''
class XinpianchangVideoClient(BaseVideoClient):
    source = 'XinpianchangVideoClient'
    def __init__(self, **kwargs):
        super(XinpianchangVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            "accept-encoding": "identity;q=1, *;q=0",
            "referer": "https://www.xinpianchang.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
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
            vid = parsed_url.path.strip('/').split('/')[-1][1:]
            resp = self.get(f'https://www.xinpianchang.com/api/xpc/v2/article/{vid}/related_folders', **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            media_id = raw_data['data']['list'][0]['article_list'][0]['item']['video_library_id'] or raw_data['data']['list'][0]['article_list'][0]['item']['media_id']
            resp = self.get(f"https://mod-api.xinpianchang.com/mod/api/v2/media/{media_id}?appKey=61a2f329348b3bf77&extend=userInfo%2CuserStatus", **request_overrides)
            resp.raise_for_status()
            raw_data[f'media/{media_id}'] = resp2json(resp=resp)
            progressive = raw_data[f'media/{media_id}']["data"]["resource"]["progressive"]
            sorted_by_resolution = sorted(progressive, key=lambda x: x['height'], reverse=True)
            download_urls = [item.get('url') or item.get('backupUrl') for item in sorted_by_resolution if item.get('url') or item.get('backupUrl')]
            download_url = download_urls[0]
            video_info.update(dict(download_url=download_url, download_with_ffmpeg=True))
            video_title = legalizestring(raw_data['data']['list'][0]['article_list'][0]['item'].get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
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
            valid_domains = ["www.xinpianchang.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)