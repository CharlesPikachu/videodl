'''
Function:
    Implementation of PlusFIFAVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from pathlib import Path
from .base import BaseVideoClient
from ..utils import initcdm, closecdm
from urllib.parse import urlparse, parse_qs
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, safeextractfromdict, VideoInfo


'''PlusFIFAVideoClient'''
class PlusFIFAVideoClient(BaseVideoClient):
    source = 'PlusFIFAVideoClient'
    DEVICE_ID = None
    LANGUAGE = 'eng'
    RES_PRIORITY = {"SDP": 0, "SD": 1, "HD": 2, "HDP": 3}
    CDM_WVD_FILE_PATH = Path(__file__).resolve().parents[2] / "modules" / "cdm" / "charlespikachu_plusfifa.wvd"
    SEARCH_URL = 'https://www.plus.fifa.com/api/v2/search'
    DEVICES_URL = 'https://www.plus.fifa.com/gatekeeper/api/v1/devices/'
    STREAMING_URL = 'https://www.plus.fifa.com/flux-capacitor/api/v1/streaming/urls'
    SESSION_URL = 'https://www.plus.fifa.com/flux-capacitor/api/v1/streaming/session'
    VIDEO_URL = 'https://www.plus.fifa.com/en/player/{video_id}?catalogId={catalog_id}'
    CONTENTS_URL = 'https://www.plus.fifa.com/entertainment/api/v1/contents/{catalog_id}/child'
    ASSET_URL = 'https://www.plus.fifa.com/flux-capacitor/api/v1/videoasset?catalog={catalog_id}'
    SHOWCASES_URL = 'https://www.plus.fifa.com/entertainment/api/v1/showcases/{content_id}/child?orderBy=EDITORIAL'
    LICENSE_URL = "https://www.plus.fifa.com/flux-capacitor/api/v1/licensing/widevine/modular?sessionId={session_id}"
    def __init__(self, **kwargs):
        super(PlusFIFAVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getdeviceid'''
    def _getdeviceid(self, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        resp = self.post(PlusFIFAVideoClient.DEVICES_URL, json={'model': 'model', 'manufacturer': 'manufacturer', 'profile': 'WEB', 'store': 'CHILI'}, **request_overrides)
        resp.raise_for_status()
        device_id = resp2json(resp=resp)['id']
        return device_id
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, ext='mkv', download_with_ffmpeg=True, enable_nm3u8dlre=True, nm3u8dlre_settings={'key': None})
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        if self.DEVICE_ID is None: self.DEVICE_ID = self._getdeviceid()
        # try parse
        try:
            try:
                catalog_id = parse_qs(urlparse(url).query, keep_blank_values=True)['catalogId'][0]
                video_id = re.search(r"/player/([^/?]*)", urlparse(url).path.strip('/')).group(1)
            except:
                catalog_id = urlparse(url).path.strip('/').split("/")[-1]
                resp = self.get(PlusFIFAVideoClient.ASSET_URL.format(catalog_id=catalog_id), headers={'x-chili-device-id': self.DEVICE_ID}, **request_overrides)
                resp.raise_for_status()
                assets = resp2json(resp=resp)
                video_id = next(asset["id"] for asset in assets if (isinstance(asset, dict) and asset.get("type", "").lower() == "main"))
            raw_data = {}
            try:
                resp = self.get(PlusFIFAVideoClient.CONTENTS_URL.format(catalog_id=catalog_id).split("/child")[0], headers={'x-chili-device-id': self.DEVICE_ID}, **request_overrides)
                resp.raise_for_status()
                raw_data['CONTENTS_URL_RESPONSE'] = resp2json(resp=resp)
                video_title = legalizestring(raw_data['CONTENTS_URL_RESPONSE']['title'] or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            except:
                m = re.search(r"/content/(.*?)/", urlparse(url).path.strip('/'))
                video_title = legalizestring((m.group(1) if m else video_id) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            resp = self.post(PlusFIFAVideoClient.SESSION_URL, json={'videoAssetId': video_id}, headers={'x-chili-device-id': self.DEVICE_ID, 'x-chili-avod-compatibility': 'free,free-ads', 'x-chili-accept-stream': 'mpd/cenc+h264;mpd/clear+h264;mp4/', 'x-chili-accept-stream-mode': 'multi/codec-compatibility;mono/strict', 'x-chili-manifest-properties': 'subtitles'}, **request_overrides)
            resp.raise_for_status()
            raw_data['SESSION_URL_RESPONSE'] = resp2json(resp=resp)
            session_id = raw_data['SESSION_URL_RESPONSE']["id"]
            resp = self.get(PlusFIFAVideoClient.STREAMING_URL, headers={'x-chili-streaming-session': session_id}, **request_overrides)
            resp.raise_for_status()
            raw_data['STREAMING_URL_RESPONSE'] = resp2json(resp=resp)
            manifest = sorted(raw_data['STREAMING_URL_RESPONSE'], key=lambda m: PlusFIFAVideoClient.RES_PRIORITY[m["quality"]], reverse=True)
            manifest = [m for m in manifest if m["quality"] == manifest[0]["quality"]]
            temp_man = [m for m in manifest if m["language"].lower().startswith(PlusFIFAVideoClient.LANGUAGE) or PlusFIFAVideoClient.LANGUAGE.startswith(m["language"].lower())]
            download_url = (temp_man[0] if temp_man else manifest[0])['url']
            video_info.update(dict(download_url=download_url))
            pssh_value = str(min(re.findall(r'<cenc:pssh\b[^>]*>(.*?)</cenc:pssh>', self.get(download_url).content.decode()), key=len))
            cdm, cdm_session_id, challenge = initcdm(pssh_value, PlusFIFAVideoClient.CDM_WVD_FILE_PATH)
            licence = self.post(PlusFIFAVideoClient.LICENSE_URL.format(session_id=session_id), data=challenge)
            licence.raise_for_status()
            raw_data['LICENSE_URL_RESPONSE'] = licence.content
            video_info.update(dict(raw_data=raw_data))
            key = list(set(closecdm(cdm, cdm_session_id, licence.content)))[0]
            cover_url = safeextractfromdict(raw_data, ['CONTENTS_URL_RESPONSE', 'backdropUrl'], None)
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info.ext}'), identifier=video_id, nm3u8dlre_settings={'key': key}, cover_url=cover_url))
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
        valid_domains = set(valid_domains or []) | {"plus.fifa.com"}
        return BaseVideoClient.belongto(url, valid_domains)