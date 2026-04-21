'''
Function:
    Implementation of PlayerPLVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
from pathlib import Path
from .base import BaseVideoClient
from ..utils.cmd import DownloadWithNM3U8DLRECommand
from ..utils import initcdm, closecdm, SearchPsshValueUtils
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, safeextractfromdict, taskprogress, VideoInfo


'''PlayerPLVideoClient'''
class PlayerPLVideoClient(BaseVideoClient):
    source = 'PlayerPLVideoClient'
    PLATFORM = "BROWSER"
    PLAYLIST_URL = 'https://player.pl/playerapi/item/{item_id}/playlist'
    TRANSLATE_URL = 'https://player.pl/playerapi/item/translate'
    SERIAL_URL = 'https://player.pl/playerapi/product/vod/serial/{show_id}'
    SEASONS_URL = 'https://player.pl/playerapi/product/vod/serial/{show_id}/season/list'
    EPISODES_URL = 'https://player.pl/playerapi/product/vod/serial/{show_id}/season/{season_id}/episode/list'
    CDM_WVD_FILE_PATH = Path(__file__).resolve().parents[2] / "modules" / "cdm" / "charlespikachu_playerpl.wvd"
    def __init__(self, **kwargs):
        super(PlayerPLVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlsinglevideo'''
    @useparseheaderscookies
    def _parsefromurlsinglevideo(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        clean_url = url.split("?")[0].split("#")[0].rstrip("/")
        if not self.belongto(url=url) or (("/filmy-online" not in clean_url) and (not re.findall(r',S\d+E\d+,\d+$', clean_url.split("/")[-1]))): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source, ext='mp4', download_with_ffmpeg=True, enable_nm3u8dlre=True), yieldtimerelatedtitle(self.source), []
        # try parse
        try:
            # --basic information
            vid, item_type, item_key = clean_url.split(",")[-1], "MOVIE", "articleId"
            (resp := self.get(PlayerPLVideoClient.TRANSLATE_URL, params={item_key: vid, 'platform': PlayerPLVideoClient.PLATFORM}, **request_overrides)).raise_for_status()
            (resp := self.get(PlayerPLVideoClient.PLAYLIST_URL.format(item_id=(item_id := (raw_data := resp2json(resp=resp))['id'])), params={'type': item_type, 'platform': PlayerPLVideoClient.PLATFORM}, **request_overrides)).raise_for_status()
            raw_data['play_details'] = resp2json(resp=resp); content_info = safeextractfromdict(raw_data['play_details'], ['movie', 'info'], {}) or {}; nl_data = safeextractfromdict(raw_data['play_details'], ['movie', 'stats', 'nl_data'], {}) or {}
            # --video title
            series_title = content_info.get('series_title') or nl_data.get('program'); video_title = " - ".join(dict.fromkeys(filter(None, [series_title, nl_data.get('title')])))
            video_title = legalizestring(video_title or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --solve drm
            if (drm_info := safeextractfromdict(raw_data['play_details'], ['movie', 'video', 'protections'], {})):
                license_url, manifest_url = safeextractfromdict(drm_info, ['widevine', 'src'], None), safeextractfromdict(raw_data['play_details'], ['movie', 'video', 'sources', 'dash', 'url'], '')
                pssh_value = SearchPsshValueUtils.getpsshfromdefaultkid((manifest_content := self.get(manifest_url, **request_overrides).content.decode()), xml_node="default_KID")
                if pssh_value is None: pssh_value = SearchPsshValueUtils.getpsshfromcencpssh(manifest_content)
                if pssh_value is None: pssh_value = SearchPsshValueUtils.getpsshfromplayready(manifest_content)
                if pssh_value is None: manifest_url = raw_data['play_details']["movie"]["video"]["sources"]["smooth"]["url"]; manifest_content = self.get(manifest_url, **request_overrides).content.decode(); pssh_value = SearchPsshValueUtils.getpsshfromplayready(manifest_content)
            else:
                license_url, pssh_value, manifest_url = None, None, None; sources: dict = raw_data['play_details']["movie"]["video"]["sources"]
                any(isinstance(v, dict) and (manifest_url := v.get('url')) for _, v in sources.items())
            raw_data['drm_details'], key = {'license_url': license_url, 'manifest_url': manifest_url, 'pssh_value': pssh_value}, None
            if pssh_value and license_url: 
                cdm, cdm_session_id, challenge = initcdm(pssh_value, PlayerPLVideoClient.CDM_WVD_FILE_PATH)
                (licence_resp := self.post(license_url, data=challenge, **request_overrides)).raise_for_status()
                raw_data['LICENSE_URL_RESPONSE'] = licence_resp.content; video_info.update(dict(raw_data=raw_data))
                key = list(set(closecdm(cdm, cdm_session_id, licence_resp.content)))[0]
            video_info.update(dict(download_url=manifest_url, nm3u8dlre_settings=DownloadWithNM3U8DLRECommand.addkeyafterretry(key_value=key)))
            cover_url = safeextractfromdict(raw_data, ['play_details', 'movie', 'info', 'media', 'thumbnail_big'], None) or safeextractfromdict(raw_data, ['play_details', 'movie', 'info', 'media', 'poster'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info.ext}'), identifier=item_id, cover_url=cover_url)); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlsinglevideo >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        if not self.belongto(url=url): return []
        clean_url, request_overrides, video_infos = url.split("?")[0].split("#")[0].rstrip("/"), request_overrides or {}, []
        if (("/filmy-online" not in clean_url) and (not re.findall(r',S\d+E\d+,\d+$', clean_url.split("/")[-1]))):
            (resp := self.get(PlayerPLVideoClient.TRANSLATE_URL, params={'programId': clean_url.split(",")[-1], 'platform': PlayerPLVideoClient.PLATFORM}, **request_overrides)).raise_for_status()
            (resp := self.get(PlayerPLVideoClient.SERIAL_URL.format(show_id=(content_id := resp2json(resp=resp)['id'])), params={'platform': PlayerPLVideoClient.PLATFORM}, **request_overrides)).raise_for_status(); raw_data = resp2json(resp=resp)
            (resp := self.get(PlayerPLVideoClient.SEASONS_URL.format(show_id=content_id), params={'platform': PlayerPLVideoClient.PLATFORM}, **request_overrides)).raise_for_status(); raw_data['SEASONS_URL_RESPONSE'] = resp2json(resp=resp)
            with taskprogress(description='Possible Multiple Seasons Detected >>> Parsing One by One', total=len((seasons := sorted(resp2json(resp=resp), key=lambda s: s["number"])))) as progress_season:
                for season_idx, season in enumerate(seasons):
                    (resp := self.get(PlayerPLVideoClient.EPISODES_URL.format(show_id=content_id, season_id=season["id"]), params={'platform': PlayerPLVideoClient.PLATFORM}, **request_overrides)).raise_for_status()
                    with taskprogress(description=f'Possible Multiple Videos in Season {season_idx+1} Detected >>> Parsing One by One', total=len((episodes := sorted(resp2json(resp=resp), key=lambda e: e["episode"])))) as progress_eps:
                        for episode_idx, episode in enumerate(episodes):
                            (raw_data_eps := copy.deepcopy(raw_data)).update({'EPISODE_DETAILS': episode})
                            video_info_eps = self._parsefromurlsinglevideo(episode["shareUrl"], request_overrides=request_overrides)
                            if any((not info.with_valid_download_url) for info in (video_info_eps or [])): progress_eps.advance(1); continue
                            video_info_eps[0].raw_data['ROOT'] = raw_data_eps; video_info_eps[0].title = f"S{season_idx+1}E{episode_idx+1} {video_info_eps[0].title}"
                            video_info_eps[0].save_path = os.path.join(self.work_dir, self.source, f'{video_info_eps[0].title}.{video_info_eps[0].ext}'); video_infos.extend(video_info_eps); progress_eps.advance(1)
                    progress_season.advance(1)
        else:
            video_infos = self._parsefromurlsinglevideo(url=url, request_overrides=request_overrides)
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"player.pl"}
        return BaseVideoClient.belongto(url, valid_domains)