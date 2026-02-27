'''
Function:
    Implementation of WittyTVVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from pathlib import Path
from contextlib import suppress
from .base import BaseVideoClient
from ..utils import initcdm, closecdm
from urllib.parse import urlparse, urlencode, urlunparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, VideoInfo


'''WittyTVVideoClient'''
class WittyTVVideoClient(BaseVideoClient):
    source = 'WittyTVVideoClient'
    BEARER_TOKEN = None
    RES_PRIORITY = ["hd", "hr", "sd"]
    CDM_WVD_FILE_PATH = Path(__file__).resolve().parents[2] / "modules" / "cdm" / "charlespikachu_wittytv.wvd"
    MEDIASET_URL = 'https://mediasetinfinity.mediaset.it'
    ACCOUNT_URL = "http://access.auth.theplatform.com/data/Account/{a_id}"
    PLAYBACK_URL = 'https://api-ott-prod-fe.mediaset.net/PROD/play/playback/check/v2.0'
    LOGIN_URL = "https://api-ott-prod-fe.mediaset.net/PROD/play/idm/anonymous/login/v2.0"
    LICENSE_URL = 'https://widevine.entitlement.theplatform.eu/wv/web/ModularDrm/getRawWidevineLicense'
    PROGRAM_URL = 'https://feed.entertainment.tv.theplatform.eu/f/-/mediaset-prod-ext-programs-v2/guid/-/{guid}'
    QUERY_URL = 'https://www.wittytv.it/wp-admin/admin-ajax.php?action=load_more&query[category_name]={category_name}&query[trasmissioni]={broadcast}&query[paged]={page}'
    def __init__(self, **kwargs):
        super(WittyTVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getbearertoken'''
    def _getbearertoken(self, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        resp = self.post(WittyTVVideoClient.LOGIN_URL, json={'client_id': 'client_id', 'appName': 'embed//mediasetplay-embed'}, **request_overrides)
        resp.raise_for_status()
        device_id = resp2json(resp=resp)["response"]["beToken"]
        return device_id
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, ext='mp4', download_with_ffmpeg=True, enable_nm3u8dlre=True)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        if self.BEARER_TOKEN is None: self.BEARER_TOKEN = self._getbearertoken()
        # try parse
        video_infos = []
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            content_id, raw_data = re.search(r'guIDcurrentGlobal\s*=\s*"([^"]+)"', resp.text).group(1), {}
            resp = self.get(WittyTVVideoClient.PROGRAM_URL.format(guid=content_id), **request_overrides)
            resp.raise_for_status()
            raw_data['PROGRAM_URL_RESPONSE'] = resp2json(resp=resp)
            program = raw_data['PROGRAM_URL_RESPONSE'].get("mediasetprogram$brandTitle", None) or raw_data['PROGRAM_URL_RESPONSE'].get("mediasetprogram$auditelBrandName", None) or raw_data['PROGRAM_URL_RESPONSE'].get("mediasetprogram$tvLinearSeasonTitle", None)
            if not program: video_title = legalizestring(raw_data['PROGRAM_URL_RESPONSE'].get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            else: video_title = legalizestring(f"{program}-{raw_data['PROGRAM_URL_RESPONSE'].get('title') or null_backup_title}", replace_null_string=null_backup_title).removesuffix('.')
            resp = self.post(WittyTVVideoClient.PLAYBACK_URL, json={'contentId': content_id, 'streamType': 'VOD'}, headers={'Authorization': f'Bearer {self.BEARER_TOKEN}'})
            resp.raise_for_status()
            raw_data['PLAYBACK_URL_RESPONSE'] = resp2json(resp=resp)
            media_selector: dict = raw_data['PLAYBACK_URL_RESPONSE']["response"]["mediaSelector"]
            manifest = media_selector.pop("url")
            media_selector["auth"] = self.BEARER_TOKEN
            resp = self.get(f"{manifest}?{urlencode(media_selector)}", headers={'Accept': 'application/json, text/plain, */*', 'Origin': WittyTVVideoClient.MEDIASET_URL, 'Referer': WittyTVVideoClient.MEDIASET_URL})
            resp.raise_for_status()
            raw_data['MANIFEST_URL_RESPONSE'] = resp.text
            matches = re.findall(r'<video\s*src="([^"]+)"', raw_data['MANIFEST_URL_RESPONSE'])
            download_url: str = [m for m in matches if ".mpd" in m][0]
            parsed_url = urlparse(download_url); path_parts = parsed_url.path.split("/"); suffix_parts = path_parts[-1].split("_")[1:]
            for resolution in WittyTVVideoClient.RES_PRIORITY:
                with suppress(Exception): candidate_url = urlunparse(parsed_url._replace(path="/".join([*path_parts[:-1], "_".join([resolution, *suffix_parts])]))); response = self.get(f"{candidate_url}?formats={media_selector['formats']}", **request_overrides); assert 200 <= response.status_code < 300; pssh = min(re.findall(r"<cenc:pssh>(.+?)</cenc:pssh>", response.text), key=len, default=None); result = (candidate_url, str(pssh) if pssh else None); break
            download_url, pssh_value = result
            video_info.update(dict(download_url=download_url))
            release_pid, account = re.search(r"\|pid=(.*?)\|", raw_data['MANIFEST_URL_RESPONSE']).group(1), re.search(r"aid=(.*?)\|", raw_data['MANIFEST_URL_RESPONSE']).group(1)
            cdm, cdm_session_id, challenge = initcdm(pssh_value, WittyTVVideoClient.CDM_WVD_FILE_PATH)
            licence = self.post(WittyTVVideoClient.LICENSE_URL, data=challenge, params={'releasePid': release_pid, 'account': WittyTVVideoClient.ACCOUNT_URL.format(a_id=account), 'schema': '1.0', 'token': self.BEARER_TOKEN})
            licence.raise_for_status()
            raw_data['LICENSE_URL_RESPONSE'] = licence.content
            video_info.update(dict(raw_data=raw_data))
            key = list(set(closecdm(cdm, cdm_session_id, licence.content)))[0]
            try: cover_url = raw_data['PROGRAM_URL_RESPONSE']['thumbnails']['image_horizontal_cover-704x396']['url']
            except Exception: cover_url = None
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info.ext}'), identifier=content_id, nm3u8dlre_settings={'key': key}, cover_url=cover_url))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"wittytv.it"}
        return BaseVideoClient.belongto(url, valid_domains)