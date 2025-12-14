'''
Function:
    Implementation of QZXDPToolsVideoClient: https://tools.qzxdp.cn/video_spider
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
from datetime import datetime
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json


'''QZXDPToolsVideoClient'''
class QZXDPToolsVideoClient(BaseVideoClient):
    source = 'QZXDPToolsVideoClient'
    def __init__(self, **kwargs):
        super(QZXDPToolsVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "host": "tools.qzxdp.cn",
            "origin": "https://tools.qzxdp.cn",
            "referer": "https://tools.qzxdp.cn/video_spider",
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
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
            # --post request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.post(f'https://tools.qzxdp.cn/api/video_spider/query', data={'video_url': url}, headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = raw_data['data'].get('title') or f'{self.source}_null_{date_str}'
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            # --download url
            download_url = raw_data['data']['url']
            video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
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