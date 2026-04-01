'''
Function:
    Implementation of CCCVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, FileTypeSniffer, VideoInfo


'''CCCVideoClient'''
class CCCVideoClient(BaseVideoClient):
    source = 'CCCVideoClient'
    def __init__(self, **kwargs):
        super(CCCVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlsinglevideo'''
    def _parsefromurlsinglevideo(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        single_video_pattern = re.compile(r'https?://(?:www\.)?media\.ccc\.de/v/(?P<id>[^/?#&]+)')
        isvideo_func = lambda rec: isinstance(rec.get("mime_type"), str) and rec["mime_type"].startswith("video/")
        # try parse
        try:
            display_id = single_video_pattern.match(url).group('id')
            (resp := self.get(url, **request_overrides)).raise_for_status()
            event_id = re.search(r"\bdata-id\s*=\s*(['\"])(\d+)\1", resp.text, flags=re.IGNORECASE).group(2)
            (resp := self.get(f'https://media.ccc.de/public/events/{event_id}', **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp))))
            video_title = legalizestring(raw_data.get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            fmt_rank = lambda rec: {"video/mp4": 2, "video/webm": 1}.get(rec.get("mime_type", ""), 0)
            quality_key = lambda rec: ((1 if rec.get("high_quality") else 0), ((rec.get("width") or 0) * (rec.get("height") or 0)), (rec.get("width") or 0), (rec.get("height") or 0), fmt_rank(rec))
            videos = [r for r in raw_data["recordings"] if isvideo_func(r)]; videos_sorted = sorted(videos, key=quality_key, reverse=True)
            video_info.update(dict(download_url=videos_sorted[0]['recording_url']))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=videos_sorted[0]['recording_url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f'{display_id}-{event_id}', cover_url=raw_data.get('poster_url')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlsinglevideo >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, video_infos = request_overrides or {}, VideoInfo(source=self.source), []
        # play list or single video match
        m = re.compile(r'https?://(?:www\.)?media\.ccc\.de/c/(?P<id>[^/?#&]+)').match(url)
        # try parse
        if not m: return self._parsefromurlsinglevideo(url, request_overrides=request_overrides)
        try:
            (resp := self.get('https://media.ccc.de/public/conferences/' + m.group('id'), **request_overrides)).raise_for_status()
            for event in resp2json(resp=resp)['events']:
                if not isinstance(event, dict) or not event.get('frontend_link'): continue
                if not (video_info := self._parsefromurlsinglevideo(event['frontend_link'], request_overrides=request_overrides)): continue
                if ((video_info := video_info[0]).get("download_url") or "").upper() in ("", "NULL", "None"): continue
                video_info.update(dict(title=f"ep{len(video_infos)+1}-{video_info.title}", save_path=os.path.join(self.work_dir, self.source, f'ep{len(video_infos)+1}-{video_info.title}.{video_info.ext}'))); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"media.ccc.de"}
        return BaseVideoClient.belongto(url, valid_domains)