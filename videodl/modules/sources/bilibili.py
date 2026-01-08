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
from .base import BaseVideoClient
from urllib.parse import urlparse, parse_qs
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''BilibiliVideoClient'''
class BilibiliVideoClient(BaseVideoClient):
    source = 'BilibiliVideoClient'
    def __init__(self, **kwargs):
        super(BilibiliVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromcommonurl'''
    def _parsefromcommonurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/(?:video/|festival/[^/?#]+\?(?:[^#]*&)?bvid=)(?P<prefix>[aAbB][vV])(?P<id>[^/?#&]+)')
        m = pattern.match(url)
        video_id, prefix = m.group('id', 'prefix')
        # try parse
        video_infos = []
        try:
            parsed_url = urlparse(url)
            part_id = parse_qs(parsed_url.query, keep_blank_values=True).get('p', None)
            if part_id and isinstance(part_id, list): part_id = int(part_id[0]) if part_id and str(part_id[0]).lstrip("+-").isdigit() else None
            else: part_id = None
            if prefix.upper() in ['BV']:
                resp = self.get(f"https://api.bilibili.com/x/web-interface/view?bvid=BV{video_id}", **request_overrides)
                resp.raise_for_status()
                raw_data = resp2json(resp=resp)
            elif prefix.upper() in ['AV']:
                resp = self.get(f"https://api.bilibili.com/x/web-interface/view?aid={video_id}", **request_overrides)
                resp.raise_for_status()
                raw_data = resp2json(resp=resp)
                video_id = raw_data['data']['bvid']
            for page_idx, page in enumerate(raw_data['data']["pages"]):
                if part_id and page_idx + 1 != part_id: continue
                cid = page['cid']
                try:
                    resp = self.get(f"https://api.bilibili.com/x/player/playurl?otype=json&fnver=0&fnval=0&qn=80&bvid={video_id}&cid={cid}&platform=html5", **request_overrides)
                    resp.raise_for_status()
                except:
                    continue
                page_raw_data = resp2json(resp=resp)
                page_raw_data['x/web-interface/view'] = copy.deepcopy(raw_data)
                video_page_info = copy.deepcopy(video_info)
                video_page_info.update(dict(raw_data=page_raw_data))
                durl = page_raw_data['data']['durl']
                durl = [x for x in durl if x.get('url')]
                download_url = max(page_raw_data['data']['durl'], key=lambda x: x['size'])['url']
                video_page_info.update(dict(download_url=download_url))
                video_title = f"ep{len(video_infos)+1}-{page.get('part')}" if len(raw_data['data']["pages"]) > 1 else raw_data["data"].get('title')
                video_title = legalizestring(video_title or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']
                video_page_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f'{video_id}-{cid}'))
                video_infos.append(video_page_info)
        except Exception as err:
            err_msg = f'{self.source}._parsefromcommonurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_parsefrombangumiepurl'''
    def _parsefrombangumiepurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/bangumi/play/ep(?P<id>\d+)')
        episode_id = str(pattern.match(url).group('id'))
        # try parse
        video_infos = []
        try:
            resp = self.get('https://api.bilibili.com/pgc/view/web/season', params={'ep_id': episode_id}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            result_episodes = safeextractfromdict(raw_data, ['result', 'episodes'], [])
            for item in safeextractfromdict(raw_data, ['result', 'section'], []): result_episodes += item.get('episodes', [])
            for _, page in enumerate(result_episodes):
                if str(page['ep_id']) != episode_id: continue
                try:
                    resp = self.get(f"https://api.bilibili.com/pgc/player/web/v2/playurl?fnval=12240&ep_id={str(page['ep_id'])}", **request_overrides)
                    resp.raise_for_status()
                except:
                    continue
                page_raw_data = resp2json(resp=resp)
                page_raw_data['pgc/view/web/season'] = copy.deepcopy(raw_data)
                video_page_info, formats = copy.deepcopy(video_info), []
                video_page_info.update(dict(raw_data=page_raw_data))
                for item in page_raw_data['result']['video_info']['dash']['video']:
                    formats.append({'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0, 'width': item.get('width') or 0, 'height': item.get('height') or 0})
                formats: list[dict] = sorted(formats, key=lambda x: (x["width"]*x["height"], x["filesize"]), reverse=True)
                formats: list[dict] = [item for item in formats if item.get('url')]
                download_url = formats[0]['url']
                video_page_info.update(dict(download_url=download_url))
                video_title = page.get('share_copy') or page.get('show_title') or null_backup_title
                video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']
                video_page_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=episode_id))
                audio_formats = []
                for item in safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'dolby', 'audio'], []) + safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'audio'], []):
                    audio_formats.append({'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0})
                audio_formats: list[dict] = sorted(audio_formats, key=lambda x: x["filesize"], reverse=True)
                audio_formats: list[dict] = [item for item in audio_formats if item.get('url')]
                if len(audio_formats) == 0: video_infos.append(video_page_info); continue
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_formats[0]['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                if audio_ext in ['m4s']: audio_ext = 'm4a'
                video_page_info.update(dict(
                    audio_download_url=audio_formats[0]['url'], guess_audio_ext_result=guess_audio_ext_result, audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            err_msg = f'{self.source}._parsefrombangumiepurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_parsefrombangumissurl'''
    def _parsefrombangumissurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        pattern = re.compile(r'(?x)https?://(?:www\.)?bilibili\.com/bangumi/play/ss(?P<id>\d+)')
        ss_id = str(pattern.match(url).group('id'))
        # try parse
        video_infos = []
        try:
            resp = self.get('https://api.bilibili.com/pgc/web/season/section', params={'season_id': ss_id}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            result_episodes = safeextractfromdict(raw_data, ['result', 'main_section', 'episodes'], [])
            for item in safeextractfromdict(raw_data, ['result', 'section'], []): result_episodes += item.get('episodes', [])
            for _, page in enumerate(result_episodes):
                episode_id = page['id']
                try:
                    resp = self.get(f"https://api.bilibili.com/pgc/player/web/v2/playurl?fnval=12240&ep_id={episode_id}", **request_overrides)
                    resp.raise_for_status()
                except:
                    continue
                page_raw_data = resp2json(resp=resp)
                page_raw_data['pgc/web/season/section'] = copy.deepcopy(raw_data)
                video_page_info, formats = copy.deepcopy(video_info), []
                video_page_info.update(dict(raw_data=page_raw_data))
                if not safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'video'], []): continue
                for item in page_raw_data['result']['video_info']['dash']['video']:
                    formats.append({'url': item.get('baseUrl') or item.get('base_url'), 'filesize': item.get('size'), 'width': item.get('width'), 'height': item.get('height')})
                formats: list[dict] = sorted(formats, key=lambda x: (x["width"]*x["height"], x["filesize"]), reverse=True)
                formats: list[dict] = [item for item in formats if item.get('url')]
                download_url = formats[0]['url']
                video_page_info.update(dict(download_url=download_url))
                video_title = page.get('long_title') or page.get('title') or null_backup_title
                video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']
                video_page_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=episode_id))
                audio_formats = []
                for item in safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'dolby', 'audio'], []) + safeextractfromdict(page_raw_data, ['result', 'video_info', 'dash', 'audio'], []):
                    audio_formats.append({'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0})
                audio_formats: list[dict] = sorted(audio_formats, key=lambda x: x["filesize"], reverse=True)
                audio_formats: list[dict] = [item for item in audio_formats if item.get('url')]
                if len(audio_formats) == 0: video_infos.append(video_page_info); continue
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_formats[0]['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                if audio_ext in ['m4s']: audio_ext = 'm4a'
                video_page_info.update(dict(
                    audio_download_url=audio_formats[0]['url'], guess_audio_ext_result=guess_audio_ext_result, audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            err_msg = f'{self.source}._parsefrombangumissurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_parsefromcheeseepurl'''
    def _parsefromcheeseepurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/cheese/play/ep(?P<id>\d+)')
        episode_id = str(pattern.match(url).group('id'))
        # try parse
        video_infos = []
        try:
            resp = self.get(f"https://api.bilibili.com/pugv/view/web/season?ep_id={episode_id}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            for _, page in enumerate(raw_data['data']['episodes']):
                if str(page['id']) != episode_id: continue
                try:
                    resp = self.get('https://api.bilibili.com/pugv/player/web/playurl', params={'avid': page['aid'], 'cid': page['cid'], 'ep_id': episode_id, 'fnval': 16, 'fourk': 1}, **request_overrides)
                    resp.raise_for_status()
                except:
                    continue
                page_raw_data = resp2json(resp=resp)
                page_raw_data['pugv/view/web/season'] = copy.deepcopy(raw_data)
                video_page_info, formats = copy.deepcopy(video_info), []
                video_page_info.update(dict(raw_data=page_raw_data))
                for item in page_raw_data['data']['dash']['video']:
                    formats.append({'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0, 'width': item.get('width') or 0, 'height': item.get('height') or 0})
                formats: list[dict] = sorted(formats, key=lambda x: (x["width"]*x["height"], x["filesize"]), reverse=True)
                formats: list[dict] = [item for item in formats if item.get('url')]
                download_url = formats[0]['url']
                video_page_info.update(dict(download_url=download_url))
                video_title = page.get('title') or null_backup_title
                video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']
                video_page_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=episode_id))
                audio_formats = []
                for item in safeextractfromdict(page_raw_data, ['data', 'dash', 'audio'], []):
                    audio_formats.append({'url': item.get('baseUrl') or item.get('base_url') or item.get('url'), 'filesize': item.get('size') or 0})
                audio_formats: list[dict] = sorted(audio_formats, key=lambda x: x["filesize"], reverse=True)
                audio_formats: list[dict] = [item for item in audio_formats if item.get('url')]
                if len(audio_formats) == 0: video_infos.append(video_page_info); continue
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_formats[0]['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                if audio_ext in ['m4s']: audio_ext = 'm4a'
                video_page_info.update(dict(
                    audio_download_url=audio_formats[0]['url'], guess_audio_ext_result=guess_audio_ext_result, audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            err_msg = f'{self.source}._parsefromcheeseepurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''_getredirecturl'''
    def _getredirecturl(self, url: str, aid: str, request_overrides: dict = None):
        try:
            resp = self.get("https://api.bilibili.com/x/web-interface/view", params={"aid": aid}, **request_overrides)
            redirect_url = resp2json(resp=resp)['data']['redirect_url']
            redirect_url = self.get(redirect_url, allow_redirects=True, **request_overrides).url
            return redirect_url
        except:
            return url
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        try: url = self.get(url, allow_redirects=True, **request_overrides).url
        except: url = url
        # common url
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/(?:video/|festival/[^/?#]+\?(?:[^#]*&)?bvid=)(?P<prefix>[aAbB][vV])(?P<id>[^/?#&]+)')
        m = pattern.match(url)
        if m and (m.group('prefix').upper() in ('AV')): url = self._getredirecturl(url, m.group('id'), request_overrides)
        m = pattern.match(url)
        if m: video_id, prefix = m.group('id', 'prefix')
        if m and video_id and prefix: return self._parsefromcommonurl(url, request_overrides=request_overrides)
        # bangumi ep url
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/bangumi/play/ep(?P<id>\d+)')
        m = pattern.match(url)
        if m: episode_id = m.group('id')
        if m and episode_id: return self._parsefrombangumiepurl(url, request_overrides=request_overrides)
        # bangumi ss url
        pattern = re.compile(r'(?x)https?://(?:www\.)?bilibili\.com/bangumi/play/ss(?P<id>\d+)')
        m = pattern.match(url)
        if m: ss_id = m.group('id')
        if m and ss_id: return self._parsefrombangumissurl(url, request_overrides=request_overrides)
        # cheese ep url
        pattern = re.compile(r'https?://(?:www\.)?bilibili\.com/cheese/play/ep(?P<id>\d+)')
        m = pattern.match(url)
        if m: episode_id = m.group('id')
        if m and episode_id: return self._parsefromcheeseepurl(url, request_overrides=request_overrides)
        # not match all, fail to parse
        return [VideoInfo(source=self.source)]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.bilibili.com", "b23.tv"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)