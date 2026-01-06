'''
Function:
    Implementation of VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import sys
import copy
import click
import json_repair
if __name__ == '__main__':
    from __init__ import __version__
    from modules import BuildVideoClient, BuildCommonVideoClient, LoggerHandle, VideoClientBuilder, CommonVideoClientBuilder, printfullline
else:
    from .__init__ import __version__
    from .modules import BuildVideoClient, BuildCommonVideoClient, LoggerHandle, VideoClientBuilder, CommonVideoClientBuilder, printfullline


'''BASIC_INFO'''
BASIC_INFO = '''Function: Video Downloader --- v%s
Author: Zhenchao Jin
WeChat Official Account (微信公众号): Charles的皮卡丘
Operation Help:
    Enter `r`: Reinitialize the program (i.e., return to the main menu).
    Enter `q`: Exit the program.
Video Save Path:
    %s (root dir is the current directory if using relative path).'''


'''VideoClient'''
class VideoClient():
    def __init__(self, allowed_video_sources: list = None, init_video_clients_cfg: dict = None, clients_threadings: dict = None, requests_overrides: dict = None, apply_common_video_clients_only: bool = False):
        # init
        self.logger_handle = LoggerHandle()
        if not allowed_video_sources: allowed_video_sources = list(VideoClientBuilder.REGISTERED_MODULES.keys()) + list(CommonVideoClientBuilder.REGISTERED_MODULES.keys())
        allowed_video_sources = list(set(allowed_video_sources))
        if apply_common_video_clients_only: allowed_video_sources = [s for s in allowed_video_sources if s in CommonVideoClientBuilder.REGISTERED_MODULES]
        init_video_clients_cfg, clients_threadings, requests_overrides = init_video_clients_cfg or {}, clients_threadings or {}, requests_overrides or {}
        # instance video_clients (lazy instance to speed up parsing)
        default_video_client_cfg = dict(
            auto_set_proxies=False, random_update_ua=False, max_retries=5, maintain_session=False, logger_handle=self.logger_handle,
            disable_print=False, work_dir='videodl_outputs', freeproxy_settings=None, default_search_cookies={}, default_download_cookies={},
            default_parse_cookies={}
        )
        self.video_clients, self.work_dirs = dict(), dict()
        for vc_name in allowed_video_sources:
            if vc_name not in VideoClientBuilder.REGISTERED_MODULES: continue
            per_default_video_client_cfg = copy.deepcopy(default_video_client_cfg)
            per_default_video_client_cfg['type'] = vc_name
            if vc_name in init_video_clients_cfg: per_default_video_client_cfg.update(init_video_clients_cfg[vc_name])
            self.work_dirs[vc_name] = per_default_video_client_cfg['work_dir']
            self.video_clients[vc_name] = {'cfg': per_default_video_client_cfg, 'cls': VideoClientBuilder.REGISTERED_MODULES[vc_name]}
        # instance common_video_clients (lazy instance to speed up parsing)
        self.common_video_clients = dict()
        for cvc_name in allowed_video_sources:
            if cvc_name not in CommonVideoClientBuilder.REGISTERED_MODULES: continue
            per_default_video_client_cfg = copy.deepcopy(default_video_client_cfg)
            per_default_video_client_cfg['type'] = cvc_name
            if cvc_name in init_video_clients_cfg: per_default_video_client_cfg.update(init_video_clients_cfg[cvc_name])
            self.work_dirs[cvc_name] = per_default_video_client_cfg['work_dir']
            self.common_video_clients[cvc_name] = {'cfg': per_default_video_client_cfg, 'cls': CommonVideoClientBuilder.REGISTERED_MODULES[cvc_name]}
        # set attributes
        self.clients_threadings = clients_threadings
        self.requests_overrides = requests_overrides
        self.allowed_video_sources = allowed_video_sources
        self.apply_common_video_clients_only = apply_common_video_clients_only
    '''printbasicinfo'''
    def printbasicinfo(self):
        printfullline(ch='-')
        print(BASIC_INFO % (__version__, ', '.join([f'"{v} for {k}"' for k, v in self.work_dirs.items()])))
        printfullline(ch='-')
    '''startparseurlcmdui'''
    def startparseurlcmdui(self):
        while True:
            self.printbasicinfo()
            # process user inputs
            user_input = self.processinputs('Please enter video url for downloading: ')
            # parse and download
            video_infos = self.parsefromurl(url=user_input)
            self.download(video_infos=video_infos)
    '''parsefromurl'''
    def parsefromurl(self, url: str):
        video_infos = []
        if not self.apply_common_video_clients_only:
            for vc_name in list(self.video_clients.keys()):
                video_client = self.video_clients[vc_name]
                if isinstance(video_client, dict): is_belongto_this_vc = video_client['cls'].belongto(url)
                else: is_belongto_this_vc = video_client.belongto(url)
                if is_belongto_this_vc:
                    if isinstance(video_client, dict): self.video_clients[vc_name] = BuildVideoClient(module_cfg=video_client['cfg'])
                    try:
                        video_infos = self.video_clients[vc_name].parsefromurl(url, request_overrides=self.requests_overrides.get(vc_name, {}))
                        if any(((info.get("download_url") or "") not in ("", "NULL")) for info in (video_infos or [])): break
                    except:
                        video_infos = []
        if not any(((info.get("download_url") or "") not in ("", "NULL")) for info in (video_infos or [])):
            for cvc_name in list(self.common_video_clients.keys()):
                common_video_client = self.common_video_clients[cvc_name]
                if isinstance(common_video_client, dict): self.common_video_clients[cvc_name] = BuildCommonVideoClient(module_cfg=common_video_client['cfg'])
                try:
                    video_infos = self.common_video_clients[cvc_name].parsefromurl(url, request_overrides=self.requests_overrides.get(cvc_name, {}))
                    if any(((info.get("download_url") or "") not in ("", "NULL")) for info in (video_infos or [])): break
                except:
                    video_infos = []
        return video_infos
    '''download'''
    def download(self, video_infos):
        classified_video_infos = {}
        for video_info in video_infos:
            if video_info['source'] in classified_video_infos:
                classified_video_infos[video_info['source']].append(video_info)
            else:
                classified_video_infos[video_info['source']] = [video_info]
        for source, source_video_infos in classified_video_infos.items():
            if source in self.video_clients:
                if isinstance(self.video_clients[source], dict): self.video_clients[source] = BuildVideoClient(module_cfg=self.video_clients[source]['cfg'])
                self.video_clients[source].download(
                    video_infos=source_video_infos, num_threadings=self.clients_threadings.get(source, 5), request_overrides=self.requests_overrides.get(source, {}),
                )
            else:
                if isinstance(self.common_video_clients[source], dict): self.common_video_clients[source] = BuildCommonVideoClient(module_cfg=self.common_video_clients[source]['cfg'])
                self.common_video_clients[source].download(
                    video_infos=source_video_infos, num_threadings=self.clients_threadings.get(source, 5), request_overrides=self.requests_overrides.get(source, {}),
                )
    '''processinputs'''
    def processinputs(self, input_tip='', prefix: str = '\n', restart_ui: str = 'startparseurlcmdui'):
        # accept user inputs
        user_input = input(prefix + input_tip)
        # quit
        if user_input.lower() == 'q':
            self.logger_handle.info('Goodbye — thanks for using videodl; come back anytime!')
            sys.exit()
        # restart
        elif user_input.lower() == 'r':
            getattr(self, restart_ui)()
        # common inputs
        else:
            return user_input
    '''str'''
    def __str__(self):
        return 'Welcome to use videodl!\nYou can visit https://github.com/CharlesPikachu/videodl for more details.'


'''VideoClientCMD'''
@click.command()
@click.version_option(version=__version__)
@click.option(
    '-i', '--index-url', '--index_url', default=None, help='URL of the video to download. If not specified, videodl will start in terminal mode.', type=str, show_default=True,
)
@click.option(
    '-a', '--allowed-video-sources', '--allowed_video_sources', default=None, help='Platforms to search. Separate multiple platforms with "," (e.g., "AcFunVideoClient,PipixVideoClient"). If not specified, videodl will search all supported platforms globally and use the first one that can download the video url.', type=str, show_default=True,
)
@click.option(
    '-c', '--init-video-clients-cfg', '--init_video_clients_cfg', default=None, help='Config such as `work_dir` for each video client as a JSON string.', type=str, show_default=True,
)
@click.option(
    '-r', '--requests-overrides', '--requests_overrides', default=None, help='Requests.get kwargs such as `headers` and `proxies` for each video client as a JSON string.', type=str, show_default=True,
)
@click.option(
    '-t', '--clients-threadings', '--clients_threadings', default=None, help='Number of threads used for each video client as a JSON string.', type=str, show_default=True,
)
@click.option(
    '-g', '--apply-common-video-clients-only', '--apply_common_video_clients_only', is_flag=True, default=False, help='Only apply common video clients.', show_default=True,
)
def VideoClientCMD(index_url: str, allowed_video_sources: str, init_video_clients_cfg: str, requests_overrides: str, clients_threadings: str, apply_common_video_clients_only: bool):
    # load settings
    def _safe_load(string):
        if string is not None:
            result = json_repair.loads(string) or {}
        else:
            result = {}
        return result
    allowed_video_sources = [s.strip() for s in allowed_video_sources.strip().split(',')] if allowed_video_sources else []
    init_video_clients_cfg = _safe_load(init_video_clients_cfg)
    requests_overrides = _safe_load(requests_overrides)
    clients_threadings = _safe_load(clients_threadings)
    # instance video client
    video_client = VideoClient(
        allowed_video_sources=allowed_video_sources, init_video_clients_cfg=init_video_clients_cfg, clients_threadings=clients_threadings, 
        requests_overrides=requests_overrides, apply_common_video_clients_only=apply_common_video_clients_only,
    )
    # switch according to keyword
    if index_url is None:
        video_client.startparseurlcmdui()
    else:
        print(video_client)
        # --parse
        video_infos = video_client.parsefromurl(url=index_url)
        # --download
        video_client.download(video_infos=video_infos)


'''tests'''
if __name__ == '__main__':
    music_client = VideoClient(apply_common_video_clients_only=True)
    music_client.startparseurlcmdui()