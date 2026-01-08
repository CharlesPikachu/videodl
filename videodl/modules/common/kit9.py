'''
Function:
    Implementation of KIT9VideoClient: https://apis.kit9.cn/api/aggregate_videos/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''KIT9VideoClient'''
class KIT9VideoClient(BaseVideoClient):
    source = 'KIT9VideoClient'
    def __init__(self, **kwargs):
        super(KIT9VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
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
            resp = self.get(f'https://apis.kit9.cn/api/aggregate_videos/api.php?link={url}', headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data['data'].get('video_title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            video_link = raw_data['data']['video_link']
            if isinstance(video_link, dict):
                video_link = dict(sorted(video_link.items(), key=lambda kv: (int((re.search(r'(\d{3,4})(?=\s*p\b)', str(kv[0]).lower()) or re.search(r'(\d{3,4})', str(kv[0])) or re.search(r'(.*)', '0')).group(1)) if re.search(r'(\d{3,4})(?=\s*p\b)|(\d{3,4})', str(kv[0]).lower()) else -1, str(kv[0]))))
                video_info.update(dict(download_url=list(video_link.values())[-1]))
            else:
                video_info.update(dict(download_url=video_link))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
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