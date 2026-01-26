'''
Function:
    Implementation of AnyFetcherVideoClient: https://anyfetcher.com/zh-cn
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
from ..utils import RandomIPGenerator
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, optionalimport


'''AnyFetcherVideoClient'''
class AnyFetcherVideoClient(BaseVideoClient):
    source = 'AnyFetcherVideoClient'
    def __init__(self, **kwargs):
        if ('enable_parse_curl_cffi' not in kwargs) and optionalimport('curl_cffi'): kwargs['enable_parse_curl_cffi'] = True
        super(AnyFetcherVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Content-Type": "application/json", "Origin": "https://anyfetcher.com", "Referer": "https://anyfetcher.com/zh-cn/",
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
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=True)
        null_backup_title = yieldtimerelatedtitle(self.source)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        # try parse
        video_infos = []
        try:
            # --post request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.post(f'https://anyfetcher.com/api/video/parse', headers=headers, json={"url": url}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --extract download url
            video_medias: list[dict] = [item for item in raw_data['medias'] if item['media_type'] in ('video',)]
            audio_medias: list[dict] = [item for item in raw_data['medias'] if item['media_type'] in ('audio',)]
            if video_medias: video_medias: dict = video_medias[0]
            if 'formats' in video_medias:
                formats = sorted(video_medias["formats"], key=lambda item, re=__import__("re"): tuple(int(m.group()) if (m := re.search(r"\d+", str(item.get(k)))) else 0 for k in ("quality", "video_size")), reverse=True)
                formats: list[dict] = [fmt for fmt in formats if fmt.get('video_url')]
                download_url, audio_download_url = formats[0].get('video_url'), formats[0].get('audio_url')
                if not audio_download_url and audio_medias: audio_download_url = audio_medias[0].get('resource_url') or audio_medias[0].get('preview_url')
            else:
                download_url = video_medias.get('resource_url') or video_medias.get('preview_url')
                audio_download_url = audio_medias[0].get('resource_url') or audio_medias[0].get('preview_url') if audio_medias else ""
            # --deal with special download urls
            download_url, is_converter_performed = self._convertspecialdownloadurl(download_url)
            if is_converter_performed: video_info.update(dict(enable_nm3u8dlre=True))
            video_info.update(dict(download_url=download_url))
            if audio_download_url and audio_download_url != 'NULL': video_info.update(dict(audio_download_url=audio_download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=raw_data.get('preview_url')
            ))
            if audio_download_url and audio_download_url != 'NULL':
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                video_info.update(dict(guess_audio_ext_result=guess_audio_ext_result))
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                if audio_ext in ['m4s']: audio_ext = 'm4a'
                video_info.update(dict(audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos