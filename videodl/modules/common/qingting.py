'''
Function:
    Implementation of QingtingVideoClient: https://33tool.com/video_parse/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''QingtingVideoClient'''
class QingtingVideoClient(BaseVideoClient):
    source = 'QingtingVideoClient'
    def __init__(self, **kwargs):
        super(QingtingVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
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
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        video_infos = []
        try:
            # --get request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            if "douyin.com" in url: resp = self.get(f'https://api.33tool.com/api/parse/douyin?url={url}', headers=headers, **request_overrides)
            elif "bilibili.com" in url or "b23.tv" in url: resp = self.get(f'https://api.33tool.com/api/parse/bilibili?url={url}', headers=headers, **request_overrides)
            elif "xiaohongshu.com" in url or "xhslink.com" in url: resp = self.get(f'https://api.33tool.com/api/parse/redbook?url={url}', headers=headers, **request_overrides)
            elif "kuaishou.com" in url: resp = self.get(f'https://api.33tool.com/api/parse/kuaishou?url={url}', headers=headers, **request_overrides)
            else: raise NotImplementedError()
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data['data'].get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            download_url = raw_data['data']['videoUrl']
            video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos