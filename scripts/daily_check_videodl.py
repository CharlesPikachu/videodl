'''
Function:
    Implementation of auto daily checking for videodl + small preview videos
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json
import time
import random
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from videodl.modules import VideoClientBuilder, BaseVideoClient


'''constants'''
WORK_DIR = 'videodl_tmp_outputs'
MAX_PREVIEW_DURATION = 30
VIDEODL_TEST_SAMPLES = {
    'AcFunVideoClient': [
        'https://www.acfun.cn/v/ac29566205', 
        'https://www.acfun.cn/v/ac47998293', 
        'https://www.acfun.cn/v/ac36491489',
    ],
    'HaokanVideoClient': [
        'https://haokan.baidu.com/v?vid=7295039339702288421', 
        'https://haokan.baidu.com/v?vid=7224830823778858146',
    ],
    'TedVideoClient': [
        'https://www.ted.com/talks/alanna_shaikh_why_covid_19_is_hitting_us_now_and_how_to_prepare_for_the_next_outbreak', 
        'https://www.ted.com/talks/adam_kucharski_how_can_we_control_the_coronavirus_pandemic'
    ],
    'PipigaoxiaoVideoClient': [
        'https://h5.ippzone.com/pp/post/350259149175?zy_to=copy_link&share_count=1&m=0cd13da8548a1bc85813d8c60d331e22&app=&type=post&did=d2bddf23159ae495&mid=1270840711117&pid=350259149175',
        'https://h5.ippzone.com/pp/post/870235406308?app=&did=d2bddf23159ae495&m=0cd13da8548a1bc85813d8c60d331e22&mid=1270840711117&pid=870235406308&share_count=1&type=post&zy_to=copy_link'
    ],
    'PipixVideoClient': [
        'https://h5.pipix.com/item/6740623460659108107?app_id=1319&app=super&timestamp=1574241444&user_id=1085910221863021&carrier_region=cn&region=cn&language=zh&utm_source=weixin',
        'https://h5.pipix.com/item/6863294377570081027?app_id=1319&app=super&timestamp=1598011674&user_id=62108092335&carrier_region=cn&region=cn&language=zh&utm_source=weixin'
    ],
    'Ku6VideoClient': [
        'https://www.ku6.com/video/detail?id=McZoSe_hgG_jwzy7pQLqvMJ3IoI.', 
        'https://www.ku6.com/video/detail?id=HE3lfhcp13Gd0qND4zfzXYQONMY.'
    ],
    'KuaishouVideoClient': [
        'https://www.kuaishou.com/short-video/3xwzr5dveyqc5fa?authorId=3xv7d3j7hqqpksi', 
        'https://www.kuaishou.com/short-video/3xjpwzyparcgnck?authorId=3xbbsmxr7cdmhqs'
    ],
    'BilibiliVideoClient': [
        'https://www.bilibili.com/video/BV16Z4y1X784/?spm_id_from=333.851.b_7265636f6d6d656e64.2', 
        'https://www.bilibili.com/video/BV1KZgHzJEs6/?spm_id_from=333.337.search-card.all.click'
    ],
    'YinyuetaiVideoClient': [
        'https://www.yinyuetai.com/watch/7200480383631265792?listType=swiper&listId=6998475633361805312'
    ],
    'BaiduTiebaVideoClient': [
        'https://tieba.baidu.com/p/7280373361',
        'https://tieba.baidu.com/p/10253039554'
    ],
    'MGTVVideoClient': [
        'https://www.mgtv.com/l/100026064/19868457.html?fpa=1684&fpos=&lastp=ch_home&cpid=5',
        'https://www.mgtv.com/b/788366/23780111.html?fpa=1756&fpos=&lastp=ch_home', # requires pass VIP login-in cookies by default_download_cookies to download full video
        'https://www.mgtv.com/b/805972/23756299.html?fpa=1261&fpos=&lastp=ch_home&cpid=5', # requires pass login-in cookies by default_download_cookies to download full video
    ],
    'OasisVideoClient': [
        'https://m.oasis.weibo.cn/v1/h5/share?sid=4497689997350015&luicode=10001122&lfid=lz_qqfx&bid=4497689997350015',
        'https://m.oasis.weibo.cn/v1/h5/share?sid=4506676592820518',
    ],
    'PearVideoClient': [
        'https://www.pearvideo.com/video_1803264',
        'https://www.pearvideo.com/video_1803574',
    ],
    'HuyaVideoClient': [
        'https://www.huya.com/video/play/1084162990.html',
        'https://www.huya.com/video/play/1081888422.html',
    ],
    'MeipaiVideoClient': [
        'http://www.meipai.com/media/6995325250108940314',
        'http://www.meipai.com/media/6983711035636086653'
    ],
    'DuxiaoshiVideoClient': [
        'http://quanmin.baidu.com/sv?source=share-h5&pd=qm_share_search&vid=12474281128791424380', 
        'https://mbd.baidu.com/newspage/data/videolanding?nid=sv_8388278490910791594&sourceFrom=rec'
    ],
    'SixRoomVideoClient': [
        'https://v.6.cn/minivideo/7425678',
        'https://v.6.cn/profile/watchMini.php?vid=5584111', 
    ],
    'WeishiVideoClient': [
        'https://h5.weishi.qq.com/weishi/feed/76EaWNkEF1IqtfYVH/',
        'https://isee.weishi.qq.com/ws/app-pages/share/index.html?wxplay=1&id=7siJelmUp1MkDSPeo&spid=3704775550396963513&qua=v1_and_weishi_8.81.0_590_312026001_d&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011'
    ],
    'ZuiyouVideoClient': [
        'https://share.xiaochuankeji.cn/hybrid/share/post?pid=285701565&zy_to=applink&share_count=1&m=01a529af83555742c8f3b3dd43458057&d=9d65722d31131635796498e5eefbb375256c002df068298ce57006de10ed92fd&app=zuiyou&recommend=r0&name=n0&title_type=t0',
        'https://share.xiaochuankeji.cn/hybrid/share/post?pid=413455067'
    ],
    'XinpianchangVideoClient': [
        'https://www.xinpianchang.com/a13536060?from=IndexPick&part=%E7%BC%96%E8%BE%91%E7%B2%BE%E9%80%89&index=1',
        'https://www.xinpianchang.com/a13419465?from=ArticleList'
    ],
    'WeSingVideoClient': [
        'https://kg.qq.com/node/user/bb132c338e/song/play-edLkcwAsRj?s=bCyoDlbCUhcjXbkQ&shareuid=&topsource=znxvljkwehoit_rqojkwehfguioqef_fnajkgfb&g_f=',
        'https://kg.qq.com/node/play?s=WYsF1AWj1UTvLWXu&g_f=personal&appsource=&pageId=personalH5'
    ],
    'XiguaVideoClient': [
        'https://www.ixigua.com/7382121243505328655',
    ],
    'WeiboVideoClient': [
        'https://weibo.com/tv/show/1034:5234817776943232?mid=5234851004547318',
        'https://m.weibo.cn/detail/5234820306442377',
        'https://m.weibo.cn/detail/4749967266939049',
        'https://weibo.com/tv/v/HApWK8FAc?fid=1034:4386795211940756',
    ],
    'RednoteVideoClient': [
        'http://xhslink.com/o/6B9wstL9kEM',
    ],
    'CCTVVideoClient': [
        'https://v.cctv.com/2021/06/05/VIDEwn0n7VRJokIL7rBi2ink210605.shtml?spm=C90324.Pfdd0SYeqktv.Eri5TUDwaTXO.6',
        'https://tv.cctv.com/2022/04/15/VIDEYQOwJ33dIqm1h9PvmIpO220415.shtml?spm=C95797228340.P3XSH3djsU2B.0.0',
        'https://xczx.cctv.com/2025/11/19/ARTIhGNpDUfXpmRX0qjQ6mSC251119.shtml?spm=C73274.Pt2UfsofZQQ5.EmwSKtAQYeDI.2',
    ],
    'SohuVideoClient': [
        'https://tv.sohu.com/v/dXMvMjcxMzIzNDM0LzY3OTc4Mzk0OC5zaHRtbA==.html?src=list',
        'https://tv.sohu.com/v/dXMvMzQ0NDIzNTcxLzY4NDgyODI5Mi5zaHRtbA==.html',
        'https://film.sohu.com/album/9697072.html',
        'https://tv.sohu.com/v/MjAyNDA5MjIvbjYyMDAxMTUyMS5zaHRtbA==.html',
    ],
    'YouTubeVideoClient': [
        'https://music.youtube.com/watch?v=PgPhDyV0J2w&list=RDAMVMPgPhDyV0J2w',
        'https://www.youtube.com/watch?v=hie-SsINu4Q&list=RDhie-SsINu4Q&start_radio=1',
    ],
    'ZhihuVideoClient': [
        'https://www.zhihu.com/zvideo/1342930761977176064',
        'https://www.zhihu.com/zvideo/1975671354259968920',
    ],
    'KakaoVideoClient': [
        'http://tv.kakao.com/channel/2671005/cliplink/301965083',
        'https://tv.kakao.com/channel/2671005/cliplink/375041999',
    ],
    'YoukuVideoClient': [
        'https://v.youku.com/v_show/id_XMTgzNDQxNTkzNg==.html?spm=a2hkl.14919748_WEBHOME_HOME.scg_scroll_2.d_2_play&s=cc17d2fe962411de83b1&scm=20140719.rcmd.feed.show_cc17d2fe962411de83b1&alginfo=-1reqId-2b07ec602%204b42%204177%20aeb0%204e65d2d04e8f%231764098407663-1seqId-20IU4z6f0BTnk0zFX-1abId-2468079-1sceneId-246595&scg_id=22896328',
        'https://www.youku.com/ku/webduanju?vid=XNjQ4MzYzNTY5Ng%3D%3D&showid=afafff1a3aef4f96a2ff&spm=a2hkl.pcshortshow.feed_2.d_1_1&scm=20140689.rcmd.feed.video_XNjQ4MzYzNTY5Ng%3D%3D',
    ],
    'TencentVideoClient': [
        'https://v.qq.com/x/cover/mzc00349vqikdb0/b3535d8h2a1.html',
        'https://v.qq.com/x/cover/ygci7rbfq3celp8/S0010phisz5.html?cut_vid=i4101ucafw7&scene_id=3&start=93',
        'https://www.iflix.com/en/play/0s682hc45t0ohll/a00340c66f8-EP1%3A_Miss_Gu_Who_Is_Silent',
        # 'https://wetv.vip/en/play/air11ooo2rdsdi3-Cute-Programmer/v0040pr89t9-EP1-Cute-Programmer'
    ],
    'GeniusVideoClient': [
        'https://genius.com/videos/Halle-breaks-down-the-meaning-of-bite-your-lip',
        'https://genius.com/videos/Ashnikko-breaks-down-the-meaning-of-sticky-fingers',
    ],
    'UnityVideoClient': [
        'https://learn.unity.com/course/2d-beginner-game-sprite-flight/tutorial/set-up-your-2d-game-world?version=6.0',
        'https://learn.unity.com/course/creative-core-prototyping/tutorial/get-started-with-prototyping-3?version=6.0',
    ],
    'FoxNewsVideoClient': [
        'https://www.foxnews.com/video/6385658327112',
        'https://video.foxnews.com/v/6320653836112',
        'http://video.insider.foxnews.com/v/video-embed.html?video_id=5099377331001&autoplay=true&share_url=http://insider.foxnews.com/2016/08/25/univ-wisconsin-student-group-pushing-silence-certain-words&share_title=Student%20Group:%20Saying%20%27Politically%20Correct,%27%20%27Trash%27%20and%20%27Lame%27%20Is%20Offensive&share=true',
    ],
    'SinaVideoClient': [
        'http://video.sina.com.cn/view/250587748.html',
        'https://video.sina.com.cn/p/finance/2025-11-28/detail-infyypay7178654.d.html',
        'http://video.sina.com.cn/news/spj/topvideoes20160504/?opsubject_id=top1#250576030',
    ],
    'XuexiCNVideoClient': [
        'https://www.xuexi.cn/lgpage/detail/index.html?id=6898516301450608472',
        'https://www.xuexi.cn/lgpage/detail/index.html?id=16575802844879171560',
    ],
    'Open163VideoClient': [
        'https://open.163.com/newview/movie/free?pid=WIAL798Q9&mid=BIAL799D2',
        'https://open.163.com/newview/movie/free?pid=MEFVFM2AC&mid=MEFVGF5RU',
        'https://open.163.com/newview/movie/free?pid=CGJTHROS9&mid=SGJTHVGI2',
    ],
    'CCtalkVideoClient': [
        'https://www.cctalk.com/v/17604950351552?sid=1760494906733025',
        'https://www.cctalk.com/v/17576427071521?sid='
    ],
    'KedouVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7578412593719577899',
        'https://www.bilibili.com/video/BV11tCVBXEMf/?spm_id_from=333.337.search-card.all.click'
    ],
    'IIILabVideoClient': [
        'https://www.le.com/ptv/vplay/77953489.html',
        'https://www.youtube.com/watch?v=Nf1C1fSJG_8&list=RDMMNf1C1fSJG_8&start_radio=1',
        'https://www.facebook.com/100085919341237/videos/851834657389993/?__so__=discover&__rv__=video_home_www_loe_popular_videos',
    ],
    'SnapAnyVideoClient': [
        'https://www.youtube.com/watch?v=uZ8rxvAoFuc&list=RDuZ8rxvAoFuc&start_radio=1',
        'https://www.le.com/ptv/vplay/20137387.html',
    ],
    'GVVIPVideoClient': [
        'https://www.iqiyi.com/v_16ne2x4z6zc.html?bkt=9685_B,10000_B,9689_D,9687_B&rseat=image_1&r_area=most_popular&ht=2&r_source=1529@565@66&recArea=most_popular&rank=1&block=pca_recommend_hot_recommend&vfrm=pcw_home&ext=w:0.25495089432236995,score:0.7450883984565735,c_type:1&a=image&eventId=967dbf95d6315d75e5c4a50944a0d7bc&bstp=3&r_originl=351010512,4179785420284901&e=967dbf95d6315d75e5c4a50944a0d7bc&stype=2&r_ext=w:0.25495089432236995,score:0.7450883984565735,c_type:1&c1=2&vfrmrst=image_1&bucket=9685_B,10000_B,9689_D,9687_B&vfrmblk=pca_recommend_hot_recommend&r=2143888498822401&event_id=967dbf95d6315d75e5c4a50944a0d7bc&rpage=pcw_home&position=5',
        'https://v.qq.com/x/cover/mzc00200ss1zz0x/r4101dsk6f5.html?cut_vid=p41012zzjzo&scene_id=3&start=1455',
    ],
    'VgetVideoClient': [
        'https://www.youtube.com/watch?v=qPzZLAWuAbw&list=RDqPzZLAWuAbw&start_radio=1',
        'https://x.com/iluminatibot/status/1996651394963734976',
    ],
    'ILoveAPIVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7538145141593263403',
        'http://peiyinxiu.com/m/127066455',
    ],
    'EyepetizerVideoClient': [
        'https://home.eyepetizer.net/video/video-detail?resource_id=219143&resource_type=pgc_video',
        'https://home.eyepetizer.net/video/video-detail?resource_id=222084&resource_type=pgc_video',
        'http://www.eyepetizer.net/detail.html?udid=cfcde4e18636135d6d3f383f42a7351305ea6590&vid=14243&vc=2306',
        'https://m.eyepetizer.net/u1/video-detail?resource_type=video&video_id=14245',
    ],
    'ArteTVVideoClient': [
        'https://www.arte.tv/en/videos/127781-000-A/arte-reportage/',
        'https://www.arte.tv/en/videos/124453-003-A/masha-on-russia/'
    ],
    'XMFlvVideoClient': [
        'https://www.iqiyi.com/v_16ne2x4z6zc.html',
        'https://v.youku.com/v_show/id_XNDU3MDY3NjQ3Mg==.html?s=e2b1cec58f1546cd97dc'
    ],
    'C56VideoClient': [
        'https://www.56.com/u11/v_MTk5NjI0OTIw.html',
        'https://www.56.com/w45/play_album-aid-14385994_vid-MTYxMTUwMzky.html',
    ],
    'QZXDPToolsVideoClient': [
        'https://www.bilibili.com/video/BV1uymuBcE6D/?spm_id_from=333.1007.tianma.1-2-2.click',
        'https://www.douyin.com/user/MS4wLjABAAAAswuDtKmG0QULFeYM6qX_sqEKVOUDvEgwAVj3jGpoM6s?modal_id=6679709231748287757',
    ],
    'RedditVideoClient': [
        'https://www.reddit.com/r/videos/comments/6rrwyj/that_small_heart_attack/',
        'https://old.reddit.com/r/ketamine/comments/degtjo/when_the_k_hits/',
        'https://www.reddit.com/r/KamenRider/comments/wzqkxp/finale_kamen_rider_revice_episode_50_family_to/'
    ],
    'KuKuToolsVideoClient': [
        'https://www.bilibili.com/video/BV1epspzAERJ/?spm_id_from=333.1007.tianma.5-2-16.click',
        'https://www.xiaohongshu.com/explore/6898415f000000000403dc3b?xsec_token=ABozZxFfnIo4Jum5RDrI97yLjwD0ng6sc5_55zhZGU4gQ=&xsec_source=pc_user',
    ],
    'YouChuangVideoClient': [
        'https://www.bilibili.com/video/BV1DxCQBBE24/?spm_id_from=333.1007.tianma.2-2-5.click',
        'https://m.immomo.com/s/moment/new-share-v2/ar8198227777.html?time=1580294283&name=LpBAX+1lhEzqgkLc/ICG1w==&avatar=036495A9-5988-B90B-0CFA-C2415EAC1A3E20190912&isdaren=0&isuploader=1&from=weibo',
    ],
    'LongZhuVideoClient': [
        'https://www.bilibili.com/video/BV1DxCQBBE24/?spm_id_from=333.1007.tianma.2-2-5.click',
        'https://www.toutiao.com/video/7358202402865938953/?log_from=24fdd11d4e4e68_1765499453711'
    ],
}
PARSE_SUPPLEMENT = {
    'Ku6VideoClient': {'name': 'Ku6VideoClient', 'display_name': 'Ku6VideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'Ku6VideoClient', 'test_url': 'https://www.ku6.com/video/detail?id=McZoSe_hgG_jwzy7pQLqvMJ3IoI.', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'Ku6VideoClient', 'download_url': 'https://rbv01.ku6.com/wifi/o_1f9dtdubn8l8154lddtcdtdusm', 'title': '看到泪崩！微视频百年风华', 'file_path': 'videodl_tmp_outputs\\Ku6VideoClient\\看到泪崩！微视频百年风华.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'requests.head', 'ok': True}}}, {'name': 'Ku6VideoClient', 'test_url': 'https://www.ku6.com/video/detail?id=HE3lfhcp13Gd0qND4zfzXYQONMY.', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'Ku6VideoClient', 'download_url': 'https://rbv01.ku6.com/wifi/o_1evr90gl2sdhjs4nn31bad1v3ue', 'title': '微视频｜领航新征程', 'file_path': 'videodl_tmp_outputs\\Ku6VideoClient\\微视频｜领航新征程.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'requests.head', 'ok': True}}}]},
    'WeishiVideoClient': {'name': 'WeishiVideoClient', 'display_name': 'WeishiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'WeishiVideoClient', 'test_url': 'https://h5.weishi.qq.com/weishi/feed/76EaWNkEF1IqtfYVH/', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'WeishiVideoClient', 'download_url': 'http://v.weishi.qq.com/tjg_2012262636_1047_e167370371ca4988a45e2b0ed039vide.f30.mp4?dis_k=1ff643abe43d47772c6fcd1e0c6504c5&dis_t=1764139343&fromtag=0&pver=5.8.5&weishi_play_expire=1764182543&wsadapt=_1126144223__367349920_0_0_0_2_8_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW&wsadapt=_1126144223__367349920_0_0_0_2_0_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW', 'title': '自己烤的串，果然比外面卖的便宜又好吃！', 'file_path': 'videodl_tmp_outputs\\WeishiVideoClient\\自己烤的串，果然比外面卖的 便宜又好吃！.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': '76EaWNkEF1IqtfYVH', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'WeishiVideoClient', 'test_url': 'https://isee.weishi.qq.com/ws/app-pages/share/index.html?wxplay=1&id=7siJelmUp1MkDSPeo&spid=3704775550396963513&qua=v1_and_weishi_8.81.0_590_312026001_d&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'WeishiVideoClient', 'download_url': 'http://v.weishi.qq.com/gzc_1594_1047_0bc35eac6aaamuaip6jm7fqrp2ief7uqal2a.f70.mp4?dis_k=6cfc9fe3c0374579f29d72756e638ff0&dis_t=1764139358&fromtag=0&pver=1.0.0&weishi_play_expire=1764182558&wsadapt=_1126144238__160236066_0_0_0_27_2_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW&wsadapt=_1126144238__160236066_0_0_0_27_0_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW', 'title': '古装片，就是这样排出来的', 'file_path': 'videodl_tmp_outputs\\WeishiVideoClient\\古装片，就是这样排出来的.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': '7siJelmUp1MkDSPeo', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}]},
    'DuxiaoshiVideoClient': {'name': 'DuxiaoshiVideoClient', 'display_name': 'DuxiaoshiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'DuxiaoshiVideoClient', 'test_url': 'http://quanmin.baidu.com/sv?source=share-h5&pd=qm_share_search&vid=12474281128791424380', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'DuxiaoshiVideoClient', 'download_url': 'https://vd2.bdstatic.com/mda-rabs6zmqbg9w8ab1/720p/mv_cae264_backtrack_720p_normal/1736706974323303590/mda-rabs6zmqbg9w8ab1.mp4?pd=-1&pt=-1&cr=2&vt=0&cd=0&did=cfcd208495d565ef66e7dff9f98764da&logid=0264873267&vid=12474281128791424380&auth_key=1764142465-0-0-08bc8379f5553a95b144ab8175d62483&bcevod_channel=searchbox_feed', 'title': 'Redis分布式缓存常用命令解析', 'file_path': 'videodl_tmp_outputs\\DuxiaoshiVideoClient\\Redis分布式缓存常用命令解析.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'DuxiaoshiVideoClient', 'test_url': 'https://mbd.baidu.com/newspage/data/videolanding?nid=sv_8388278490910791594&sourceFrom=rec', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'DuxiaoshiVideoClient', 'download_url': 'https://vd9.bdstatic.com/mda-rhqnq9m87qbe70gw/mb/720p/mv_cae264_backtrack_720p_normal/1756137776222451415/mda-rhqnq9m87qbe70gw.mp4?pd=-1&pt=-1&cr=2&vt=0&cd=0&did=cfcd208495d565ef66e7dff9f98764da&logid=0280782570&vid=8388278490910791594&auth_key=1764142482-0-0-7dc2d04e37ad072c749bdf27dcbcf0f9&bcevod_channel=searchbox_feed', 'title': '天津中驰：专注声测管与注浆管生产，细节决定成败', 'file_path': 'videodl_tmp_outputs\\DuxiaoshiVideoClient\\天津中驰：专注声测管与注浆管生产，细节决定成败.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}]},
    'YouTubeVideoClient': {'name': 'YouTubeVideoClient', 'display_name': 'YouTubeVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'YouTubeVideoClient', 'test_url': 'https://music.youtube.com/watch?v=PgPhDyV0J2w&list=RDAMVMPgPhDyV0J2w', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'YouTubeVideoClient', 'download_url': '<videodl.modules.utils.youtubeutils.Stream object at 0x0000028BF67E18D0>', 'title': '【创造营人气学员】 希林娜依·高 《中国新歌声2》音乐合辑完整版 SING!CHINA S2 [浙江卫视官方HD]', 'file_path': 'videodl_tmp_outputs\\YouTubeVideoClient\\ 【创造营人气学员】 希林娜依·高 《中国新歌声2》音乐合辑完整版 SING!CHINA S2 [浙江卫视官方HD].mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'PgPhDyV0J2w', 'guess_video_ext_result': 'NULL'}}, {'name': 'YouTubeVideoClient', 'test_url': 'https://www.youtube.com/watch?v=hie-SsINu4Q&list=RDhie-SsINu4Q&start_radio=1', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'YouTubeVideoClient', 'download_url': '<videodl.modules.utils.youtubeutils.Stream object at 0x0000028BF67E1870>', 'title': "周杰倫好聽的40首歌 Best Songs Of Jay Chou 周杰倫最偉大的命中 下雨天在车里听周杰伦- 完美结合 Jay Chou's Top 40 Love Songs", 'file_path': "videodl_tmp_outputs\\YouTubeVideoClient\\周杰倫好聽 的40首歌 Best Songs Of Jay Chou 周杰倫最偉大的命中 下雨天在车里听周杰伦- 完美结合 Jay Chou's Top 40 Love Songs.mp4", 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'hie-SsINu4Q', 'guess_video_ext_result': 'NULL'}}]},
    'DuxiaoshiVideoClient': {'name': 'DuxiaoshiVideoClient', 'display_name': 'DuxiaoshiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'DuxiaoshiVideoClient', 'test_url': 'http://quanmin.baidu.com/sv?source=share-h5&pd=qm_share_search&vid=12474281128791424380', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'DuxiaoshiVideoClient', 'download_url': 'https://vd2.bdstatic.com/mda-rabs6zmqbg9w8ab1/720p/mv_cae264_backtrack_720p_normal/1736706974323303590/mda-rabs6zmqbg9w8ab1.mp4?pd=-1&pt=-1&cr=2&vt=0&cd=0&did=cfcd208495d565ef66e7dff9f98764da&logid=0651143897&vid=12474281128791424380&auth_key=1764142851-0-0-552e13f1bbb6289ab58ad686f5421643&bcevod_channel=searchbox_feed', 'title': 'Redis分布式缓存常用命令解析', 'file_path': 'videodl_tmp_outputs\\DuxiaoshiVideoClient\\Redis分布式缓存常用命令解析.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'DuxiaoshiVideoClient', 'test_url': 'https://mbd.baidu.com/newspage/data/videolanding?nid=sv_8388278490910791594&sourceFrom=rec', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'DuxiaoshiVideoClient', 'download_url': 'https://vd9.bdstatic.com/mda-rhqnq9m87qbe70gw/mb/720p/mv_cae264_backtrack_720p_normal/1756137776222451415/mda-rhqnq9m87qbe70gw.mp4?pd=-1&pt=-1&cr=2&vt=0&cd=0&did=cfcd208495d565ef66e7dff9f98764da&logid=0664547893&vid=8388278490910791594&auth_key=1764142865-0-0-01f66d1bf2f53a3778ec3a5266053e7f&bcevod_channel=searchbox_feed', 'title': '天津中驰：专注声测管与注浆管生产，细节决定成败', 'file_path': 'videodl_tmp_outputs\\DuxiaoshiVideoClient\\天津中驰：专注声测管与注浆管生产，细节决定成败.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}]},
    'YoukuVideoClient': {'name': 'YoukuVideoClient', 'display_name': 'YoukuVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'YoukuVideoClient', 'test_url': 'https://v.youku.com/v_show/id_XMTgzNDQxNTkzNg==.html?spm=a2hkl.14919748_WEBHOME_HOME.scg_scroll_2.d_2_play&s=cc17d2fe962411de83b1&scm=20140719.rcmd.feed.show_cc17d2fe962411de83b1&alginfo=-1reqId-2b07ec602%204b42%204177%20aeb0%204e65d2d04e8f%231764098407663-1seqId-20IU4z6f0BTnk0zFX-1abId-2468079-1sceneId-246595&scg_id=22896328', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'YoukuVideoClient', 'download_url': 'http://pl-ali.youku.com/playlist/m3u8?vid=XMTgzNDQxNTkzNg%3D%3D&type=mp4hd3v3&ups_client_netip=725c13f7&utid=PZatIUx1BUICAXJcE%2Fco2F6k&ccode=0564&psid=82adbc953bd657ab9eb9c5d507c5417c41346&duration=3530&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1764141118&onOff=0&encr=0&ups_key=d76ca22cf3b155d9b944df405b988a7d&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0', 'title': '努尔哈赤速写', 'file_path': 'videodl_tmp_outputs\\YoukuVideoClient\\努尔哈赤速写.m3u', 'ext': 'm3u', 'download_with_ffmpeg': True, 'err_msg': 'NULL', 'identifier': 'XMTgzNDQxNTkzNg==', 'guess_video_ext_result': {'ext': 'm3u', 'sniffer': 'requests.head', 'ok': True}}}, {'name': 'YoukuVideoClient', 'test_url': 'https://www.youku.com/ku/webduanju?vid=XNjQ4MzYzNTY5Ng%3D%3D&showid=afafff1a3aef4f96a2ff&spm=a2hkl.pcshortshow.feed_2.d_1_1&scm=20140689.rcmd.feed.video_XNjQ4MzYzNTY5Ng%3D%3D', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'YoukuVideoClient', 'download_url': 'http://pl-ali.youku.com/playlist/m3u8?vid=XNjQ4MzYzNTY5Ng%3D%3D&type=mp4hd3v3&ups_client_netip=725c13f7&utid=SpatIfN8jBsCAXJcE%2FfHxkur&ccode=0564&psid=c836dbbf04bfc2ed710ab7e058b0a0c741346&duration=190&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1764141130&onOff=0&encr=0&ups_key=ff7c8e5d2b6049d7da32d6edc4e9f4ed&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0', 'title': '我投喂了古代大将军', 'file_path': 'videodl_tmp_outputs\\YoukuVideoClient\\我投喂了古代大将军.m3u', 'ext': 'm3u', 'download_with_ffmpeg': True, 'err_msg': 'NULL', 'identifier': 'XNjQ4MzYzNTY5Ng==', 'guess_video_ext_result': {'ext': 'm3u', 'sniffer': 'requests.head', 'ok': True}}}]},
    'CCTVVideoClient': {'name': 'CCTVVideoClient', 'display_name': 'CCTVVideoClient', 'success_count': 3, 'total_count': 3, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'CCTVVideoClient', 'test_url': 'https://v.cctv.com/2021/06/05/VIDEwn0n7VRJokIL7rBi2ink210605.shtml?spm=C90324.Pfdd0SYeqktv.Eri5TUDwaTXO.6', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'CCTVVideoClient', 'download_url': 'https://dhlsaliwx01.v.cntv.cn/asp/enc/hls/main/0303000a/3/default/437ddd8637e445598511370540e48788/main.m3u8?maxbr=2048&contentid=18120319242338', 'title': '王冰冰看《新兵请入列》的反应太可爱了！', 'file_path': 'videodl_tmp_outputs\\CCTVVideoClient\\王冰冰看《新兵请入列》的反应太可爱了！.m3u8', 'ext': 'm3u8', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'download_with_ffmpeg_cctv': True, 'pid': '437ddd8637e445598511370540e48788'}}, {'name': 'CCTVVideoClient', 'test_url': 'https://tv.cctv.com/2022/04/15/VIDEYQOwJ33dIqm1h9PvmIpO220415.shtml?spm=C95797228340.P3XSH3djsU2B.0.0', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'CCTVVideoClient', 'download_url': 'https://dhlsqqwx01.v.cntv.cn/asp/enc/hls/main/0303000a/3/default/be2a31ee9fc54e808a207f8106b36ca4/main.m3u8?maxbr=2048&contentid=18120319242338', 'title': '《百家讲坛》 20220415 品读中华经典诗文 8 乐天派的人生区间', 'file_path': 'videodl_tmp_outputs\\CCTVVideoClient\\《百家讲坛》 20220415 品读中华经典诗文 8 乐天派的人生区间.m3u8', 'ext': 'm3u8', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'download_with_ffmpeg_cctv': True, 'pid': 'be2a31ee9fc54e808a207f8106b36ca4'}}, {'name': 'CCTVVideoClient', 'test_url': 'https://xczx.cctv.com/2025/11/19/ARTIhGNpDUfXpmRX0qjQ6mSC251119.shtml?spm=C73274.Pt2UfsofZQQ5.EmwSKtAQYeDI.2', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'CCTVVideoClient', 'download_url': 'https://dhlswswx01.v.cntv.cn/asp/enc/hls/main/0303000a/3/default/e26953187476490d8b7b594518646a17/main.m3u8?maxbr=2048&contentid=18120319242338', 'title': ' 《三农群英汇》 20251118 棉田守望者', 'file_path': 'videodl_tmp_outputs\\CCTVVideoClient\\《三农群英汇》 20251118 棉田守 望者.m3u8', 'ext': 'm3u8', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'download_with_ffmpeg_cctv': True, 'pid': 'e26953187476490d8b7b594518646a17'}}]},
    'TencentVideoClient': {'name': 'TencentVideoClient', 'display_name': 'TencentVideoClient', 'success_count': 3, 'total_count': 3, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'TencentVideoClient', 'test_url': 'https://v.qq.com/x/cover/mzc00349vqikdb0/b3535d8h2a1.html', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'TencentVideoClient', 'download_url': 'https://ltsxmty.gtimg.com/B_A_YRAqlJgvVaYHglAxaQJfV12w371NTSDMB-krWYTNqdJ_TeXmnDodZY1PKC6igARr6cZkSDCqub0P7XNI-Wm3lqB8EUcW5ebXuuTfolZYBPf22oEYl-HgBFgxJPhUmgcigQv8Es1S9Hw6vTR1QABA/svp_50069/82TpMcASjPjY_CU-CldVzgTPOQPFV5ro2tTzQGPd1vERRxexmqlYTyncsqAD5fnnJhdlSFyTavE9cM4l5gYEfy5oQxvKWgTuey5NJiOrEFrjPnESM6y4z-6wCjwOuTil_FlRxMkoqdRDdHy4yg3BCXMc_JncljFKIhsCtie38P09bogvCKDXI8wUxj9cwsdM/gzc_1000035_0bc3w4anyaaah4aplreqtvszln6d3s3qbxca.f306310.ts.m3u8?ver=4', 'title': '心存善意，真爱自会降临', 'file_path': 'videodl_tmp_outputs\\TencentVideoClient\\心存善意，真爱自会降临.m3u8', 'ext': 'm3u8', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 'download_with_ffmpeg_cctv': False, 'err_msg': 'NULL', 'identifier': 'mzc00349vqikdb0_b3535d8h2a1', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'TencentVideoClient', 'test_url': 'https://v.qq.com/x/cover/ygci7rbfq3celp8/S0010phisz5.html?cut_vid=i4101ucafw7&scene_id=3&start=93', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'TencentVideoClient', 'download_url': 'https://ltsxmty.gtimg.com/B_A_YRAqlJgvVaYHglAxaQJY4Lq5DKNKADEp_6QL-GYC-U85-Co4bFbnu9AjEZLxqOmuynudbBCDBNp02Ou9hDbPcRLwDWBU4kUuAGBG_DlrxnjjB60aJR8DHxKMJSA1VF_lQvo8wGU93_iGZi2QGpkQ/svp_50112/iDNu6dpkLFMvYLFNj_KzYc55AGy2fNAMjRhsG1lnZE-WYFfkURUAY6IU7qJUd-E9KbfDguY8uAGXeIBouhkHE3iPO6dKnPcfC8xoIto6yqjgBai3tBL1R3_2Y2bQCQrtXkeIzoADfONd92Yh0bkj4cUQKvdbxVEX9x1_XyiZjAo7ppswU8xvKNaxP56VT8iH/gzc_1000102_0b53wmaaaaaa2maizlvj5brmbm6dac2qabca.f322063.ts.m3u8?ver=4', 'title': '罗小黑战记Cat.4《飘》', 'file_path': 'videodl_tmp_outputs\\TencentVideoClient\\罗小黑战记Cat.4《飘》.m3u8', 'ext': 'm3u8', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 'download_with_ffmpeg_cctv': False, 'err_msg': 'NULL', 'identifier': 'ygci7rbfq3celp8_S0010phisz5', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'TencentVideoClient', 'test_url': 'https://www.iflix.com/en/play/0s682hc45t0ohll/a00340c66f8-EP1%3A_Miss_Gu_Who_Is_Silent', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'TencentVideoClient', 'download_url': 'https://cffaws.wetvinfo.com/svp_50112/01E5392356207F85E8A31495503D25600828F9A33A68FA9E386C104D5EF3299380673158C9907CB0A845CA7210AC39664316C92A33594319519C963AF22F6AE4662FFDE0AB50855573E092434F4BEFC8C79CC53F8788B690F24A0AF4712A87B61C77E614E2F987D631A69D4D0ADF905F16018B8F33FFF30F859DDB13DBDC1967B5/gzc_1000102_0b53wqabkaaayyamu5pa2vrmbngdcw4aaeca.f323013.ts.m3u8?ver=4', 'title': 'EP1 Miss Gu Who Is Silent', 'file_path': 'videodl_tmp_outputs\\TencentVideoClient\\EP1 Miss Gu Who Is Silent.m3u8', 'ext': 'm3u8', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 'download_with_ffmpeg_cctv': False, 'err_msg': 'NULL', 'identifier': '0s682hc45t0ohll_a00340c66f8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}}}]},
    'GeniusVideoClient': {'name': 'GeniusVideoClient', 'display_name': 'GeniusVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'GeniusVideoClient', 'test_url': 'https://genius.com/videos/Halle-breaks-down-the-meaning-of-bite-your-lip', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'GeniusVideoClient', 'download_url': 'http://house-fastly-signed-us-east-1-prod.brightcovecdn.com/media/v1/pmp4/static/clear/4863540648001/961d8e32-d67f-4573-8ee1-33a9769e1091/ed93d7cf-6e1e-4b60-b295-ccaf5d36d5c2/main.mp4?fastly_token=Njk0ZGZhN2RfMmExNWQ5ZDI4YWZiYjgyZmQzOTE1NGY4NWU2Y2Y5YzgxOTFmZTc2NDkwNmQ2NmE1OGE3YmQxMTUxMTg2MTcyZF8vL2hvdXNlLWZhc3RseS1zaWduZWQtdXMtZWFzdC0xLXByb2QuYnJpZ2h0Y292ZWNkbi5jb20vbWVkaWEvdjEvcG1wNC9zdGF0aWMvY2xlYXIvNDg2MzU0MDY0ODAwMS85NjFkOGUzMi1kNjdmLTQ1NzMtOGVlMS0zM2E5NzY5ZTEwOTEvZWQ5M2Q3Y2YtNmUxZS00YjYwLWIyOTUtY2NhZjVkMzZkNWMyL21haW4ubXA0', 'title': 'Halle-breaks-down-the-meaning-of-bite-your-lip', 'file_path': 'videodl_tmp_outputs\\GeniusVideoClient\\Halle-breaks-down-the-meaning-of-bite-your-lip.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 'download_with_ffmpeg_cctv': False, 'err_msg': 'NULL', 'identifier': '6385323870112', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'GeniusVideoClient', 'test_url': 'https://genius.com/videos/Ashnikko-breaks-down-the-meaning-of-sticky-fingers', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'GeniusVideoClient', 'download_url': 'http://house-fastly-signed-us-east-1-prod.brightcovecdn.com/media/v1/pmp4/static/clear/4863540648001/eaba2f9f-7980-441b-a5ed-9e4cfda46597/a88de6e6-02e9-48e9-a5d9-969c31fb778b/main.mp4?fastly_token=Njk0ZGZhMTJfYTBlOTU5NDZlMGY3ZjIyMDUxY2I0NDkxY2ZkODMzOWM4ODU0YjJlZDJiYmM2NjczNmEzOGQxMjlmZDAxYzUxMV8vL2hvdXNlLWZhc3RseS1zaWduZWQtdXMtZWFzdC0xLXByb2QuYnJpZ2h0Y292ZWNkbi5jb20vbWVkaWEvdjEvcG1wNC9zdGF0aWMvY2xlYXIvNDg2MzU0MDY0ODAwMS9lYWJhMmY5Zi03OTgwLTQ0MWItYTVlZC05ZTRjZmRhNDY1OTcvYTg4ZGU2ZTYtMDJlOS00OGU5LWE1ZDktOTY5YzMxZmI3NzhiL21haW4ubXA0', 'title': 'Ashnikko-breaks-down-the-meaning-of-sticky-fingers', 'file_path': 'videodl_tmp_outputs\\GeniusVideoClient\\Ashnikko-breaks-down-the-meaning-of-sticky-fingers.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'download_with_aria2c': False, 'download_with_ffmpeg_cctv': False, 'err_msg': 'NULL', 'identifier': '6384979708112', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}]},
}


'''runningingithubactions'''
def runningingithubactions() -> bool:
    return (
        os.getenv("GITHUB_ACTIONS", "").lower() == "true"
        and os.getenv("CI", "").lower() == "true"
    )


'''makepreviewvideo'''
def makepreviewvideo(sample_idx: int, sample: dict, base_dir: str):
    client_name = sample["name"]
    client_cls = VideoClientBuilder.REGISTERED_MODULES.get(client_name)
    if client_cls is None:
        print(f"[Preview] No client class for {client_name}, skip.")
        return None
    client: BaseVideoClient = client_cls(work_dir=WORK_DIR)
    video_info = dict(sample["parse_result"])
    print(f"[Preview] Downloading via {client_name}: {sample['test_url']}")
    try:
        video_info = client.download([video_info])[0]
    except Exception as err:
        print(f"[Preview] client.download failed: {err!r}")
    src_path = video_info.get("file_path")
    download_url = video_info.get("download_url")
    if src_path and os.path.exists(src_path):
        input_spec = src_path
    elif download_url and download_url != "NULL":
        input_spec = download_url
    else:
        print("[Preview] No valid input for ffmpeg, skip this sample.")
        return None
    base_dir_path = Path(base_dir)
    videos_dir = base_dir_path / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    out_filename = f"sample_{sample_idx}.mp4"
    out_path = videos_dir / out_filename
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(input_spec), "-t", str(MAX_PREVIEW_DURATION), "-vf", "scale=-2:480", "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "28", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out_path),
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except Exception as err:
        print(f"[Preview] ffmpeg failed: {err!r}")
        return None
    public_path = f"{base_dir_path.name}/videos/{out_filename}"
    print(f"[Preview] Preview video written to {public_path}")
    return public_path


'''runcheck'''
def runcheck(output_path: str):
    # prepare
    out_dir = os.path.dirname(output_path)
    if out_dir: os.makedirs(out_dir, exist_ok=True)
    result = {"generated_at": datetime.now(timezone.utc).isoformat(), "clients": []}
    all_success_samples: list[dict] = []
    # iter to check (some websites limit github action server access, we use the backup information to replace)
    for client_name, client_cls in list(VideoClientBuilder.REGISTERED_MODULES.items()):
        sample_urls = VIDEODL_TEST_SAMPLES.get(client_name)
        if not sample_urls:
            print(f"[Skip] {client_name}: no test samples configured.")
            continue
        print(f"\n[Module] {client_name}")
        if client_name in PARSE_SUPPLEMENT and runningingithubactions():
            client_entry = PARSE_SUPPLEMENT[client_name]
            success_count, total_count, status_tag = client_entry['success_count'], client_entry['total_count'], client_entry['status']
        else:
            client: BaseVideoClient = client_cls(work_dir=WORK_DIR)
            tests, success_count, total_count = [], 0, 0
            for url in sample_urls:
                total_count += 1
                status = {"name": client_name, "test_url": url, "ok": False, "err_msg": None, "parse_result": {}}
                try:
                    video_infos = client.parsefromurl(url)
                    video_info = video_infos[0] if video_infos else {}
                    video_info.pop('raw_data')
                    status["parse_result"] = video_info or {}
                    download_url = (video_info or {}).get("download_url")
                    err_msg = (video_info or {}).get("err_msg")
                    ok = bool(download_url and download_url != "NULL" and (not err_msg or err_msg == "NULL"))
                    status["ok"] = ok
                    status["err_msg"] = err_msg
                except Exception as err:
                    status["ok"] = False
                    status["err_msg"] = repr(err)
                if status["ok"]:
                    success_count += 1
                    if client_name not in ['YinyuetaiVideoClient']:
                        all_success_samples.append({"name": client_name, "test_url": status["test_url"], "ok": True, "err_msg": status["err_msg"], "parse_result": status["parse_result"]})
                tests.append(status)
                time.sleep(10 + random.randint(1, 5))
            if total_count == 0: continue
            if success_count == total_count: status_tag = "ok"
            elif success_count > 0: status_tag = "partial"
            else: status_tag = "fail"
            client_entry = {
                "name": client_name, "display_name": client_name, "success_count": success_count, "total_count": total_count, 
                "success_rate": success_count / total_count, "status": status_tag, "tests": tests,
            }
        print(
            f"  Parsed video urls: {success_count}/{total_count} "
            f"(status={status_tag})"
        )
        result["clients"].append(client_entry)
    # random select some videos to download for showing
    if all_success_samples:
        random.shuffle(all_success_samples)
        chosen = all_success_samples[:3]
        preview_samples = []
        base_dir = os.path.dirname(output_path) or "."
        for sample_idx, sample in enumerate(chosen):
            public_video = makepreviewvideo(sample_idx, sample, base_dir)
            sample_out = dict(sample)
            if public_video: sample_out["local_video"] = public_video
            preview_samples.append(sample_out)
        result["random_samples"] = preview_samples
    # save results
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    output_path_daily = os.path.join(os.path.dirname(output_path), f'videodl_{datetime.now().strftime("%Y-%m-%d")}.json')
    with open(output_path_daily, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nSaved test results to {output_path} and {output_path_daily}")
    shutil.rmtree(WORK_DIR, ignore_errors=True)


'''main'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", default="daily_test_results/videodl_status.json",  help="Path to save JSON status file.")
    args = parser.parse_args()
    runcheck(args.output)


'''tests'''
if __name__ == "__main__":
    main()