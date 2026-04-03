'''
Function:
    Implementation of YouTubeVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import random
import requests
import json_repair
from .base import BaseVideoClient
from ..utils.youtubeutils import YouTube
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, VideoInfo, FileTypeSniffer


'''YouTubeVideoClient'''
class YouTubeVideoClient(BaseVideoClient):
    source = 'YouTubeVideoClient'
    def __init__(self, **kwargs):
        super(YouTubeVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {}
        self.default_download_headers = {}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlwithvidssave'''
    def _parsefromurlwithvidssave(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        get_download_link_func = lambda text: next((link for line in str(text).splitlines() if line.startswith("data:") for link in [json_repair.loads(line[5:].strip()).get("download_link")] if link), None)
        # try parse
        try:
            vid = parse_qs(urlparse(url).query, keep_blank_values=True)['v'][0]
            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "referer": "https://vidssave.com/"}
            (resp := self.post('https://api.vidssave.com/api/contentsite_api/media/parse', headers=headers, data={"link": url, "domain": "api-ak.vidssave.com", "origin": "source", "auth": "20250901majwlqo"}, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp)))); resources = [r for r in raw_data['data']['resources'] if isinstance(r, dict) and (str(r.get('format')).lower() in {'mp4'}) and (r.get('download_url') or r.get('resource_content'))][::-1]
            resources = sorted(resources, key=lambda item: item.get('size', 0) or 0, reverse=True); video_info.download_url = resources[0]['download_url']
            if not video_info.with_valid_download_url:
                (resp := self.post('https://api.vidssave.com/api/contentsite_api/media/download', data={'auth': '20250901majwlqo', 'domain': 'api-ak.vidssave.com', 'request': resources[0]['resource_content'], 'no_encrypt': '1'}, **request_overrides)).raise_for_status()
                max_retries_for_download_no_cache_contents, time_sleep_interval = 30, 0.5
                for _ in range(max_retries_for_download_no_cache_contents):
                    (resp := self.get('https://api.vidssave.com/sse/contentsite_api/media/download_query', params={'auth': '20250901majwlqo', 'domain': 'api-ak.vidssave.com', 'task_id': resp2json(resp=resp)['data']['task_id'], 'download_domain': 'vidssave.com', 'origin': 'content_site'}, **request_overrides)).raise_for_status()
                    if not (download_url := get_download_link_func(resp.text)): time.sleep(time_sleep_interval + random.random()); continue
                    video_info.update(dict(download_url=download_url)); break
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, identifier=vid, cover_url=safeextractfromdict(raw_data, ['data', 'thumbnail'], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlwithvidssave >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''_parsefromurlwithdownr'''
    def _parsefromurlwithdownr(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = parse_qs(urlparse(url).query, keep_blank_values=True)['v'][0]
            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "referer": "https://downr.org/"}
            cookies = requests.utils.dict_from_cookiejar(self.get('https://downr.org/.netlify/functions/analytics', **request_overrides).cookies)
            (resp := self.post('https://downr.org/.netlify/functions/nyt', headers=headers, cookies=cookies, json={"url": url}, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            video_medias: list[dict] = [item for item in raw_data['medias'] if item['type'] in ('video',)]
            audio_medias: list[dict] = [item for item in raw_data['medias'] if item['type'] in ('audio',)]
            video_medias: list[dict] = sorted(video_medias, key=lambda item: (item.get('height') * item.get('width'), item.get('bitrate')), reverse=True)
            audio_medias: list[dict] = sorted(audio_medias, key=lambda item: (item.get('bitrate'), float(item.get('audioSampleRate') or 0)), reverse=True)
            download_url, ext, audio_download_url, audio_ext = video_medias[0]['url'], video_medias[0]['ext'], audio_medias[0]['url'], audio_medias[0]['ext']
            video_info.update(dict(download_url=download_url, ext=ext, audio_download_url=audio_download_url, audio_ext=audio_ext))
            video_title = legalizestring(safeextractfromdict(raw_data, ['title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}'), identifier=vid, cover_url=safeextractfromdict(raw_data, ['thumbnail'], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlwithdownr >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse with some third part apis
        for parser in [self._parsefromurlwithvidssave, self._parsefromurlwithdownr]:
            video_infos = parser(url, request_overrides)
            if any(video_info.with_valid_download_url for video_info in (video_infos or [])): return video_infos
        # try parse with official apis
        try:
            vid = parse_qs(urlparse(url).query, keep_blank_values=True)['v'][0]
            yt = YouTube(video_id=vid); video_info.update(dict(raw_data=(raw_data := yt.vid_info)))
            download_url = yt.streams.gethighestresolution(); video_info.update(dict(download_url=download_url))
            video_title = legalizestring(yt.title, replace_null_string=null_backup_title).removesuffix('.')
            cover_url = safeextractfromdict(raw_data, ['videoDetails', 'thumbnail', 'thumbnails', -1, 'url'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.mp4'), ext='mp4', identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"youtube.com"}
        return BaseVideoClient.belongto(url, valid_domains)