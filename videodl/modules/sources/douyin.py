'''
Function:
    Implementation of DouyinVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import random
import json_repair
from urllib.parse import quote
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo
from ..utils.douyin_sign import get_a_bogus, gen_verify_fp, DEFAULT_UA


'''DouyinVideoClient'''
class DouyinVideoClient(BaseVideoClient):
    source = 'DouyinVideoClient'
    ROUTER_DATA_RE = re.compile(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>", re.S | re.I)
    # 匿名 ttwid 注册体（拿 ttwid，约 1 年有效，签名 web 接口要带它）
    TTWID_REGISTER_URL = 'https://ttwid.bytedance.com/ttwid/union/register/'
    TTWID_REGISTER_BODY = {'region': 'cn', 'aid': 1768, 'needFid': False, 'service': 'www.ixigua.com',
                           'migrate_info': {'ticket': '', 'source': 'node'}, 'cbUrlProtocol': 'https', 'union': True}
    # web detail 接口
    DETAIL_URL = 'https://www.douyin.com/aweme/v1/web/aweme/detail/'
    # 浏览器画像池：每次解析随机挑一套（UA + 浏览器版本 + 平台 + 系统）。
    # 关键约束：a_bogus 用 ua 签名、请求也用 ua，且参数里的 browser_version/os 必须与 ua 一致。
    WEB_PROFILES = [
        {'ua': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
         'ver': '131.0.0.0', 'platform': 'MacIntel', 'os_name': 'Mac+OS', 'os_version': '10.15.7', 'libra': 'Mac'},
        {'ua': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
         'ver': '138.0.0.0', 'platform': 'MacIntel', 'os_name': 'Mac+OS', 'os_version': '10.15.7', 'libra': 'Mac'},
        {'ua': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
         'ver': '149.0.0.0', 'platform': 'MacIntel', 'os_name': 'Mac+OS', 'os_version': '10.15.7', 'libra': 'Mac'},
        {'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
         'ver': '133.0.0.0', 'platform': 'Win32', 'os_name': 'Windows', 'os_version': '10', 'libra': 'Windows'},
        {'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
         'ver': '144.0.0.0', 'platform': 'Win32', 'os_name': 'Windows', 'os_version': '10', 'libra': 'Windows'},
    ]
    '''_detailquery: 按画像拼出 detail 接口的查询串（与签名严格一致）'''
    @staticmethod
    def _detailquery(aweme_id: str, p: dict, verify_fp: str) -> str:
        return (f"device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}"
                f"&pc_client_type=1&pc_libra_divert={p['libra']}&support_h265=1&support_dash=0"
                f"&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1512&screen_height=982"
                f"&browser_language=en-US&browser_platform={p['platform']}&browser_name=Chrome"
                f"&browser_version={p['ver']}&browser_online=true&engine_name=Blink&engine_version={p['ver']}"
                f"&os_name={p['os_name']}&os_version={p['os_version']}&cpu_core_num=10&device_memory=16"
                f"&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&verifyFp={verify_fp}&fp={verify_fp}")
    def __init__(self, **kwargs):
        super(DouyinVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'}
        self.default_headers = self.default_parse_headers
        self._ttwid = None
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            (resp := self.get(url, allow_redirects=False, **request_overrides)).raise_for_status(); location = resp.headers.get("Location")
            if not location: (resp := self.get(url, allow_redirects=True, **request_overrides)).raise_for_status(); location = resp.url
            vid = re.search(r"\d+", location).group(0)
            (resp := self.get(f"https://www.iesdouyin.com/share/video/{vid}", **request_overrides)).raise_for_status()
            raw_data = DouyinVideoClient.ROUTER_DATA_RE.search(resp.text).group(1).strip().rstrip("; \n\r\t")
            if not raw_data.startswith("{"): raw_data = raw_data[raw_data.find("{"):].rstrip("; \n\r\t") if raw_data.find("{") != -1 else raw_data
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(raw_data))))
            video_detail = safeextractfromdict(raw_data, ['loaderData', 'video_(id)/page', 'videoInfoRes', 'item_list', 0], {})
            # 图集/实况帖：分享页里 images 只有静态图、不含实况视频（被剥离），
            # 拿不到视频时才走签名 web 接口把每个实况的视频抓出来（issue #61）。
            if video_detail.get('images'):
                live_infos = self._parse_livephotos(vid, request_overrides)
                if live_infos: return live_infos
            # 普通视频（或纯静态图集的合成幻灯片）：先走分享页老链接
            download_url = f"http://www.iesdouyin.com/aweme/v1/play/?video_id={video_detail['video']['play_addr']['uri']}&ratio=1080p&line=0"
            video_title = legalizestring(video_detail.get('desc') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            dl_headers = self.default_download_headers
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=dl_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            # 部分视频的 iesdouyin 老端点已失效（被迁移到签名接口、返回 404）：探测到死链就
            # fallback 到签名 web detail 拿真实直链（修复"部分视频取不到"）。
            if not guess_video_ext_result.get('ok'):
                real_url = safeextractfromdict(self._awemedetail(vid, request_overrides) or {}, ['video', 'play_addr', 'url_list', 0], None)
                if real_url:
                    download_url, dl_headers = real_url, {'User-Agent': DEFAULT_UA, 'Referer': 'https://www.douyin.com/'}
                    video_info.default_download_headers = dl_headers
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=dl_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True) or guess_video_ext_result
            ext = guess_video_ext_result['ext'] if guess_video_ext_result.get('ext') and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(download_url=download_url, title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(video_detail, ['video', 'cover', 'url_list', 0], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''_ensurettwid: 匿名获取并缓存 ttwid（签名 web 接口需带）'''
    def _ensurettwid(self, request_overrides: dict = None):
        if self._ttwid: return self._ttwid
        request_overrides = request_overrides or {}
        try:
            resp = self.post(DouyinVideoClient.TTWID_REGISTER_URL, json=DouyinVideoClient.TTWID_REGISTER_BODY, **request_overrides)
            self._ttwid = (getattr(resp, 'cookies', None) or {}).get('ttwid') if resp is not None else None
        except Exception as err:
            self.logger_handle.error(f'{self.source}._ensurettwid >>> (Error: {err})', disable_print=self.disable_print)
        return self._ttwid
    '''_awemedetail: 随机挑一套浏览器画像，用 a_bogus 签名 + ttwid 调 web detail 接口，返回 aweme_detail'''
    def _awemedetail(self, aweme_id: str, request_overrides: dict = None):
        request_overrides = dict(request_overrides or {})
        ttwid = self._ensurettwid(request_overrides)
        if not ttwid: return None
        profile = random.choice(DouyinVideoClient.WEB_PROFILES)
        ua = profile['ua']
        query = DouyinVideoClient._detailquery(aweme_id, profile, gen_verify_fp())
        a_bogus = get_a_bogus(query, ua)
        url = f'{DouyinVideoClient.DETAIL_URL}?{query}&a_bogus={quote(a_bogus, safe="")}'
        # 关键：发请求的 UA 必须与签名用的 UA 一致 + 带 ttwid cookie
        overrides = dict(request_overrides)
        overrides['headers'] = {**(request_overrides.get('headers') or {}), 'User-Agent': ua, 'Referer': 'https://www.douyin.com/'}
        overrides['cookies'] = {**(request_overrides.get('cookies') or {}), 'ttwid': ttwid}
        resp = self.get(url, **overrides)
        return (resp.json() or {}).get('aweme_detail') if resp is not None else None
    '''_parse_livephotos: 把图集里每个实况的视频各解析成一个 VideoInfo（静态图跳过）'''
    def _parse_livephotos(self, aweme_id: str, request_overrides: dict = None):
        detail = self._awemedetail(aweme_id, request_overrides)
        if not detail: return []
        images = detail.get('images') or []
        null_backup_title = yieldtimerelatedtitle(self.source)
        base_title = legalizestring(detail.get('desc') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
        web_headers = {'User-Agent': DEFAULT_UA, 'Referer': 'https://www.douyin.com/'}
        infos, idx = [], 0
        for image in images:
            video = image.get('video') if isinstance(image, dict) else None
            download_url = safeextractfromdict(video or {}, ['play_addr', 'url_list', 0], None)
            if not download_url: continue   # 静态图（无实况视频）跳过
            idx += 1
            title = f'{base_title}_{idx:02d}'
            vi = VideoInfo(source=self.source)
            vi.update(dict(
                download_url=download_url, title=title, ext='mp4',
                save_path=os.path.join(self.work_dir, self.source, f'{title}.mp4'),
                identifier=f'{aweme_id}_{idx:02d}',
                cover_url=safeextractfromdict(video, ['cover', 'url_list', 0], None),
                default_download_headers=web_headers,
            ))
            infos.append(vi)
        return infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"douyin.com"}
        return BaseVideoClient.belongto(url, valid_domains)
