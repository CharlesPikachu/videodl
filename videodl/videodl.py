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
if __name__ == '__main__':
    from __init__ import __version__
    from modules import BuildVideoClient, LoggerHandle, VideoClientBuilder
else:
    from .__init__ import __version__
    from .modules import BuildVideoClient, LoggerHandle, VideoClientBuilder


'''BASIC_INFO'''
BASIC_INFO = '''************************************************************
Function: Video Downloader --- v%s
Author: Zhenchao Jin
WeChat Official Account (微信公众号): Charles的皮卡丘
Operation Help:
    Enter `r`: Reinitialize the program (i.e., return to the main menu).
    Enter `q`: Exit the program.
Video Save Path:
    %s (root dir is the current directory if using relative path).
************************************************************'''


'''VideoClient'''
class VideoClient():
    def __init__(self, allowed_video_sources: list = None, init_video_clients_cfg: dict = {}, clients_threadings: dict = {}, requests_overrides: dict = {}):
        # init
        self.logger_handle = LoggerHandle()
        if allowed_video_sources is None: allowed_video_sources = list(VideoClientBuilder.REGISTERED_MODULES.keys())
        # instance video_clients
        default_video_client_cfg = dict(
            auto_set_proxies=False, random_update_ua=False, max_retries=5, maintain_session=False, logger_handle=self.logger_handle,
            disable_print=False, work_dir='videodl_outputs', proxy_sources=None, default_search_cookies={}, default_download_cookies={},
            default_parse_cookies={}
        )
        self.video_clients, self.work_dirs = dict(), dict()
        for allowed_video_source in allowed_video_sources:
            per_default_video_client_cfg = copy.deepcopy(default_video_client_cfg)
            per_default_video_client_cfg['type'] = allowed_video_source
            if allowed_video_source in init_video_clients_cfg:
                per_default_video_client_cfg.update(init_video_clients_cfg[allowed_video_source])
            self.work_dirs[allowed_video_source] = per_default_video_client_cfg['work_dir']
            self.video_clients[allowed_video_source] = BuildVideoClient(module_cfg=per_default_video_client_cfg)
        # set attributes
        self.clients_threadings = clients_threadings
        self.requests_overrides = requests_overrides
        self.allowed_video_sources = allowed_video_sources
    '''startparseurlcmdui'''
    def startparseurlcmdui(self):
        while True:
            print(BASIC_INFO % (__version__, ', '.join([f'"{v} for {k}"' for k, v in self.work_dirs.items()])))
            # process user inputs
            user_input = self.processinputs('Please enter video url for downloading: ')
            # parse and download
            for video_client_name, video_client in self.video_clients.items():
                if video_client.belongto(user_input):
                    video_infos = video_client.parsefromurl(user_input, request_overrides=self.requests_overrides.get(video_client_name, {}))
                    video_client.download(
                        video_infos=video_infos, num_threadings=self.clients_threadings.get(video_client_name, 1), request_overrides=self.requests_overrides.get(video_client_name, {})
                    )
                    break
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