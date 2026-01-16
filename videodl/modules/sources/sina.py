'''
Function:
    Implementation of SinaVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, safeextractfromdict, VideoInfo


'''SinaVideoClient'''
class SinaVideoClient(BaseVideoClient):
    source = 'SinaVideoClient'
    def __init__(self, **kwargs):
        super(SinaVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Referer': 'https://video.sina.cn/',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'https://video.sina.cn/',
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
            # --parse video id
            pattern = re.compile(r'''(?x)https?://(?:[^/?#]+\.)?video\.sina\.com\.cn/
                        (?:
                            (?:view/|.*\#)(?P<id>\d+)|
                            .+?/(?P<pseudo_id>[^/?#]+)(?:\.s?html)|
                            api/sinawebApi/outplay.php/(?P<token>.+?)\.swf
                        )
                  ''')
            video_id = pattern.match(url).group('id')
            if not video_id:
                if pattern.match(url).group('token') is not None:
                    resp = self.get(url, **request_overrides)
                    resp.raise_for_status()
                    assert resp.url != url
                    self.parsefromurl(resp.url, request_overrides=request_overrides)
                else:
                    resp = self.get(url, **request_overrides)
                    resp.raise_for_status()
                    for p in [r"video_id\s*:\s*'(\d+)'", r"video_id\s*:\s*(\d+),"]:
                        try: video_id = re.search(p, resp.text, flags=re.DOTALL).group(1); break
                        except: continue
            # --obtain raw_data
            resp = self.get('http://s.video.sina.com.cn/video/h5play', params={'video_id': video_id}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --parse raw data
            video_data, formats = raw_data['data'], []
            for quality_id, quality in safeextractfromdict(video_data, ['videos', 'mp4'], {}).items():
                if not isinstance(quality, dict): continue
                file_api, file_id = quality.get('file_api'), quality.get('file_id')
                if not file_api or not file_id: continue
                download_url = f'{file_api}?foo=bar&vid={file_id}'
                formats.append({'quality': quality_id, 'download_url': download_url})
            quality_rank = {'cif': 0, 'sd': 1, 'hd': 2, 'fhd': 3, 'ffd': 4}
            formats: list[dict] = sorted(formats, key=lambda x: quality_rank.get(x['quality'], -1), reverse=True)
            formats: list[dict] = [item for item in formats if item.get('download_url')]
            download_url = formats[0]['download_url']
            resp = self.get(download_url, stream=True, **request_overrides)
            if resp.status_code > 400:
                params = {
                    "video_id": video_id, "appver": "V11220.210521.03", "appname": "sinaplayer_pc", "applt": "web", "tags": "sinaplayer_pc", "player": "all", "jsonp": "", 
                    "plid": "2021012801", "prid": "", "uid": "", "tid": "", "pid": "1", "ran": "0.2649524433568291", "r": "https://video.sina.com.cn/p/finance/2025-11-28/detail-infyypay7178654.d.html", 
                    "referrer": "", "ssid": "gusr_pc_1764397613438", "preload": "0", "uu": "114.92.19.247_1764392514.160162", "isAuto": "1",
                }
                resp = self.get('https://api.ivideo.sina.com.cn/public/video/play?', params=params, **request_overrides)
                resp.raise_for_status()
                raw_data['play'] = resp2json(resp=resp)
                formats = raw_data['play']['data']['videos']
                formats: list[dict] = sorted(formats, key=lambda x: quality_rank.get(x['definition'], -1), reverse=True)
                formats: list[dict] = [item for item in formats if item['dispatch_result']['url'] or item['dispatch_result']['bakurl']]
                download_url = formats[0]['dispatch_result']['url'] or formats[0]['dispatch_result']['bakurl']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(video_data.get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.mp4'), ext='mp4', identifier=video_id,
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
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"video.sina.com.cn"}
        return BaseVideoClient.belongto(url, valid_domains)