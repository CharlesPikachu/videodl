'''
Function:
    Implementation of BilibiliVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
from contextlib import suppress
from .base import BaseVideoClient
from urllib.parse import urlparse, parse_qs
from ..utils.domains import BILIBILI_SUFFIXES
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, taskprogress, FileTypeSniffer, VideoInfo


'''BilibiliVideoClient'''
class BilibiliVideoClient(BaseVideoClient):
    source = 'BilibiliVideoClient'
    def __init__(self, **kwargs):
        super(BilibiliVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/',}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/',}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromcommonurl'''
    def _parsefromcommonurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        video_id, prefix = re.compile(r'https?://(?:www\.)?bilibili\.com/(?:video/|festival/[^/?#]+\?(?:[^#]*&)?bvid=)(?P<prefix>[aAbB][vV])(?P<id>[^/?#&]+)').match(url).group('id', 'prefix')
        # try parse
        try:
            part_id = int(part_id[0]) if (part_id := parse_qs(urlparse(url).query, keep_blank_values=True).get('p', None)) and isinstance(part_id, list) and str(part_id[0]).lstrip("+-").isdigit() else None
            if prefix.upper() in ['BV']: (resp := self.get(f"https://api.bilibili.com/x/web-interface/view?bvid=BV{video_id}", **request_overrides)).raise_for_status(); raw_data = resp2json(resp=resp)
            elif prefix.upper() in ['AV']: (resp := self.get(f"https://api.bilibili.com/x/web-interface/view?aid={video_id}", **request_overrides)).raise_for_status(); video_id = (raw_data := resp2json(resp=resp))['data']['bvid']
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len((extracted_video_items := raw_data['data']["pages"]))) as progress:
                for video_idx, extracted_video_item in enumerate(extracted_video_items):
                    if (part_id and video_idx + 1 != part_id) or (not isinstance(extracted_video_item, dict)): progress.advance(1); continue
                    with suppress(Exception): resp = None; (resp := self.get(f"https://api.bilibili.com/x/player/playurl?otype=json&fnver=0&fnval=0&qn=80&bvid={video_id}&cid={extracted_video_item['cid']}&platform=html5", **request_overrides)).raise_for_status()
                    if not locals().get('resp') or not hasattr(locals().get('resp'), 'text'): progress.advance(1); continue
                    (page_raw_data := resp2json(resp=resp))['x/web-interface/view'] = copy.deepcopy(raw_data)
                    (video_page_info := copy.deepcopy(video_info)).update(dict(raw_data=page_raw_data, download_url=(download_url := max(page_raw_data['data']['durl'], key=lambda x: x['size'])['url'])))
                    video_title = legalizestring((f"EP{len(video_infos)+1}-{extracted_video_item.get('part')}" if len(raw_data['data']["pages"]) > 1 else safeextractfromdict(raw_data, ['data', 'title'], None)) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (ext := guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']) in {'m4s'}: ext = 'mp4'
                    video_page_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f"{video_id}-{extracted_video_item['cid']}", cover_url=safeextractfromdict(extracted_video_item, ['first_frame'], None) or safeextractfromdict(page_raw_data['x/web-interface/view'], ['data', 'pic'], None))); video_infos.append(video_page_info); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromcommonurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_parsefrombangumiepurl'''
    def _parsefrombangumiepurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        episode_id = str(re.compile(r'https?://(?:www\.)?bilibili\.com/bangumi/play/ep(?P<id>\d+)').match(url).group('id'))
        # try parse
        try:
            (resp := self.get('https://api.bilibili.com/pgc/view/web/season', params={'ep_id': episode_id}, **request_overrides)).raise_for_status()
            result_episodes = safeextractfromdict((raw_data := resp2json(resp=resp)), ['result', 'episodes'], [])
            result_episodes += [ep for item in safeextractfromdict(raw_data, ['result', 'section'], []) for ep in dict(item).get('episodes', [])]
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len(result_episodes)) as progress:
                for _, result_episode in enumerate(result_episodes):
                    if (not isinstance(result_episode, dict)) or (str(result_episode['ep_id']) != episode_id): progress.advance(1); continue
                    with suppress(Exception): resp = None; (resp := self.get(f"https://api.bilibili.com/pgc/player/web/v2/playurl?fnval=12240&ep_id={str(result_episode['ep_id'])}", **request_overrides)).raise_for_status()
                    if not locals().get('resp') or not hasattr(locals().get('resp'), 'text'): progress.advance(1); continue
                    (page_raw_data := resp2json(resp=resp))['pgc/view/web/season'] = copy.deepcopy(raw_data)
                    (video_page_info := copy.deepcopy(video_info)).update(dict(raw_data=page_raw_data))
                    formats = [{'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0, 'width': item.get('width') or 0, 'height': item.get('height') or 0} for item in page_raw_data['result']['video_info']['dash']['video'] if isinstance(item, dict)]
                    formats: list[dict] = [item for item in sorted(formats, key=lambda x: (x["width"]*x["height"], x["filesize"]), reverse=True) if item.get('url')]
                    video_page_info.update(dict(download_url=(download_url := formats[0]['url'])))
                    video_title = legalizestring(result_episode.get('share_copy') or result_episode.get('show_title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (ext := guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']) in ['m4s']: ext = 'mp4'
                    video_page_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=episode_id, cover_url=safeextractfromdict(result_episode, ['cover'], None)))
                    audio_formats = [{'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0} for item in (safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'dolby', 'audio'], []) + safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'audio'], [])) if isinstance(item, dict)]
                    audio_formats: list[dict] = [item for item in sorted(audio_formats, key=lambda x: x["filesize"], reverse=True) if item.get('url')]
                    if len(audio_formats) == 0: video_infos.append(video_page_info); progress.advance(1); continue
                    guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(url=audio_formats[0]['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (audio_ext := guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info.audio_ext) in ['m4s']: audio_ext = 'm4a'
                    video_page_info.update(dict(audio_download_url=audio_formats[0]['url'], guess_audio_ext_result=guess_audio_ext_result, audio_ext=audio_ext, audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}'))); video_infos.append(video_page_info); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefrombangumiepurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_parsefrombangumissurl'''
    def _parsefrombangumissurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        ss_id = str(re.compile(r'(?x)https?://(?:www\.)?bilibili\.com/bangumi/play/ss(?P<id>\d+)').match(url).group('id'))
        # try parse
        try:
            (resp := self.get('https://api.bilibili.com/pgc/web/season/section', params={'season_id': ss_id}, **request_overrides)).raise_for_status()
            result_episodes: list[dict] = safeextractfromdict((raw_data := resp2json(resp=resp)), ['result', 'main_section', 'episodes'], [])
            result_episodes += [ep for item in safeextractfromdict(raw_data, ['result', 'section'], []) if isinstance(item, dict) for ep in item.get('episodes', [])]
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len(result_episodes)) as progress:
                for _, result_episode in enumerate(result_episodes):
                    with suppress(Exception): resp = None; (resp := self.get(f"https://api.bilibili.com/pgc/player/web/v2/playurl?fnval=12240&ep_id={result_episode['id']}", **request_overrides)).raise_for_status()
                    if not locals().get('resp') or not hasattr(locals().get('resp'), 'text'): progress.advance(1); continue
                    (page_raw_data := resp2json(resp=resp))['pgc/web/season/section'] = copy.deepcopy(raw_data)
                    if not safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'video'], []): progress.advance(1); continue
                    (video_page_info := copy.deepcopy(video_info)).update(dict(raw_data=page_raw_data))
                    formats = [{'url': item.get('baseUrl') or item.get('base_url'), 'filesize': item.get('size'), 'width': item.get('width'), 'height': item.get('height')} for item in page_raw_data['result']['video_info']['dash']['video'] if isinstance(item, dict)]
                    formats: list[dict] = [item for item in sorted(formats, key=lambda x: (x["width"]*x["height"], x["filesize"]), reverse=True) if item.get('url')]
                    video_page_info.update(dict(download_url=(download_url := formats[0]['url'])))
                    video_title = legalizestring(result_episode.get('long_title') or result_episode.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (ext := guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']) in ['m4s']: ext = 'mp4'
                    video_page_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=result_episode['id'], cover_url=safeextractfromdict(result_episode, ['cover'], None)))
                    audio_formats = [{'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0} for item in (safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'dolby', 'audio'], []) + safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'audio'], [])) if isinstance(item, dict)]
                    audio_formats: list[dict] = [item for item in sorted(audio_formats, key=lambda x: x["filesize"], reverse=True) if item.get('url')]
                    if len(audio_formats) == 0: video_infos.append(video_page_info); progress.advance(1); continue
                    guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(url=audio_formats[0]['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (audio_ext := guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info.audio_ext) in ['m4s']: audio_ext = 'm4a'
                    video_page_info.update(dict(audio_download_url=audio_formats[0]['url'], guess_audio_ext_result=guess_audio_ext_result, audio_ext=audio_ext, audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}'))); video_infos.append(video_page_info); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefrombangumissurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_parsefromcheeseepurl'''
    def _parsefromcheeseepurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        episode_id = str(re.compile(r'https?://(?:www\.)?bilibili\.com/cheese/play/ep(?P<id>\d+)').match(url).group('id'))
        # try parse
        try:
            (resp := self.get(f"https://api.bilibili.com/pugv/view/web/season?ep_id={episode_id}", **request_overrides)).raise_for_status()
            result_episodes = (raw_data := resp2json(resp=resp))['data']['episodes']
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len(result_episodes)) as progress:
                for _, result_episode in enumerate(result_episodes):
                    if (not isinstance(result_episode, dict)) or (str(result_episode['id']) != episode_id): progress.advance(1); continue
                    with suppress(Exception): resp = None; (resp := self.get('https://api.bilibili.com/pugv/player/web/playurl', params={'avid': result_episode['aid'], 'cid': result_episode['cid'], 'ep_id': episode_id, 'fnval': 16, 'fourk': 1}, **request_overrides)).raise_for_status()
                    if not locals().get('resp') or not hasattr(locals().get('resp'), 'text'): progress.advance(1); continue
                    (page_raw_data := resp2json(resp=resp))['pugv/view/web/season'] = copy.deepcopy(raw_data)
                    (video_page_info := copy.deepcopy(video_info)).update(dict(raw_data=page_raw_data))
                    formats = [{'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0, 'width': item.get('width') or 0, 'height': item.get('height') or 0} for item in page_raw_data['data']['dash']['video'] if isinstance(item, dict)]
                    formats: list[dict] = [item for item in sorted(formats, key=lambda x: (x["width"]*x["height"], x["filesize"]), reverse=True) if item.get('url')]
                    video_page_info.update(dict(download_url=(download_url := formats[0]['url'])))
                    video_title = legalizestring(result_episode.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (ext := guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']) in ['m4s']: ext = 'mp4'
                    video_page_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=episode_id, cover_url=safeextractfromdict(result_episode, ['cover'], None)))
                    audio_formats = [{'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0} for item in safeextractfromdict(page_raw_data, ['data', 'dash', 'audio'], []) if isinstance(item, dict)]
                    audio_formats: list[dict] = [item for item in sorted(audio_formats, key=lambda x: x["filesize"], reverse=True) if item.get('url')]
                    if len(audio_formats) == 0: video_infos.append(video_page_info); progress.advance(1); continue
                    guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(url=audio_formats[0]['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    if (audio_ext := guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info.audio_ext) in ['m4s']: audio_ext = 'm4a'
                    video_page_info.update(dict(audio_download_url=audio_formats[0]['url'], guess_audio_ext_result=guess_audio_ext_result, audio_ext=audio_ext, audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}'))); video_infos.append(video_page_info); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromcheeseepurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_getredirecturl'''
    def _getredirecturl(self, url: str, aid: str, request_overrides: dict = None):
        with suppress(Exception): (resp := self.get("https://api.bilibili.com/x/web-interface/view", params={"aid": aid}, **request_overrides)).raise_for_status(); return self.get(resp2json(resp=resp)['data']['redirect_url'], allow_redirects=True, **request_overrides).url
        return url
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        if not self.belongto(url=url): return []
        with suppress(Exception): url = self.get(url, allow_redirects=True, **request_overrides).url
        # common url
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/(?:video/|festival/[^/?#]+\?(?:[^#]*&)?bvid=)(?P<prefix>[aAbB][vV])(?P<id>[^/?#&]+)')
        if (m := pattern.match(url)) and (m.group('prefix').upper() in ('AV')): url = self._getredirecturl(url, m.group('id'), request_overrides)
        if (m := pattern.match(url)): video_id, prefix = m.group('id', 'prefix')
        if m and video_id and prefix: return self._parsefromcommonurl(url, request_overrides=request_overrides)
        # bangumi ep url
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/bangumi/play/ep(?P<id>\d+)')
        if (m := pattern.match(url)): episode_id = m.group('id')
        if m and episode_id: return self._parsefrombangumiepurl(url, request_overrides=request_overrides)
        # bangumi ss url
        pattern = re.compile(r'(?x)https?://(?:www\.)?bilibili\.com/bangumi/play/ss(?P<id>\d+)')
        if (m := pattern.match(url)): ss_id = m.group('id')
        if m and ss_id: return self._parsefrombangumissurl(url, request_overrides=request_overrides)
        # cheese ep url
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/cheese/play/ep(?P<id>\d+)')
        if (m := pattern.match(url)): episode_id = m.group('id')
        if m and episode_id: return self._parsefromcheeseepurl(url, request_overrides=request_overrides)
        # not match all, fail to parse
        return [VideoInfo(source=self.source)]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | BILIBILI_SUFFIXES
        return BaseVideoClient.belongto(url, valid_domains)