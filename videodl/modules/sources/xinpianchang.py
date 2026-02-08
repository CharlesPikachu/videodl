'''
Function:
    Implementation of XinpianchangVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''XinpianchangVideoClient'''
class XinpianchangVideoClient(BaseVideoClient):
    source = 'XinpianchangVideoClient'
    def __init__(self, **kwargs):
        super(XinpianchangVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            "accept-encoding": "identity;q=1, *;q=0", "referer": "https://www.xinpianchang.com/", "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
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
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            resp = self.get(url, headers={'Referer': url}, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            tag = soup.find("script", id="__NEXT_DATA__")
            raw = tag.string if tag.string is not None else tag.get_text()
            raw_data = json_repair.loads(raw.strip())
            video_data = raw_data['props']['pageProps']['detail']['video']
            vid = video_data["vid"]
            resp = self.get(f"https://mod-api.xinpianchang.com/mod/api/v2/media/{vid}?appKey={video_data['appKey']}&extend=userInfo%2CuserStatus", **request_overrides)
            resp.raise_for_status()
            raw_data[f'media/{vid}'] = resp2json(resp=resp)
            for k, v in raw_data[f'media/{vid}']['data']['resource'].items():
                if k in ('dash', 'hls') and isinstance(v, dict): download_url = v.get('url'); break
                elif k in ('progressive',) and isinstance(v, list):
                    sorted_by_resolution = sorted(v, key=lambda x: (x.get('height', 0) * x.get('width', 0), x.get('filesize', 0)), reverse=True)
                    download_url = [item.get('url') or item.get('backupUrl') for item in sorted_by_resolution if item.get('url') or item.get('backupUrl')][0]
                    break
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data[f'media/{vid}'], ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(raw_data[f'media/{vid}'], ['data', 'cover'], None)))
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
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"xinpianchang.com"}
        return BaseVideoClient.belongto(url, valid_domains)