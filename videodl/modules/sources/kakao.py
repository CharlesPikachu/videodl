'''
Function:
    Implementation of KakaoVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, FileTypeSniffer, VideoInfo


'''KakaoVideoClient'''
class KakaoVideoClient(BaseVideoClient):
    source = 'KakaoVideoClient'
    def __init__(self, **kwargs):
        super(KakaoVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
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
        if not self.belongto(url=url): return [video_info]
        # try parse
        try:
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            params = {
                'player': 'monet_html5', 'referer': url, 'uuid': '', 'service': 'kakao_tv', 'section': '', 'dteType': 'PC',
                'fields': ','.join(['-*', 'tid', 'clipLink', 'displayTitle', 'clip', 'title', 'description', 'channelId', 'createTime', 'duration', 'playCount',
                                    'likeCount', 'commentCount', 'tagList', 'channel', 'name', 'clipChapterThumbnailList', 'thumbnailUrl', 'timeInSec', 'isDefault',
                                    'videoOutputList', 'width', 'height', 'kbps', 'profile', 'label']),
            }
            resp = self.get(f'http://tv.kakao.com/api/v1/ft/playmeta/cliplink/{vid}/', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            clip_link = raw_data['clipLink']
            clip = clip_link['clip']
            video_output_list = clip.get('videoOutputList') or []
            video_output_list = sorted(video_output_list, key=lambda s: (s["width"] * s["height"], s["kbps"]), reverse=True)
            for fmt in video_output_list:
                profile_name = fmt.get('profile')
                if not profile_name or profile_name == 'AUDIO': continue
                params.update({'profile': profile_name, 'fields': '-*,code,message,url'})
                download_url = ""
                try:
                    resp = self.get(f'https://tv.kakao.com/katz/v1/ft/cliplink/{vid}/readyNplay?', params=params, **request_overrides)
                    resp.raise_for_status()
                    fmt_raw_data = resp2json(resp=resp)
                    download_url = fmt_raw_data['videoLocation']['url']
                    raw_data['readyNplay'] = fmt_raw_data
                except:
                    continue
                if download_url: break
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                clip.get('title', f'{self.source}_null_{date_str}') or clip_link.get('displayTitle', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=vid,
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
            valid_domains = ["tv.kakao.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)