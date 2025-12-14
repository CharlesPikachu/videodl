'''
Function:
    Implementation of GVVIPVideoClient: https://greenvideo.cc/video/vip
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
from datetime import datetime
from ..sources import BaseVideoClient
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json


'''GVVIPVideoClient'''
class GVVIPVideoClient(BaseVideoClient):
    source = 'GVVIPVideoClient'
    def __init__(self, **kwargs):
        super(GVVIPVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
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
        # try parse
        video_infos = []
        try:
            # --get request
            resp = self.get(f'https://greenvideo.cc/video-tool/movie/getRawDynamicPlayUrl?url={url}', **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = raw_data['data'].get('title') or f'{self.source}_null_{date_str}'
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            # --sort by success rate
            def _successrate(item):
                m = re.search(r"成功率:(\d+)%", item["label"])
                return int(m.group(1)) if m else 0
            play_list = raw_data["data"]["playList"]
            play_list = [pl for pl in play_list if '.html?' not in pl['url']]
            sorted_play_list = sorted(play_list, key=_successrate, reverse=True)
            download_url = sorted_play_list[0]['url']
            video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True,
                guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos