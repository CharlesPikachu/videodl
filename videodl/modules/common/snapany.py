'''
Function:
    Implementation of SnapAnyVideoClient: https://snapany.com/zh
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import copy
import base64
import hashlib
from datetime import datetime
from urllib.parse import urlparse
from .kedou import KedouVideoClient
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, touchdir


'''constants'''
SALT = '6HTugjCXxR'


'''SnapAnyVideoClient'''
class SnapAnyVideoClient(KedouVideoClient):
    source = 'SnapAnyVideoClient'
    def __init__(self, **kwargs):
        super(SnapAnyVideoClient, self).__init__(**kwargs)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        # try parse
        video_infos = []
        try:
            # --encrypt post data
            site = urlparse(url).netloc.split('.')[-2]
            timestamp = str(int(time.time() * 1000))
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            headers['G-Footer'] = hashlib.md5(f"{url}{site}{timestamp}{SALT}".encode('utf-8')).hexdigest()
            headers['G-Timestamp'] = timestamp
            headers['Accept-Language'] = site
            # --post request
            resp = self.post('https://api.snapany.com/v1/extract', json={"link": url}, headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = raw_data.get('text', f'{self.source}_null_{date_str}')
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            # --sort by quality
            pattern = re.compile(r'data:[^;]+;base64,([A-Za-z0-9+/=]+)')
            try:
                formats = raw_data["medias"][0]['formats']
                video_items = [
                    x for x in formats if "video_url" in x and (x["video_url"].startswith('http') or (pattern.match(x["video_url"])))
                ]
                video_items_sorted = sorted(video_items, key=lambda item: item.get("video_size", 0) or 0, reverse=True)
                download_url, audio_download_url = video_items_sorted[0]['video_url'], video_items_sorted[0].get('audio_url')
            except:
                download_url = raw_data["medias"][0].get('resource_url') or raw_data["medias"][0].get('preview_url')
                audio_download_url = 'NULL'
            m = pattern.match(download_url)
            if m:
                download_url = base64.b64decode(m.group(1)).decode("utf-8", errors="ignore")
                if download_url.startswith('#EXTM3U'):
                    touchdir(os.path.join(self.work_dir, self.source))
                    with open(os.path.join(self.work_dir, self.source, f'{video_title}.m3u8'), 'w') as fp:
                        fp.write(download_url)
                    download_url = os.path.join(self.work_dir, self.source, f'{video_title}.m3u8')
                    video_info.update(dict(enable_nm3u8dlre=True))
            video_info.update(dict(download_url=download_url))
            if audio_download_url and audio_download_url != 'NULL': video_info.update(dict(audio_download_url=audio_download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=download_url,
            ))
            if audio_download_url and audio_download_url != 'NULL':
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                video_info.update(dict(guess_audio_ext_result=guess_audio_ext_result))
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                video_info.update(dict(audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}_audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos