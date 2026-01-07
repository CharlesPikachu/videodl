'''
Function:
    Implementation of YoukuVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import random
import string
from .base import BaseVideoClient
from urllib.parse import urlparse, parse_qs
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''YoukuVideoClient'''
class YoukuVideoClient(BaseVideoClient):
    source = 'YoukuVideoClient'
    def __init__(self, **kwargs):
        super(YoukuVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        if not self.default_parse_cookies: self.default_parse_cookies = {'__ysuid': self._getysuid(), 'xreferrer': 'http://www.youku.com'}
        self._initsession()
    '''_getysuid'''
    def _getysuid(self):
        return "{}{}".format(int(time.time()), ''.join(random.choices(string.ascii_letters, k=3)))
    '''_getformatname'''
    def _getformatname(self, fm):
        return {'3gp': 'h6', '3gphd': 'h5', 'flv': 'h4', 'flvhd': 'h4', 'mp4': 'h3', 'mp4hd': 'h3', 'mp4hd2': 'h4', 'mp4hd3': 'h4', 'hd2': 'h2', 'hd3': 'h1'}.get(fm)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, download_with_ffmpeg=True)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            parsed_url = urlparse(url)
            if parsed_url.netloc in ["v.youku.com"]:
                vid = parsed_url.path.strip('/').split('/')[-1].removesuffix('.html').removeprefix('id_')
            else:
                vid = parse_qs(parsed_url.query, keep_blank_values=True)['vid'][0]
            resp = self.get('https://log.mmstat.com/eg.js', **request_overrides)
            resp.raise_for_status()
            etag = resp.headers.get('ETag') or resp.headers.get('etag')
            cna = etag.strip('"')
            params = {'vid': vid, 'ccode': '0564', 'client_ip': '192.168.1.1', 'utid': cna, 'client_ts': int(time.time())}
            self.default_headers.update({'Referer': url})
            resp = self.get(f'https://ups.youku.com/ups/get.json', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            video_data = raw_data.get('data') or {}
            video_urls = [{
                'url': stream.get('m3u8_url'), 'filesize': int(stream.get('size', 0) or 0), 'width': int(stream.get('width', 0) or 0), 'height': int(stream.get('height', 0) or 0)
            } for stream in video_data.get('stream', []) if stream.get('channel_type') != 'tail']
            video_urls_sorted = sorted(video_urls, key=lambda f: (f.get('height') or 0, f.get('width') or 0, f.get('filesize') or 0), reverse=True)
            video_urls_sorted = [v for v in video_urls_sorted if v.get('url')]
            download_url = video_urls_sorted[0]['url']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(video_data, ['video', 'title'], null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
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
            valid_domains = ["v.youku.com", "www.youku.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)