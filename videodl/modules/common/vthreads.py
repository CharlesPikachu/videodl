'''
Function:
    Implementation VThreadsVideoClient: https://vthreads.top/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from urllib.parse import urljoin, quote
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, safeextractfromdict


'''VThreadsVideoClient'''
class VThreadsVideoClient(BaseVideoClient):
    source = 'VThreadsVideoClient'
    def __init__(self, **kwargs):
        super(VThreadsVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36", "referer": "https://vthreads.top/zh/"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36", "referer": "https://vthreads.top/zh/"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getdownloadurlfrommediainfo'''
    def _getdownloadurlfrommediainfo(self, media_info: dict, video_title: str, visitor_id: str, headers: dict, request_overrides: dict = None) -> str:
        request_overrides, download_url = request_overrides or {}, urljoin('https://vthreads.top/', media_info['url'])
        if media_info.get('format') in {'merge', 'audio'} or '.m3u8' in download_url.lower() or '/api/download_merge' in download_url:
            task_url = download_url if 'title=' in download_url else f'{download_url}{"&" if "?" in download_url else "?"}title={quote(video_title, safe="")}&vid={visitor_id}'
            (resp := self.get(task_url, headers=headers, **request_overrides)).raise_for_status()
            max_check_status_retry_times, time_interval_for_check_status, task_id = 20, 2, resp2json(resp=resp)['task_id']
            for _ in range(max_check_status_retry_times):
                (resp := self.get(f'https://vthreads.top/api/check_status/{task_id}', headers=headers, **request_overrides)).raise_for_status()
                if (status_data := resp2json(resp=resp)).get('download_url') and status_data.get('status') in {'SUCCESS'}: break
                if status_data.get('status') in {'FAILED'}: raise RuntimeError(status_data.get('error') or 'merge task failed')
                time.sleep(time_interval_for_check_status)
            return urljoin('https://vthreads.top/', resp2json(resp=resp)['download_url'])
        return download_url
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        request_overrides, null_backup_title, video_infos, visitor_id = request_overrides or {}, yieldtimerelatedtitle(self.source), [], f'{int(time.time() * 1000):032x}'[-32:]
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers=self.BILIBILI_REFERENCE_HEADERS, default_audio_download_headers=self.BILIBILI_REFERENCE_HEADERS))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers=self.WEIBO_REFERENCE_HEADERS, default_audio_download_headers=self.WEIBO_REFERENCE_HEADERS))
        # try parse
        try:
            # --get request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            (resp := self.get(f'https://vthreads.top/api/extract?url={quote(url, safe="")}&lang=zh&vid={visitor_id}', headers=headers, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp)), default_download_headers=self.default_download_headers))
            # --video title
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --extract download urls
            medias: list[dict] = safeextractfromdict(raw_data, ['data', 'medias'], []) or []
            audio_medias: list[dict] = [item for item in medias if item.get('format') in {'audio', 'm4a', 'mp3', 'aac', 'opus'} or item.get('media_type') in {'audio'} or 'audio' in str(item.get('quality', '')).lower()]
            merge_medias: list[dict] = [item for item in medias if item.get('format') in {'merge'} or '/api/download_merge' in str(item.get('url', ''))]
            video_medias: list[dict] = [item for item in medias if item not in audio_medias and item not in merge_medias]
            video_media = video_medias[0] if video_medias and audio_medias else merge_medias[0] if merge_medias else video_medias[0]
            audio_media = audio_medias[0] if video_medias and audio_medias else None
            video_info.update(dict(download_url=(download_url := self._getdownloadurlfrommediainfo(video_media, video_title, visitor_id, headers, request_overrides))))
            if audio_media: video_info.update(dict(audio_download_url=(audio_download_url := self._getdownloadurlfrommediainfo(audio_media, video_title, visitor_id, headers, request_overrides))))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            guess_video_ext_result['ext'] = 'avi' if video_media.get('format') in {'merge'} else guess_video_ext_result['ext']
            if (ext := guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']) in {'bin', 'm4s'}: ext = 'mp4'
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=safeextractfromdict(raw_data, ['data', 'thumbnail'], None)))
            if audio_media:
                video_info.update(dict(guess_audio_ext_result=(guess_audio_ext_result := FileTypeSniffer.getfileextensionfromurl(url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies))))
                if (audio_ext := guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']) in {'m4s', 'mp4'}: audio_ext = 'm4a'
                video_info.update(dict(audio_ext=audio_ext, audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos