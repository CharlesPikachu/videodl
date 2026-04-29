'''
Function:
    Implementation of YouTubeVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import requests
from contextlib import suppress
from .base import BaseVideoClient
from ..utils.youtubeutils import YouTube
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, floatornone, VideoInfo


'''YouTubeVideoClient'''
class YouTubeVideoClient(BaseVideoClient):
    source = 'YouTubeVideoClient'
    def __init__(self, **kwargs):
        super(YouTubeVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlwithytdown'''
    def _parsefromurlwithytdown(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, vid = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), parse_qs(urlparse(url).query, keep_blank_values=True)['v'][0]
        headers = {"origin": "https://app.ytdown.to", "referer": "https://app.ytdown.to/en27/", "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"}
        # try parse
        try:
            (resp := requests.post('https://app.ytdown.to/proxy.php', data={'url': url}, headers=headers, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            video_medias = [item for item in raw_data['api']['mediaItems'] if isinstance(item, dict) and (str(item.get('type')).lower() in {'video'}) and str(item.get('mediaUrl')).startswith('http')]
            video_medias = sorted(video_medias, key=lambda item: floatornone(str(item.get('mediaFileSize')).split(' ')[0]), reverse=True)
            audio_medias = [item for item in raw_data['api']['mediaItems'] if isinstance(item, dict) and (str(item.get('type')).lower() in {'audio'}) and str(item.get('mediaUrl')).startswith('http')]
            audio_medias = sorted(audio_medias, key=lambda item: floatornone(str(item.get('mediaFileSize')).split(' ')[0]), reverse=True)
            for video_media in video_medias:
                (resp := requests.post('https://app.ytdown.to/proxy.php', data={'url': video_media['mediaUrl']}, headers=headers, **request_overrides)).raise_for_status()
                download_url, ext, download_url_can_be_visited = resp2json(resp=resp)['api']['fileUrl'], str(video_media['mediaExtension']).lower(), False; (stream_headers := headers.copy()).update({"Range": "bytes=0-0"})
                with suppress(Exception): resp = None; (resp := requests.get(download_url, stream=True, headers=stream_headers, allow_redirects=True, verify=False, **request_overrides)).raise_for_status(); download_url_can_be_visited = True
                if hasattr(resp, 'text') and download_url_can_be_visited: break
            for audio_media in audio_medias:
                (resp := requests.post('https://app.ytdown.to/proxy.php', data={'url': audio_media['mediaUrl']}, headers=headers, **request_overrides)).raise_for_status()
                audio_download_url, audio_ext, audio_download_url_can_be_visited = resp2json(resp=resp)['api']['fileUrl'], str(audio_media['mediaExtension']).lower(), False; (stream_headers := headers.copy()).update({"Range": "bytes=0-0"})
                with suppress(Exception): resp = None; (resp := requests.get(audio_download_url, stream=True, headers=stream_headers, allow_redirects=True, verify=False, **request_overrides)).raise_for_status(); audio_download_url_can_be_visited = True
                if hasattr(resp, 'text') and audio_download_url_can_be_visited: break
            if not download_url_can_be_visited or not audio_download_url_can_be_visited: return []
            video_info.update(dict(download_url=download_url, ext=ext, audio_download_url=audio_download_url, audio_ext=audio_ext, default_download_headers=headers, default_audio_download_headers=headers))
            video_title = legalizestring(safeextractfromdict(raw_data, ['api', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}'), identifier=vid, cover_url=safeextractfromdict(raw_data, ['api', 'imagePreviewUrl'], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlwithytdown >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''_parsefromurlwithdownr'''
    def _parsefromurlwithdownr(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, vid = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), parse_qs(urlparse(url).query, keep_blank_values=True)['v'][0]
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "referer": "https://downr.org/"}
        # try parse
        try:
            cookies = requests.utils.dict_from_cookiejar(requests.get('https://downr.org/.netlify/functions/analytics', headers=headers, **request_overrides).cookies)
            (resp := requests.post('https://downr.org/.netlify/functions/nyt', headers=headers, cookies=cookies, json={"url": url}, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            video_medias: list[dict] = [item for item in raw_data['medias'] if item['type'] in ('video',)]
            video_medias: list[dict] = sorted(video_medias, key=lambda item: (item.get('height') * item.get('width'), item.get('bitrate')), reverse=True)
            audio_medias: list[dict] = [item for item in raw_data['medias'] if item['type'] in ('audio',)]
            audio_medias: list[dict] = sorted(audio_medias, key=lambda item: (item.get('bitrate'), float(item.get('audioSampleRate') or 0)), reverse=True)
            for video_media in video_medias:
                download_url, ext, download_url_can_be_visited = video_media['url'], video_media['ext'], False; (stream_headers := headers.copy()).update({"Range": "bytes=0-0"})
                with suppress(Exception): resp = None; (resp := requests.get(download_url, stream=True, headers=stream_headers, allow_redirects=True, verify=False, **request_overrides)).raise_for_status(); download_url_can_be_visited = True
                if hasattr(resp, 'text') and download_url_can_be_visited: break
            for audio_media in audio_medias:
                audio_download_url, audio_ext, audio_download_url_can_be_visited = audio_media['url'], audio_media['ext'], False; (stream_headers := headers.copy()).update({"Range": "bytes=0-0"})
                with suppress(Exception): resp = None; (resp := requests.get(audio_download_url, stream=True, headers=stream_headers, allow_redirects=True, verify=False, **request_overrides)).raise_for_status(); audio_download_url_can_be_visited = True
                if hasattr(resp, 'text') and audio_download_url_can_be_visited: break
            if not download_url_can_be_visited or not audio_download_url_can_be_visited: return []
            video_info.update(dict(download_url=download_url, ext=ext, audio_download_url=audio_download_url, audio_ext=audio_ext, default_download_headers=headers, default_audio_download_headers=headers))
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
        for parser in [self._parsefromurlwithytdown, self._parsefromurlwithdownr]:
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