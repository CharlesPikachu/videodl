'''
Function:
    Implementation of TencentVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import random
import string
import json_repair
from datetime import datetime
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse
from typing import Dict, Any, List
from ..utils import legalizestring, searchdictbykey, useparseheaderscookies, FileTypeSniffer, VideoInfo, AESAlgorithmWrapper


'''TencentVideoClient'''
class TencentVideoClient(BaseVideoClient):
    source = 'TencentVideoClient'
    def __init__(self, **kwargs):
        super(TencentVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getckey'''
    def _getckey(self, video_id, url, guid, app_version, platform):
        ua = self.default_headers['User-Agent']
        payload = (f'{video_id}|{int(time.time())}|mg3c3b04ba|{app_version}|{guid}|{platform}|{url[:48]}|{ua.lower()[:48]}||Mozilla|Netscape|Windows x86_64|00|')
        return AESAlgorithmWrapper.aescbcencryptbytes(bytes(f'|{sum(map(ord, payload))}|{payload}', 'utf-8'), b'Ok\xda\xa3\x9e/\x8c\xb0\x7f^r-\x9e\xde\xf3\x14', b'\x01PJ\xf3V\xe6\x19\xcf.B\xbb\xa6\x8c?p\xf9', padding_mode='whitespace').hex().upper()
    '''_getvinfo'''
    def _getvinfo(self, api_url, video_url, video_id, series_id, subtitle_format, video_format, video_quality, host='v.qq.com', referer='v.qq.com', app_version='3.5.57', platform='10901', request_overrides=None):
        request_overrides = request_overrides or {}
        guid = ''.join(random.choices(string.digits + string.ascii_lowercase, k=16))
        ckey = self._getckey(video_id, video_url, guid, app_version=app_version, platform=platform)
        params = {
            'vid': video_id, 'cid': series_id, 'cKey': ckey, 'encryptVer': '8.1', 'spcaptiontype': '1' if subtitle_format == 'vtt' else '0',
            'sphls': '2' if video_format == 'hls' else '0', 'dtype': '3' if video_format == 'hls' else '0', 'defn': video_quality, 'spsrt': '2',
            'sphttps': '1', 'otype': 'json', 'spwm': '1', 'hevclv': '28', 'drm': '40', 'spvideo': '4', 'spsfrhdr': '100', 'host': host, 'referer': referer,
            'ehost': video_url, 'appVer': app_version, 'platform': platform, 'guid': guid, 'flowid': ''.join(random.choices(string.digits + string.ascii_lowercase, k=32)),
        }
        resp = self.get(api_url, params=params, **request_overrides)
        resp.raise_for_status()
        vinfo = json_repair.loads(resp.text[resp.text.index('QZOutputJson=')+len('QZOutputJson='): -1])
        return vinfo
    '''_extractfromvinfo'''
    def _extractfromvinfo(self, vinfos):
        results: List[Dict[str, Any]] = []
        for api_response in vinfos:
            if not isinstance(api_response, dict): continue
            try: video_response = (api_response.get('vl') or {}).get('vi')[0]
            except Exception: continue
            if not isinstance(video_response, dict): continue
            ul = video_response.get('ul') or {}
            ui_list = ul.get('ui') or []
            if not ui_list: continue
            fl = api_response.get('fl') or {}
            fi_list = fl.get('fi') or []
            identifier = video_response.get('br')
            format_info = None
            for fi in fi_list:
                if not isinstance(fi, dict): continue
                if identifier is not None and fi.get('br') == identifier: format_info = fi; break
            if format_info is None and fi_list: format_info = fi_list[0]
            if format_info is None: format_info = {}
            format_id = format_info.get('name') or format_info.get('formatdefn')
            format_note = format_info.get('resolution') or format_info.get('cname')
            width = format_info.get('width') or video_response.get('vw')
            height = format_info.get('height') or video_response.get('vh')
            vbr = format_info.get('bandwidth')
            abr = format_info.get('audiobandwidth')
            fps = format_info.get('vfps')
            for video_format in ui_list:
                if not isinstance(video_format, dict): continue
                base_url = video_format.get('url') or ''
                if not base_url: continue
                hls = video_format.get('hls')
                if hls:
                    pt = hls.get('pt') or ''
                    url = base_url + pt
                    ext = 'm3u8'
                elif '.m3u8' in base_url:
                    url = base_url
                    ext = 'm3u8'
                else:
                    fn, vkey = video_response.get('fn') or '', video_response.get('fvkey') or ''
                    if fn and vkey: url = f'{base_url}{fn}?vkey={vkey}'
                    else: url = base_url
                    ext = 'mp4'
                if not url: continue
                results.append({'url': url, 'ext': ext, 'format_id': format_id, 'format_note': format_note, 'width': width, 'height': height, 'vbr': vbr, 'abr': abr, 'fps': fps})
        return results
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        # try parse
        try:
            # --basic info extract with different netloc
            parsed_url = urlparse(url)
            if parsed_url.netloc in ['v.qq.com']:
                api_url, app_version, platform, host, referer = 'https://h5vv6.video.qq.com/getvinfo', '3.5.57', '10901', 'v.qq.com', 'v.qq.com'
                m = re.match(r'https?://v\.qq\.com/x/(?:page|cover/(?P<series_id>\w+))/(?P<id>\w+)', url)
                video_id, series_id = m.group('id'), m.group('series_id')
                resp = self.get(url, **request_overrides)
                resp.raise_for_status()
                raw_data = re.search(r'window\.__(?:pinia|PINIA__)\s*=\s*({.*?})\s*;?\s*</script>', resp.text, flags=re.S).group(1)
                raw_data = json_repair.loads(raw_data)
            elif parsed_url.netloc in ['www.iflix.com']:
                api_url, app_version, platform, host, referer = 'https://vplay.iflix.com/getvinfo', '3.5.57', '330201', 'www.iflix.com', 'www.iflix.com'
                m = re.match(r'https?://(?:www\.)?iflix\.com/(?:[^?#]+/)?play/(?P<series_id>\w+)(?:-[^?#]+)?/(?P<id>\w+)(?:-[^?#]+)?', url)
                video_id, series_id = m.group('id'), m.group('series_id')
                resp = self.get(url, **request_overrides)
                resp.raise_for_status()
                raw_data = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(\{.*?\})</script>', resp.text, flags=re.S).group(1)
                raw_data = json_repair.loads(raw_data)
            elif parsed_url.netloc in ['wetv.vip']:
                api_url, app_version, platform, host, referer = 'https://play.wetv.vip/getvinfo', '3.5.57', '4830201', 'wetv.vip', 'wetv.vip'
                m = re.match(r'https?://(?:www\.)?wetv\.vip/(?:[^?#]+/)?play/(?P<series_id>\w+)(?:-[^?#]+)?/(?P<id>\w+)(?:-[^?#]+)?', url)
                video_id, series_id = m.group('id'), m.group('series_id')
                resp = self.get(url, **request_overrides)
                resp.raise_for_status()
                raw_data = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(\{.*?\})</script>', resp.text, flags=re.S).group(1)
                raw_data = json_repair.loads(raw_data)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            video_title = soup.title.string.split('_')[0].split('-')[0].strip().strip('“"”') if soup.title else None
            if not video_title:
                video_title = [t for t in searchdictbykey(raw_data, 'title') if t.strip() and len(t.strip()) > 1]
                video_title = video_title[0] if video_title else None
            # --get vinfos
            vinfos = [self._getvinfo(
                api_url=api_url, video_url=url, video_id=video_id, series_id=series_id, subtitle_format='srt', video_format='hls', video_quality='hd', 
                host=host, referer=referer, app_version=app_version, platform=platform, request_overrides=request_overrides
            )]
            qualities = [item.get('name') for item in vinfos[0]['fl']['fi'] if item.get('name')] or ('shd', 'fhd')
            for quality in qualities:
                if quality not in ('ld', 'sd', 'hd'):
                    try:
                        vinfos.append(self._getvinfo(
                            api_url=api_url, video_url=url, video_id=video_id, series_id=series_id, subtitle_format='vtt', video_format='hls', video_quality=quality, 
                            host=host, referer=referer, app_version=app_version, platform=platform, request_overrides=request_overrides
                        ))
                    except:
                        continue
            vinfos = [v for v in vinfos if v]
            raw_data['getvinfo'] = vinfos
            video_info.update(dict(raw_data=raw_data))
            # --reformat vinfos
            formatted_vinfos = self._extractfromvinfo(vinfos=vinfos)
            # --sorted by quality
            def _toint(v, default=0):
                try: return int(v)
                except Exception: return default
            def _inferheight(fmt: Dict[str, Any]):
                h = fmt.get('height')
                if h is not None: return _toint(h, 0)
                note = fmt.get('format_note') or ''
                m = re.search(r'(\d+)[pP]', note)
                if m: return _toint(m.group(1), 0)
                return 0
            def _inferwidth(fmt: Dict[str, Any], height: int):
                w = fmt.get('width')
                if w is not None: return _toint(w, 0)
                if height > 0: return int(height * 16 / 9)
                return 0
            def _qualitykey(fmt: Dict[str, Any]):
                h = _inferheight(fmt)
                w = _inferwidth(fmt, h)
                vbr = _toint(fmt.get('vbr'), 0)
                abr = _toint(fmt.get('abr'), 0)
                return (h, w, vbr, abr)
            sorted_formatted_vinfos = sorted(formatted_vinfos, key=_qualitykey, reverse=True)
            # --select the best and update video info
            download_url = sorted_formatted_vinfos[0]['url']
            video_info.update(dict(download_url=download_url))
            # --misc
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(video_title or f'{self.source}_null_{date_str}', replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=f'{series_id}_{video_id}'
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
            valid_domains = ["v.qq.com", "www.iflix.com", "wetv.vip"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)