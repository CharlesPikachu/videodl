'''
Function:
    Implementation of FoxNewsVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, resp2json, searchdictbykey, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''FoxNewsVideoClient'''
class FoxNewsVideoClient(BaseVideoClient):
    source = 'FoxNewsVideoClient'
    def __init__(self, **kwargs):
        super(FoxNewsVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            re_patterns = [r'https?://(?:www\.)?foxnews\.com/video/(?P<id>\d+)', r'https?://video\.(?:insider\.)?fox(?:news|business)\.com/v/(?:video-embed\.html\?video_id=)?(?P<id>\d+)']
            for re_pattern in re_patterns:
                try:
                    video_id = re.compile(re_pattern).match(url).group('id')
                    break
                except:
                    continue
            resp = self.get(f'https://api.foxnews.com/v3/video-player/{video_id}?callback=uid_{video_id}', **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            download_url = searchdictbykey(raw_data, 'media-content')[0][0]['@attributes']['url']
            video_info.update(dict(download_url=download_url))
            video_title = searchdictbykey(raw_data, 'media-title')
            video_title = legalizestring(video_title[0] if video_title else null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_id,
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
            valid_domains = ["www.foxnews.com", "video.foxnews.com", "video.insider.foxnews.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)