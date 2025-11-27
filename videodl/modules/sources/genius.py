'''
Function:
    Implementation of GeniusVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import time
import json_repair
from datetime import datetime
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, searchdictbykey, FileTypeSniffer, BrightcoveSmuggler, VideoInfo


'''GeniusVideoClient'''
class GeniusVideoClient(BaseVideoClient):
    source = 'GeniusVideoClient'
    def __init__(self, **kwargs):
        super(GeniusVideoClient, self).__init__(**kwargs)
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
            m = re.compile(r'https?://(?:www\.)?genius\.com/(?:videos|(?P<article>a))/(?P<id>[^?/#]+)').match(url)
            video_title = m.group("id")
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            m = re.search(r'["\']brightcove_video_id["\']\s*[:,]\s*(?:\[\s*)?["\'](\d{6,})["\']', resp.text, flags=re.DOTALL)
            if not m: m = re.search(r'"provider"\s*:\s*"brightcove"[^}]*?"provider_id"\s*:\s*"(\d{6,})"', resp.text, flags=re.DOTALL)
            if not m: m = re.search(r'brightcove_video_id[^0-9]+(\d{6,})', resp.text, flags=re.DOTALL)
            video_id = m.group(1)
            pattern = r"var\s+APP_CONFIG\s*=\s*JSON\.parse\('(?P<json>.*?)'\);"
            m = re.search(pattern, resp.text, re.DOTALL)
            app_config = m.group("json")
            app_config = bytes(app_config, "utf-8").decode("unicode_escape")
            app_config = json_repair.loads(app_config)
            account_id = app_config.get('brightcove_account_id', '4863540648001')
            keys = ["brightcove_standard_web_player_id", "brightcove_standard_no_autoplay_web_player_id", "brightcove_modal_web_player_id", "brightcove_song_story_web_player_id"]
            for key in keys:
                player_id = searchdictbykey(app_config, key)
                if player_id: break
            player_id = player_id[0] if player_id else "S1ZcmcOC1x"
            player_url = f"https://players.brightcove.net/{account_id}/{player_id}_default/index.html?videoId={video_id}"
            player_url = BrightcoveSmuggler.smuggleurl(player_url, {'referrer': url})
            request_overrides = copy.deepcopy(request_overrides)
            if 'headers' not in request_overrides: request_overrides['headers'] = copy.deepcopy(self.default_headers)
            if 'cookies' not in request_overrides: request_overrides['cookies'] = copy.deepcopy(self.default_cookies)
            raw_data = BrightcoveSmuggler.extract(player_url=player_url, request_overrides=request_overrides)
            video_info.update(dict(raw_data=raw_data))
            download_url = raw_data['formats'][0]['url']
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=video_id,
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
            valid_domains = ["genius.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)