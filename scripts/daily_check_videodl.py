'''
Function:
    Implementation of Auto Daily Checking For Videodl + Small Preview Videos
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
from videodl.modules import VideoClientBuilder, BaseVideoClient, VideoInfo


'''constants'''
WORK_DIR = 'videodl_tmp_outputs'
MAX_PREVIEW_DURATION = 30
VIDEODL_TEST_SAMPLES = {
    'WebMediaGrabber': [
        'https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video',
        'https://download.samplelib.com/mp4/sample-5s.mp4',
        'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8',
        'https://www.w3schools.com/html/html5_video.asp',
    ],
    'AcFunVideoClient': [
        'https://www.acfun.cn/v/ac29566205', 
        'https://www.acfun.cn/v/ac47998293', 
        'https://www.acfun.cn/v/ac36491489',
    ],
    'HaokanVideoClient': [
        'https://haokan.baidu.com/v?vid=7754398076535398724',
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
        'https://www.ku6.com/video/detail?id=HE3lfhcp13Gd0qND4zfzXYQONMY.',
    ],
    'KuaishouVideoClient': [
        'https://www.kuaishou.com/short-video/3xwzr5dveyqc5fa?authorId=3xv7d3j7hqqpksi', 
        'https://www.kuaishou.com/short-video/3xjpwzyparcgnck?authorId=3xbbsmxr7cdmhqs',
        'https://www.kuaishou.com/short-video/3x5k4yswvs3k9r9?authorId=3x9uj94tctww7fy',
        'https://v.kuaishou.com/8qIlZu',
    ],
    'BilibiliVideoClient': [
        'https://www.bilibili.com/video/BV16Z4y1X784/?spm_id_from=333.851.b_7265636f6d6d656e64.2', 
        'https://www.bilibili.com/video/BV1KZgHzJEs6/?spm_id_from=333.337.search-card.all.click',
        'https://www.bilibili.com/video/BV13x41117TL',
        'https://www.bilibili.com/video/BV1bK411W797?p=1',
        'https://www.bilibili.com/video/av8903802/',
        'https://www.bilibili.com/video/av114868162141203',
        'https://www.bilibili.com/festival/bh3-7th?bvid=BV1tr4y1f7p2&',
        'https://www.bilibili.com/festival/2023honkaiimpact3gala?bvid=BV1ay4y1d77f',
        'https://www.bilibili.com/bangumi/play/ep21495',
        'https://www.bilibili.com/bangumi/play/ep345120',
        'https://www.bilibili.com/bangumi/play/ss26801',
        'https://www.bilibili.com/cheese/play/ep229832',
    ],
    'YinyuetaiVideoClient': [
        'https://www.yinyuetai.com/watch/7200480383631265792?listType=swiper&listId=6998475633361805312'
    ],
    'BaiduTiebaVideoClient': [
        'https://tieba.baidu.com/p/7280373361',
        'https://tieba.baidu.com/p/10253039554',
        'https://tieba.baidu.com/p/10196228633',
    ],
    'MGTVVideoClient': [
        'https://www.mgtv.com/l/100026064/19868457.html?fpa=1684&fpos=&lastp=ch_home&cpid=5',
        'https://www.mgtv.com/b/788366/23780111.html?fpa=1756&fpos=&lastp=ch_home', # requires pass VIP login-in cookies by default_parse_cookies and default_download_cookies to download full video
        'https://www.mgtv.com/b/805972/23756299.html?fpa=1261&fpos=&lastp=ch_home&cpid=5', # requires pass login-in cookies by default_parse_cookies and default_download_cookies to download full video
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
        'http://www.meipai.com/media/6983711035636086653',
        'https://www.meipai.com/media/6977515645069710577',
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
        'https://www.xinpianchang.com/a13626197',
        'https://www.xinpianchang.com/a13536060',
        'https://www.xinpianchang.com/a13419465',
        'https://www.xinpianchang.com/a11879903',
        'https://stock.xinpianchang.com/footage/details/FpS51ArjiWww7g.html',
        'https://stock.xinpianchang.com/footage/details/EbL20T4Nee9ZOq.html',
    ],
    'WeSingVideoClient': [
        'https://kg.qq.com/node/user/bb132c338e/song/play-edLkcwAsRj?s=bCyoDlbCUhcjXbkQ&shareuid=&topsource=znxvljkwehoit_rqojkwehfguioqef_fnajkgfb&g_f=',
        'https://kg.qq.com/node/play?s=WYsF1AWj1UTvLWXu&g_f=personal&appsource=&pageId=personalH5'
    ],
    'XiguaVideoClient': [
        'https://www.ixigua.com/7336388303266152970',
        'https://www.ixigua.com/7356542118082380340',
        'https://www.ixigua.com/7357374222072545830',
        'https://www.ixigua.com/7114823820632031752',
    ],
    'WeiboVideoClient': [
        'https://weibo.com/tv/show/1034:5234817776943232?mid=5234851004547318',
        'https://m.weibo.cn/detail/5234820306442377',
        'https://m.weibo.cn/detail/5249667961979398',
        'https://weibo.com/tv/v/HApWK8FAc?fid=1034:4386795211940756',
    ],
    'RednoteVideoClient': [
        'http://xhslink.com/o/4aeC2uNASel',
        'http://xhslink.com/o/4CKj0aSSeO9',
        'http://xhslink.com/o/8t08X6dROt5',
        'http://xhslink.com/o/1lB9dX0Vt2t',
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
        'https://tv.kakao.com/channel/2671005/cliplink/302362342?playlistId=70284&metaObjectType=Playlist',
    ],
    'YoukuVideoClient': [
        'https://v.youku.com/v_show/id_XNDU1MTg1NjM2OA==',
        'https://v.youku.com/v_show/id_XNDA4MjA3ODA4.html?s=cbfd4dee962411de83b1&scm=20140719.apircmd.298496.video_XNDA4MjA3ODA4&spm=a2hkt.13141534.1_7.d_1_1',
        'https://www.youku.com/ku/webduanju?vid=XNjQ4MzYzNTY5Ng%3D%3D&showid=afafff1a3aef4f96a2ff&spm=a2hkl.pcshortshow.feed_2.d_1_1&scm=20140689.rcmd.feed.video_XNjQ4MzYzNTY5Ng%3D%3D',
        'https://v.youku.com/v_show/id_XNjQyOTgxMzQ2OA==.html',
    ],
    'TencentVideoClient': [
        'https://v.qq.com/x/cover/mzc00349vqikdb0/b3535d8h2a1.html',
        'https://v.qq.com/x/cover/ygci7rbfq3celp8/S0010phisz5.html?cut_vid=i4101ucafw7&scene_id=3&start=93',
        'https://www.iflix.com/en/play/0s682hc45t0ohll/a00340c66f8-EP1%3A_Miss_Gu_Who_Is_Silent',
        'https://www.iflix.com/play/0s682hc45t0ohll',
        'https://v.qq.com/x/cover/nhtfh14i9y1egge/d00249ld45q.html',
        'https://v.qq.com/x/cover/nhtfh14i9y1egge.html',
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
        'https://www.bilibili.com/bangumi/play/ep371068',
        'https://www.bilibili.com/video/BV16wiiBsE6u/?spm_id_from=333.1007.tianma.2-1-4.click',
        'https://www.douyin.com/jingxuan?modal_id=7507549841271147795',
        'https://www.facebook.com/100028981631678/videos/2151294341944888/?__so__=discover&__rv__=video_home_www_loe_popular_videos',
    ],
    'IIILabVideoClient': [
        'https://www.youtube.com/watch?v=Oi2261-l7nY&list=RDIBT0_3QUy98&index=4',
        'https://www.le.com/ptv/vplay/77916175.html#vid=77916175', 
        'https://x.com/NASA/status/2008604593941336381',
        'https://www.facebook.com/100085919341237/videos/851834657389993/?__so__=discover&__rv__=video_home_www_loe_popular_videos',
    ],
    'SnapAnyVideoClient': [
        'https://www.youtube.com/watch?v=kSeevdvySHg',
        'https://www.douyin.com/jingxuan?modal_id=7573166287598243082',
        'https://www.tiktok.com/@demi.support/video/7571066050851147028?lang=en',
        'https://x.com/NASA/status/2008665423936397363'
    ],
    'GVVIPVideoClient': [
        'https://www.iqiyi.com/v_16ne2x4z6zc.html?bkt=9685_B,10000_B,9689_D,9687_B&rseat=image_1&r_area=most_popular&ht=2&r_source=1529@565@66&recArea=most_popular&rank=1&block=pca_recommend_hot_recommend&vfrm=pcw_home&ext=w:0.25495089432236995,score:0.7450883984565735,c_type:1&a=image&eventId=967dbf95d6315d75e5c4a50944a0d7bc&bstp=3&r_originl=351010512,4179785420284901&e=967dbf95d6315d75e5c4a50944a0d7bc&stype=2&r_ext=w:0.25495089432236995,score:0.7450883984565735,c_type:1&c1=2&vfrmrst=image_1&bucket=9685_B,10000_B,9689_D,9687_B&vfrmblk=pca_recommend_hot_recommend&r=2143888498822401&event_id=967dbf95d6315d75e5c4a50944a0d7bc&rpage=pcw_home&position=5',
        'https://v.qq.com/x/cover/mzc00200ss1zz0x/r4101dsk6f5.html?cut_vid=p41012zzjzo&scene_id=3&start=1455',
    ],
    'VgetVideoClient': [
        'https://www.le.com/ptv/vplay/77905922.html#vid=77905922',
        'https://x.com/iluminatibot/status/1996651394963734976',
        'https://v.youku.com/v_show/id_XNjQ0ODIxMzg1Mg==.html',
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
        'https://v.youku.com/v_show/id_XNDU3MDY3NjQ3Mg==.html?s=e2b1cec58f1546cd97dc',
        'https://v.qq.com/x/cover/mzc00200t8ofhws/u41011qyvur.html',
        'https://v.qq.com/x/cover/mzc00200c1keuqc/y4101dz2uja.html',
    ],
    'C56VideoClient': [
        'https://www.56.com/u11/v_MTk5NjI0OTIw.html',
        'https://www.56.com/w45/play_album-aid-14385994_vid-MTYxMTUwMzky.html',
    ],
    'QZXDPToolsVideoClient': [
        'https://www.bilibili.com/video/BV1uymuBcE6D/?spm_id_from=333.1007.tianma.1-2-2.click',
        'https://www.douyin.com/user/MS4wLjABAAAAswuDtKmG0QULFeYM6qX_sqEKVOUDvEgwAVj3jGpoM6s?modal_id=6679709231748287757',
        'https://www.huya.com/video/play/1090411452.html',
        'https://v.6.cn/profile/watchMini.php?vid=7359943',
        'https://h5.pipix.com/s/hukXsy/',
    ],
    'RedditVideoClient': [
        'https://www.reddit.com/r/videos/comments/6rrwyj/that_small_heart_attack/',
        'https://old.reddit.com/r/ketamine/comments/degtjo/when_the_k_hits/',
        'https://www.reddit.com/r/KamenRider/comments/wzqkxp/finale_kamen_rider_revice_episode_50_family_to/'
    ],
    'KuKuToolVideoClient': [
        'https://www.tiktok.com/@swag2632w32/video/7589066360295017750?lang=en',
        'https://www.bilibili.com/bangumi/play/ep2550182',
        'https://www.bilibili.com/video/BV19ai2BCEnm/?spm_id_from=333.1007.tianma.7-3-25.click',
        'https://www.xiaohongshu.com/explore/6943e2c9000000001e00d46b?xsec_token=ABfgTE82ram6ZRhJHZt40YSxfkFQAVx79di0NPVMyarUM=&xsec_source=pc_feed', # will expire
        'https://www.douyin.com/jingxuan?modal_id=7563478365211987259',
    ],
    'LongZhuVideoClient': [
        'https://www.bilibili.com/video/BV1DxCQBBE24/?spm_id_from=333.1007.tianma.2-2-5.click',
        'https://share.xiaochuankeji.cn/hybrid/share/post?pid=415655156'
    ],
    'XiazaitoolVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7509062795342728500',
        'https://www.tiktok.com/@disneymusic/video/7589346194372037943?lang=en',
        'https://www.toutiao.com/video/7588799178684252691/',
    ],
    'NoLogoVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7501640534811233594',
        'https://www.bilibili.com/video/BV1amvZBuE7d/?spm_id_from=333.1007.tianma.1-2-2.click',
        'https://www.kuaishou.com/short-video/3x94xdt5zvg26x9?authorId=3x6fxie2rn8ciai&streamSource=find&area=homexxbrilliant',
    ],
    'SnapWCVideoClient': [
        'https://www.youtube.com/watch?v=Oz-Pak0YgJM',
        'https://www.youtube.com/watch?v=8EA71rLoY5s',
        'https://www.douyin.com/jingxuan?modal_id=7579947240421084426',
        'https://www.tiktok.com/@stars2kin.1/video/7590051214277053709?lang=en',
        'https://www.bilibili.com/video/BV1ociCBMEbJ/',
    ],
    'WWEVideoClient': [
        'https://www.wwe.com/videos/daniel-bryan-vs-andrade-cien-almas-smackdown-live-sept-4-2018', 
        'https://www.wwe.com/videos/full-match-damian-priest-rhea-ripley-conquer-aleister-black-zelina-vega-smackdown-highlights'
    ],
    'BugPkVideoClient': [
        'https://www.bilibili.com/video/BV1Ecm7BYECL/?vd_source=1e2322dafd39d0d1fd29f32c8a02ef61',
        'https://share.xiaochuankeji.cn/hybrid/share/post?pid=415662469',
        'https://weibo.com/tv/show/1034:5272829806182433?mid=5272830083338918',
    ],
    'ZanqianbaVideoClient': [
        'https://www.bilibili.com/bangumi/play/ep396009',
        'https://www.bilibili.com/video/BV1XhSKBFE5Q/?spm_id_from=333.1007.tianma.1-2-2.click',
        'https://www.toutiao.com/video/7585120439421108278/?log_from=33b1706a090018_1766131556972',
    ],
    'QingtingVideoClient': [
        'https://www.xiaohongshu.com/explore/6949dd4d000000001e028b9e?xsec_token=ABIyOqubVaiYv0bO_esnHROFBfG9cnxfaBfmGf9UFegSY=&xsec_source=pc_feed&source=404', # will expire
        'https://www.bilibili.com/video/BV1wRqrB7EkZ/?spm_id_from=333.1007.tianma.1-1-1.click',
        'https://www.douyin.com/jingxuan/theater?modal_id=7580778868509933947',
        'https://www.kuaishou.com/short-video/3x5a3tcqjss9sgw?authorId=3xna23q7fq2jn4i&streamSource=brilliant&hotChannelId=00&area=brilliantxxcarefully',
    ],
    'BVVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7558318672603991354',
        'https://www.tiktok.com/@j4y273/video/7582553332242271510',
        'https://www.toutiao.com/video/7457844322080129575/?log_from=86191c4a8551d8_1766485443453',
    ],
    'IQiyiVideoClient': [
        'https://www.iqiyi.com/v_1wc7muawbrc.html',
        'https://www.iqiyi.com/v_1y6z93cf2qw.html', # VIP video requires passing VIP user cookies to obtain full videos
    ],
    'M1905VideoClient': [
        'https://www.1905.com/video/play/1751538.shtml',
        'https://www.1905.com/vod/play/1573197.shtml?fr=vodhome_zxdp_tj',
        'https://vip.1905.com/play/535547.shtml',
        'https://www.1905.com/mdb/film/2245563',
        'https://www.1905.com/vod/play/1287886.shtml',
    ],
    'VideoFKVideoClient': [
        'https://www.bilibili.com/video/BV1jRADz8Eze/?spm_id_from=333.1007.tianma.1-2-2.click',
        'https://www.douyin.com/jingxuan?modal_id=7584054905644518690',
        'https://www.tiktok.com/@konbini/video/7556989514065939714?lang=en',
        'https://www.facebook.com/facebook/videos/facebook-blue-never-looked-so-good-video-by-molchanovamuamusic-by-fausto-papetti/1185846950029459/',
    ],
    'XCVTSVideoClient': [
        'https://v.douyin.com/irwsqD47/',
        'https://v.kuaishou.com/8CU76w',
    ],
    'KIT9VideoClient': [
        'http://v.douyin.com/JYthvL6/',
        'https://www.bilibili.com/video/BV1EEBiBhEDq/?spm_id_from=333.1007.tianma.13-2-48.click',
        'https://news.qq.com/rain/a/20251004V02NZ800',
        'https://ur.alipay.com/_nv7gnPJyDqjLbrPM9Dul7',
        'https://show.meitu.com/detail?feed_id=6873229026351926275',
        'https://www.bilibili.com/video/BV1eQYwzwEz4',
        'https://ishare.ifeng.com/c/vs/v006uROwi--XAO9zMVtJUUewd8gnoa2qfWilMSzGxeoAPn7lWjN87mNtuzWQFWWXIvGIc?spss=np&crowdid=7355482289721053225&recallChannel=&aman=fgr0432r3rMfgMeQ04UODIR0Mj8M0N6TUyrNTBdkZjWYy1x00v',
    ],
    'XZDXVideoClient': [
        'https://www.bilibili.com/video/BV12oS5B5Eye/?spm_id_from=333.1007.tianma.6-4-22.click',
        'https://www.douyin.com/jingxuan?modal_id=7585277829261151542',
        'https://www.kuaishou.com/short-video/3xd8b4qa8vtn6ie?authorId=3xmup9yp228r3ze&streamSource=find&area=homexxbrilliant',
    ],
    'PVVideoClient': [
        'https://www.youtube.com/watch?v=lBNYpPmjH8M',
        'https://www.bilibili.com/video/BV1vjmYBqETJ',
        'https://www.le.com/ptv/vplay/77974953.html',
        'https://www.douyin.com/jingxuan?modal_id=7585502221816155451',
        'https://www.facebook.com/facebook/videos/paint-me-like-one-of-your-facebook-reels-video-by-sams-sketchbooksmusic-by-conni/9879297875528418/',
    ],
    'MiZhiVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7592623211763718287',
        'https://share.xiaochuankeji.cn/hybrid/share/post?pid=415744765',
        'https://v.6.cn/minivideo/7466460',
    ],
    'CCCVideoClient': [
        'https://media.ccc.de/v/30C3_-_5443_-_en_-_saal_g_-_201312281830_-_introduction_to_processor_design_-_byterazor#video',
        'https://media.ccc.de/v/denog17-75209-evpn-flex-cross-connect-l2-p2p-vpns-can-be-agile-as-well#t=1',
    ],
    'RayVideoClient': [
        'https://www.youtube.com/watch?v=a0AyNzV3yk8',
        'https://www.bilibili.com/video/BV1fiiuBjEPH/',
        'https://www.bilibili.com/bangumi/play/ep247270',
        'https://www.douyin.com/jingxuan?modal_id=7585180912409726259',
        'https://www.miguvideo.com/p/detail/759959727',
    ],
    'SENJiexiVideoClient': [
        'https://v.qq.com/x/cover/mzc00200ezim4vr.html',
        'https://www.iqiyi.com/v_rmbopj0g60.html',
        'https://v.youku.com/v_show/id_XNjUwMjQxMjI0MA==.html',
        'https://v.pptv.com/show/31nibfeVLuiclc2kI.html',
        'https://www.mgtv.com/b/292920/3592322.html',
    ],
    'LvlongVideoClient': [
        'https://v.qq.com/x/cover/hcx1ffsjpj63xuj/e0024mhahej.html',
        'https://v.qq.com/x/cover/yg5drpt31xz2a1v/u4101uxlr02.html',
    ],
    'ODwonVideoClient': [
        'https://www.bilibili.com/video/BV1abi9BfEZU',
        'https://www.douyin.com/video/6982497745948921092',
        'https://www.kuaishou.com/short-video/3xn2uj6cstk6qts?authorId=3xgyzwvca7pq3pi',
        'https://www.xinpianchang.com/a11879902?from=articlePageOther',
    ],
    'IM1907VideoClient': [
        'http://www.iqiyi.com/v_19rrk4egc4.html',
        'https://v.qq.com/x/cover/iksywx0zzdetobi/r003073v399.html',
        'https://v.youku.com/v_show/id_XNjUxOTA0MzE4MA==.html',
        'https://www.mgtv.com/b/823245/24067596.html',
        'https://www.bilibili.com/bangumi/play/ss12548',
    ],
    'PlusFIFAVideoClient': [
        "https://www.plus.fifa.com/en/player/580e692e-e8fc-4ad1-a649-5ec0af83f94d?catalogId=5f24e303-ff42-499f-9d7a-b4f8e0eff2ce",
        "https://www.plus.fifa.com/en/content/fc-sochaux-montbeliard-vs-lb-chateauroux/6ff75563-c6fc-4b08-b324-54771dbd7029",
    ],
    'WittyTVVideoClient': [
        "https://www.wittytv.it/amici/giovedi-22-gennaio-il-quotidiano-di-amici/",
        "https://www.wittytv.it/ce-posta-per-te/quarta-puntata-sabato-3-febbraio/",
    ],
    'KugouMVVideoClient': [
        'https://www.kugou.com/mv/8cwxy96/',
        'https://www.kugou.com/mv/8gtun15/',
    ],
    'AnyFetcherVideoClient': [
        'https://www.youtube.com/watch?v=093JOWo1vqE',
        'https://www.bilibili.com/bangumi/play/ep165004',
        'https://www.bilibili.com/video/BV1d4BfBpENe',
        'https://www.douyin.com/jingxuan?modal_id=7577970216932609315',
        'https://www.tiktok.com/@ddlovato/video/7593447593493941559?lang=en',
    ],
    'DouyinVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7584665891071282432',
        'https://www.douyin.com/jingxuan?modal_id=7568524426870951219',
        'https://v.douyin.com/iLYNG8vA/',
        'https://v.douyin.com/JdngHhh/',
    ],
    'GVVideoClient': [
        'https://www.youtube.com/watch?v=-xFD19QwpsE',
        'https://www.xinpianchang.com/a11345150',
        'https://www.facebook.com/100083172190201/videos/1238024418444953',
        'https://www.instagram.com/reel/DVbPL2cgLrA/',
        'https://www.bilibili.com/video/BV1S5PrzZE16/?spm_id_from=333.1007.tianma.1-1-1.click',
        'https://www.dongchedi.com/video/7585761929667346968',
    ],
    'DongchediVideoClient': [
        'https://www.dongchedi.com/video/7595864547580658200',
        'https://www.dongchedi.com/video/7556176281977602606',
        'https://www.dongchedi.com/video/7498933469267952137',
        'https://www.dongchedi.com/video/7589928965104517656',
    ],
    'XiaolvfangVideoClient': [
        'https://www.bilibili.com/video/BV17KZKBdEQ3',
        'https://www.tiktok.com/@pet_statione/video/7579841364599328013?lang=en',
        'https://www.douyin.com/jingxuan?modal_id=7612988083125980479',
        'https://www.instagram.com/reel/DP39IRyAXRo/',
        'https://www.kuaishou.com/short-video/3x48szncmg4xcqe?authorId=3x9w4thv6im6ne4&streamSource=samecity&area=homexxnearby',
        'https://weibo.com/tv/show/1034:5271766164242555?mid=5271766441395892',
        'https://m.oasis.weibo.cn/v1/h5/share?sid=4506676592820518',
    ],
    'BeaconVideoClient': [
        'https://beacon.tv/content/welcome-to-beacon',
        'https://beacon.tv/content/draw-your-weapons-trailer',
    ],
    'ABCVideoClient': [
        'https://www.abc.net.au/btn/classroom/wwi-centenary/10527914',
        'https://www.abc.net.au/btn/classroom/climate-whiplash/106487762',
        'https://www.abc.net.au/btn/classroom/roblox-safety/106351518',
        'https://www.abc.net.au/news/2023-06-25/wagner-boss-orders-troops-back-to-bases-to-avoid-bloodshed/102520540',
    ],
    'TBNUKVideoClient': [
        "https://watch.tbn.uk/watch/replay/53253478",
        "https://watch.tbn.uk/watch/vod/52157303/identity-and-belonging",
        "https://watch.tbn.uk/shows/c171a631-ca92-4715-9df4-51567542481c/the-sessions-with-cynthia-garrett",
        "https://watch.tbn.uk/shows/906eb770-23de-4fc7-a369-e87167a5256d/praise-uk",
        "https://watch.tbn.uk/live/1197",
    ],
    'WoofVideoClient': [
        'https://www.instagram.com/reel/DWAGcteCVar/',
        'https://bsky.app/profile/atrupar.com/post/3mhdmjwygsd2e',
        'https://www.dailymotion.com/video/xa26uyo',
    ],
    'QwkunsVideoClient': [
        'https://www.instagram.com/reel/DV6qXd0CVgB/',
        'https://bsky.app/profile/atrupar.com/post/3mhdsmy4coo2p',
        'https://www.tiktok.com/@marianpaulineflores/video/7617021651158387975',
        'https://www.dailymotion.com/video/x9h93bs',
    ],
    'SpapiVideoClient': [
        'https://www.douyin.com/jingxuan?modal_id=7617448838516854050',
        'https://www.kuaishou.com/short-video/3xnpsz4qp2hgy9k?authorId=3xvs4y8pb2ki74g&streamSource=samecity&area=homexxnearby',
        'https://www.bilibili.com/video/BV1D5Q6BdEAM/',
    ],
    'JXM3U8VideoClient': [
        'https://v.youku.com/v_show/id_XMzAzMDkyMjUyOA==.html',
        'https://v.qq.com/x/cover/mzc00200rx67svy/q410050ws4m.html',
        'https://www.iqiyi.com/v_xkt6z3z798.html',
    ],
    'PlayerPLVideoClient': [
        "https://player.pl/filmy-online/1800-gramow,169874",
        "https://player.pl/filmy-online/podatek-od-milosci,106758",
        "https://player.pl/programy-online/power-couple-odcinki,29479/odcinek-3,S01E03,198875",
        "https://player.pl/strefa-sport/motocyklicznie-odcinki,120/odcinek-4,S03E04,2063",
        "https://player.pl/strefa-sport/krolowie-driftu-odcinki,118/odcinek-3,S01E03,2013",
        "https://player.pl/seriale-online/pulapka-odcinki,13643", # 13 videos
        "https://player.pl/programy-online/one-night-squad-odcinki,31426", # 10 videos
    ],
    'LeshiVideoClient': [
        'https://www.le.com/ptv/vplay/78006876.html#vid=78006876',
        'https://www.le.com/ptv/vplay/22011384.html',
        'https://www.le.com/ptv/vplay/26322741.html',
        'https://www.le.com/ptv/vplay/77974306.html',
    ],
    'VeedMateVideoClient': [
        'https://www.youtube.com/watch?v=d006aGNWnic',
        'https://www.tiktok.com/@nataliireynoldss/video/7615426833458236685',
        'https://www.facebook.com/facebook/videos/how-it-feels-when-you-see-that-your-bestie-already-liked-the-reel-you-were-gonna/1507983703834653/',
        'https://x.com/jushendo/status/2036224267084333475'
    ],
    'KanKanNewsVideoClient': [
        'https://www.kankanews.com/detail/PbwRzE9qow4',
        'https://www.kankanews.com/detail/ebyjZR5Lzy3',
        'https://www.kankanews.com/detail/1W2v54r4zwA',
    ],
    'NuVidVideoClient': [
        'https://www.nuvid.com/video/6513023/italian-babe',
    ],
}
PARSE_SUPPLEMENT = {
    'Ku6VideoClient': {'name': 'Ku6VideoClient', 'display_name': 'Ku6VideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'Ku6VideoClient', 'test_url': 'https://www.ku6.com/video/detail?id=McZoSe_hgG_jwzy7pQLqvMJ3IoI.', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'Ku6VideoClient', 'raw_data': {}, 'title': '看到泪崩！微视频百年风华', 'cover_url': 'https://rbv01.ku6.com/wifi/o_1f9dtdubnf8b8oe1nf9jbnt61l', 'err_msg': '', 'download_url': 'https://rbv01.ku6.com/wifi/o_1f9dtdubn8l8154lddtcdtdusm', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\Ku6VideoClient\\看到泪崩！微视频百年风华.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'requests.head', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'McZoSe_hgG_jwzy7pQLqvMJ3IoI.', 'chunk_size': 1048576}}, {'name': 'Ku6VideoClient', 'test_url': 'https://www.ku6.com/video/detail?id=HE3lfhcp13Gd0qND4zfzXYQONMY.', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'Ku6VideoClient', 'raw_data': {}, 'title': '微视频｜领航新征程', 'cover_url': 'https://rbv01.ku6.com/wifi/o_1evr90of21l1p19rg1coi13ubgpg', 'err_msg': '', 'download_url': 'https://rbv01.ku6.com/wifi/o_1evr90gl2sdhjs4nn31bad1v3ue', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\Ku6VideoClient\\微视频｜领航新征程.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'requests.head', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'HE3lfhcp13Gd0qND4zfzXYQONMY.', 'chunk_size': 1048576}}]},
    'WeishiVideoClient': {'name': 'WeishiVideoClient', 'display_name': 'WeishiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'WeishiVideoClient', 'test_url': 'https://h5.weishi.qq.com/weishi/feed/76EaWNkEF1IqtfYVH/', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'WeishiVideoClient', 'raw_data': {}, 'title': '自己烤的串，果然比外面卖的便宜又好吃！', 'cover_url': 'https://pic.weishi.qq.com/5f4c695f6f5a4a74b2b17c106c57cover.jpg/640', 'err_msg': '', 'download_url': 'http://v.weishi.qq.com/tjg_2012262636_1047_e167370371ca4988a45e2b0ed039vide.f30.mp4?dis_k=fa133b9a4d822331e114bd8025694960&dis_t=1775200421&fromtag=0&pver=5.8.5&weishi_play_expire=1775243621&wsadapt=_0403151341__196691027_0_0_0_2_8_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW&wsadapt=_0403151341__196691027_0_0_0_2_0_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\WeishiVideoClient\\自己烤的串，果然比外面卖的便宜又好吃！.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '76EaWNkEF1IqtfYVH', 'chunk_size': 1048576}}, {'name': 'WeishiVideoClient', 'test_url': 'https://isee.weishi.qq.com/ws/app-pages/share/index.html?wxplay=1&id=7siJelmUp1MkDSPeo&spid=3704775550396963513&qua=v1_and_weishi_8.81.0_590_312026001_d&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'WeishiVideoClient', 'raw_data': {}, 'title': '古装 片，就是这样排出来的', 'cover_url': 'https://xp.qpic.cn/oscar_pic/0/e7b45286dcba420d89970a8d4489pict/0', 'err_msg': '', 'download_url': 'http://v.weishi.qq.com/gzc_1594_1047_0bc35eac6aaamuaip6jm7fqrp2ief7uqal2a.f70.mp4?dis_k=be71c6501f11932bf4ae629c3b6eb147&dis_t=1775200432&fromtag=0&pver=1.0.0&weishi_play_expire=1775243632&wsadapt=_0403151352__196732989_0_0_0_27_0_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\WeishiVideoClient\\古装片，就是这样排出来的.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '7siJelmUp1MkDSPeo', 'chunk_size': 1048576}}]},
    'YouTubeVideoClient': {'name': 'YouTubeVideoClient', 'display_name': 'YouTubeVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'YouTubeVideoClient', 'test_url': 'https://music.youtube.com/watch?v=PgPhDyV0J2w&list=RDAMVMPgPhDyV0J2w', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'YouTubeVideoClient', 'raw_data': {}, 'title': '【创造 营人气学员】 希林娜依·高 《中国新歌声2》音乐合辑完整版 SING!CHINA S2 [浙江卫视官方HD]', 'cover_url': 'https://i.ytimg.com/vi/PgPhDyV0J2w/sddefault.jpg', 'err_msg': '', 'download_url': '<videodl.modules.utils.youtubeutils.Stream object at 0x0000024B9AA55AD0>', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\YouTubeVideoClient\\【创造营人气学员】 希林娜依·高 《中国新歌声2》音乐合辑完整版 SING!CHINA S2 [浙江卫视官方HD].mp4', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'PgPhDyV0J2w', 'chunk_size': 1048576}}, {'name': 'YouTubeVideoClient', 'test_url': 'https://www.youtube.com/watch?v=hie-SsINu4Q&list=RDhie-SsINu4Q&start_radio=1', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'YouTubeVideoClient', 'raw_data': {}, 'title': "周杰倫好聽的40首歌 Best Songs Of Jay Chou 周杰倫最偉大的命中 下雨天在车里听周杰伦- 完美结合 Jay Chou's Top 40 Love Songs", 'cover_url': 'https://i.ytimg.com/vi/hie-SsINu4Q/sddefault.jpg?v=605c7fce', 'err_msg': '', 'download_url': '<videodl.modules.utils.youtubeutils.Stream object at 0x0000024B99FA5290>', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': "videodl_tmp_outputs\\YouTubeVideoClient\\周杰倫好聽 的40首歌 Best Songs Of Jay Chou 周杰倫最偉大的命中 下雨天在车里听周杰伦- 完美结合 Jay Chou's Top 40 Love Songs.mp4", 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'hie-SsINu4Q', 'chunk_size': 1048576}}]},
    'DuxiaoshiVideoClient': {'name': 'DuxiaoshiVideoClient', 'display_name': 'DuxiaoshiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'DuxiaoshiVideoClient', 'test_url': 'http://quanmin.baidu.com/sv?source=share-h5&pd=qm_share_search&vid=12474281128791424380', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'DuxiaoshiVideoClient', 'raw_data': {}, 'title': 'Redis分布式缓存常用命令解析', 'cover_url': 'https://vd3.bdstatic.com/mda-rabs6zmqbg9w8ab1/1736706595/mda-rabs6zmqbg9w8ab1.jpg?for=bg@s_0,w_800,h_1000', 'err_msg': '', 'download_url': 'https://vd2.bdstatic.com/mda-rabs6zmqbg9w8ab1/720p/mv_cae264_backtrack_720p_normal/1736706974323303590/mda-rabs6zmqbg9w8ab1.mp4?pd=-1&pt=-1&cr=2&vt=0&cd=0&did=cfcd208495d565ef66e7dff9f98764da&logid=0986868529&vid=12474281128791424380&auth_key=1775202387-0-0-384d5750a2d8934b99d19a892ec8b3e2&bcevod_channel=searchbox_feed', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\DuxiaoshiVideoClient\\Redis分布式缓存常用命令解析.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '12474281128791424380', 'chunk_size': 1048576}}, {'name': 'DuxiaoshiVideoClient', 'test_url': 'https://mbd.baidu.com/newspage/data/videolanding?nid=sv_8388278490910791594&sourceFrom=rec', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'DuxiaoshiVideoClient', 'raw_data': {}, 'title': '天津中驰：专注声测管与注浆管生产，细节决定成败', 'cover_url': 'https://pic.rmb.bdstatic.com/bjh/other/56c1fdada9d2c58a35bded241e5ef663.png?for=bg@s_0,w_800,h_1000', 'err_msg': '', 'download_url': 'https://vd9.bdstatic.com/mda-rhqnq9m87qbe70gw/mb/720p/mv_cae264_backtrack_720p_normal/1756137776222451415/mda-rhqnq9m87qbe70gw.mp4?pd=-1&pt=-1&cr=2&vt=0&cd=0&did=cfcd208495d565ef66e7dff9f98764da&logid=1001523137&vid=8388278490910791594&auth_key=1775202402-0-0-6a703e954df812d8dcbe308a8fea95d1&bcevod_channel=searchbox_feed', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\DuxiaoshiVideoClient\\天津中驰：专注声测管与注浆管生产，细节决定成败.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '8388278490910791594', 'chunk_size': 1048576}}]},
    'YoukuVideoClient': {'name': 'YoukuVideoClient', 'display_name': 'YoukuVideoClient', 'success_count': 4, 'total_count': 4, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'YoukuVideoClient', 'test_url': 'https://v.youku.com/v_show/id_XNDU1MTg1NjM2OA==', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'YoukuVideoClient', 'raw_data': {}, 'title': '天津话《乡村爱情12》王木生VS二奎，俩大不孝子让赵本山操碎了心', 'cover_url': 'https://m.ykimg.com/054101015E4BF6888B2AE197DDBBE956', 'err_msg': '', 'download_url': 'http://pl-ali.youku.com/playlist/m3u8?vid=XNDU1MTg1NjM2OA%3D%3D&type=hd3&ups_client_netip=725cc0a9&utid=p1dWIlP6umcCAXJcwKlTw5DW&ccode=0564&psid=bf49367a8ce85aaf3e5dff645ca1ba4141346&duration=99&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=1&ups_ts=1775200680&onOff=0&encr=0&ups_key=7f11aa6933304249b72a571d6a32067b&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\YoukuVideoClient\\天津话《乡村爱情12》王木生VS二奎，俩大不孝子让赵本山操碎了心.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'requests.head', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': True, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'XNDU1MTg1NjM2OA==', 'chunk_size': 1048576}}, {'name': 'YoukuVideoClient', 'test_url': 'https://v.youku.com/v_show/id_XNDA4MjA3ODA4.html?s=cbfd4dee962411de83b1&scm=20140719.apircmd.298496.video_XNDA4MjA3ODA4&spm=a2hkt.13141534.1_7.d_1_1', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'YoukuVideoClient', 'raw_data': {}, 'title': '笑傲江湖 96版 01', 'cover_url': 'https://m.ykimg.com/0541010167BFF5C82C7F7A12CF06B50B', 'err_msg': '', 'download_url': 'http://pl-ali.youku.com/playlist/m3u8?vid=XMzUwMzQ3NjMyMA%3D%3D&type=mp4hd2v3&ups_client_netip=725cc0a9&utid=tVdWIpGV%2FXACAXJcwKmUUkUa&ccode=0564&psid=7537d77d7d95a037fa4aa071462e016f41346&duration=2795&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1775200694&onOff=0&encr=0&ups_key=4cd93b59002707a9b4d0b1eed49a2651&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\YoukuVideoClient\\笑傲江湖 96版 01.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'requests.head', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': True, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'XNDA4MjA3ODA4', 'chunk_size': 1048576}}, {'name': 'YoukuVideoClient', 'test_url': 'https://www.youku.com/ku/webduanju?vid=XNjQ4MzYzNTY5Ng%3D%3D&showid=afafff1a3aef4f96a2ff&spm=a2hkl.pcshortshow.feed_2.d_1_1&scm=20140689.rcmd.feed.video_XNjQ4MzYzNTY5Ng%3D%3D', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'YoukuVideoClient', 'raw_data': {}, 'title': '我投喂了古代大将军', 'cover_url': 'https://m.ykimg.com/05410101687A2590662C28152E3ECC6A', 'err_msg': '', 'download_url': 'http://pl-ali.youku.com/playlist/m3u8?vid=XNjQ4MzYzNTY5Ng%3D%3D&type=mp4hd3v3&ups_client_netip=725cc0a9&utid=wldWIhWYfTQCAXJcwKk7osd0&ccode=0564&psid=49178a46be990dbd3ff7b5f29e67619241346&duration=190&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1775200706&onOff=0&encr=0&ups_key=18b16a54991418c11ba58c0d49817702&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\YoukuVideoClient\\我投喂了古代大将军.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'requests.head', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': True, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'XNjQ4MzYzNTY5Ng==', 'chunk_size': 1048576}}, {'name': 'YoukuVideoClient', 'test_url': 'https://v.youku.com/v_show/id_XNjQyOTgxMzQ2OA==.html', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'YoukuVideoClient', 'raw_data': {}, 'title': '大人笨：所以我不要变成大人', 'cover_url': 'https://m.ykimg.com/05410101670C70593F0724269A63D2BD', 'err_msg': '', 'download_url': 'http://pl-ali.youku.com/playlist/m3u8?vid=XNjQyOTgxMzQ2OA%3D%3D&type=mp4hd2v3&ups_client_netip=725cc0a9&utid=z1dWInOm0BoCAXJcwKkPBZ%2BL&ccode=0564&psid=da46e5d8f5642e8510accf4c011dea1f41346&duration=3978&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1775200719&onOff=0&encr=0&ups_key=943ba05a98cea062c35639f95fda3aa4&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\YoukuVideoClient\\大人笨：所以我不要变成大人.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'requests.head', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': True, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'XNjQyOTgxMzQ2OA==', 'chunk_size': 1048576}}]},
    'CCTVVideoClient': {'name': 'CCTVVideoClient', 'display_name': 'CCTVVideoClient', 'success_count': 3, 'total_count': 3, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'CCTVVideoClient', 'test_url': 'https://v.cctv.com/2021/06/05/VIDEwn0n7VRJokIL7rBi2ink210605.shtml?spm=C90324.Pfdd0SYeqktv.Eri5TUDwaTXO.6', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'CCTVVideoClient', 'raw_data': {}, 'title': '王冰冰看《新兵请入列》的反应太可爱了！', 'cover_url': 'https://p2.img.cctvpic.com/fmspic/2021/06/05/437ddd8637e445598511370540e48788-180.jpg', 'err_msg': '', 'download_url': 'https://dh5wswx02.v.cntv.cn/asp/h5e/hls/2000/0303000a/3/default/437ddd8637e445598511370540e48788/2000.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\CCTVVideoClient\\王冰冰看《新兵请入列》的 反应太可爱了！.mp4', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '437ddd8637e445598511370540e48788', 'chunk_size': 1048576, 'hls_key': 'hls_h5e_url'}}, {'name': 'CCTVVideoClient', 'test_url': 'https://tv.cctv.com/2022/04/15/VIDEYQOwJ33dIqm1h9PvmIpO220415.shtml?spm=C95797228340.P3XSH3djsU2B.0.0', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'CCTVVideoClient', 'raw_data': {}, 'title': '《百家讲坛》 20220415 品读中华经典诗文 8 乐天派的人生区间', 'cover_url': 'https://p4.img.cctvpic.com/fmspic/2022/04/15/be2a31ee9fc54e808a207f8106b36ca4-1.jpg', 'err_msg': '', 'download_url': 'https://dh5ws01.v.cntv.cn/asp/h5e/hls/2000/0303000a/3/default/be2a31ee9fc54e808a207f8106b36ca4/2000.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\CCTVVideoClient\\《百家讲坛》 20220415 品读中华经典诗文 8 乐天派的人生区间.mp4', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'be2a31ee9fc54e808a207f8106b36ca4', 'chunk_size': 1048576, 'hls_key': 'hls_h5e_url'}}, {'name': 'CCTVVideoClient', 'test_url': 'https://xczx.cctv.com/2025/11/19/ARTIhGNpDUfXpmRX0qjQ6mSC251119.shtml?spm=C73274.Pt2UfsofZQQ5.EmwSKtAQYeDI.2', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'CCTVVideoClient', 'raw_data': {}, 'title': '《三农群英汇》 20251118 棉田守望者', 'cover_url': 'https://p3.img.cctvpic.com/fmspic/2025/11/18/e26953187476490d8b7b594518646a17-1.jpg', 'err_msg': '', 'download_url': 'https://dh5ws01.v.cntv.cn/asp/h5e/hls/2000/0303000a/3/default/e26953187476490d8b7b594518646a17/2000.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\CCTVVideoClient\\《三农群英汇》 20251118 棉田守望者.mp4', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'e26953187476490d8b7b594518646a17', 'chunk_size': 1048576, 'hls_key': 'hls_h5e_url'}}]},
    'TencentVideoClient': {'name': 'TencentVideoClient', 'display_name': 'TencentVideoClient', 'success_count': 6, 'total_count': 6, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'TencentVideoClient', 'test_url': 'https://v.qq.com/x/cover/mzc00349vqikdb0/b3535d8h2a1.html', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'TencentVideoClient', 'raw_data': {}, 'title': '《国外治愈短片》', 'cover_url': 'https://puui.qpic.cn/vpic_cover/b3535d8h2a1/b3535d8h2a1_1703947768_hz.jpg/496?imageMogr2/thumbnail/252x', 'err_msg': '', 'download_url': 'videodl_tmp_outputs\\TencentVideoClient\\mzc00349vqikdb0-b3535d8h2a1.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'ts', 'save_path': 'videodl_tmp_outputs\\TencentVideoClient\\《国外治愈短片》', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'mzc00349vqikdb0-b3535d8h2a1', 'chunk_size': 1048576}}, {'name': 'TencentVideoClient', 'test_url': 'https://v.qq.com/x/cover/ygci7rbfq3celp8/S0010phisz5.html?cut_vid=i4101ucafw7&scene_id=3&start=93', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'TencentVideoClient', 'raw_data': {}, 'title': '罗小黑战记', 'cover_url': 'http://i.gtimg.cn/qqlive/img/jpgcache/files/qqvideo/hori/y/ygci7rbfq3celp8_big.jpg', 'err_msg': '', 'download_url': 'videodl_tmp_outputs\\TencentVideoClient\\ygci7rbfq3celp8-S0010phisz5.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'ts', 'save_path': 'videodl_tmp_outputs\\TencentVideoClient\\罗小黑战记', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'ygci7rbfq3celp8-S0010phisz5', 'chunk_size': 1048576}}, {'name': 'TencentVideoClient', 'test_url': 'https://www.iflix.com/en/play/0s682hc45t0ohll/a00340c66f8-EP1%3A_Miss_Gu_Who_Is_Silent', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'TencentVideoClient', 'raw_data': {}, 'title': 'EP1 Miss Gu Who Is Silent', 'cover_url': 'https://vcover-hz-pic.wetvinfo.com/vcover_hz_pic/0/0s682hc45t0ohll1730713070801_ZO9GlVdO/0', 'err_msg': '', 'download_url': 'https://cffaws.wetvinfo.com/svp_50112/01FAA24431BEEBF90B8F34095D79A5A24AFECD2B6268893648AFCDC8226FAACF82B511E58375F233D56716766569D199CF50DA03664BFE5FDACD05AB33FCDB5129735CBDC0E89A3FE48340243D2A90AAE37D46B208541D05E0DAE2B20385EC6EB8B60D7C6ABE58310F3230E5E191F2DD9221D7142C4CB801FD20C8DB552776115D/gzc_1000102_0b53wqabkaaayyamu5pa2vrmbngdcw4aaeca.f323013.ts.m3u8?ver=4', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\TencentVideoClient\\EP1 Miss Gu Who Is Silent', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'a00340c66f8', 'chunk_size': 1048576}}, {'name': 'TencentVideoClient', 'test_url': 'https://www.iflix.com/play/0s682hc45t0ohll', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'TencentVideoClient', 'raw_data': {}, 'title': 'EP1 Miss Gu Who Is Silent', 'cover_url': 'https://vcover-hz-pic.wetvinfo.com/vcover_hz_pic/0/0s682hc45t0ohll1730713070801_ZO9GlVdO/0', 'err_msg': '', 'download_url': 'https://cffaws.wetvinfo.com/svp_50112/01820ACB403CF69B913EAF6977CB30817AE05FD9DCDE1BA0CF3745C3C620149A02F79D50F67C89C6746A19B39F448275BF912F87382E9C2F57B11EE2EDB8AAE0E0CFB9345F90804387F3832752ED29D9C751E1E00C1CD6B5EDF005DF72A3A909B3088F9232AC32F34BA54299DEF7E07DBB3F5AEB9D490FA5A88A3CA6DD750148B8/gzc_1000102_0b53wqabkaaayyamu5pa2vrmbngdcw4aaeca.f323013.ts.m3u8?ver=4', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\TencentVideoClient\\EP1 Miss Gu Who Is Silent', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '0s682hc45t0ohll-a00340c66f8', 'chunk_size': 1048576}}, {'name': 'TencentVideoClient', 'test_url': 'https://v.qq.com/x/cover/nhtfh14i9y1egge/d00249ld45q.html', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'TencentVideoClient', 'raw_data': {}, 'title': '李师师', 'cover_url': 'http://i.gtimg.cn/qqlive/img/jpgcache/files/qqvideo/hori/n/nhtfh14i9y1egge_big.jpg', 'err_msg': '', 'download_url': 'videodl_tmp_outputs\\TencentVideoClient\\nhtfh14i9y1egge-d00249ld45q.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'ts', 'save_path': 'videodl_tmp_outputs\\TencentVideoClient\\李师师', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'nhtfh14i9y1egge-d00249ld45q', 'chunk_size': 1048576}}, {'name': 'TencentVideoClient', 'test_url': 'https://v.qq.com/x/cover/nhtfh14i9y1egge.html', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'TencentVideoClient', 'raw_data': {}, 'title': 'ep1-李师师', 'cover_url': 'http://i.gtimg.cn/qqlive/img/jpgcache/files/qqvideo/hori/n/nhtfh14i9y1egge_big.jpg', 'err_msg': '', 'download_url': 'videodl_tmp_outputs\\TencentVideoClient\\nhtfh14i9y1egge-d00249ld45q.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'ts', 'save_path': 'videodl_tmp_outputs\\TencentVideoClient\\ep1-李师师', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'nhtfh14i9y1egge-d00249ld45q', 'chunk_size': 1048576}}]},
    'GeniusVideoClient': {'name': 'GeniusVideoClient', 'display_name': 'GeniusVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'GeniusVideoClient', 'test_url': 'https://genius.com/videos/Halle-breaks-down-the-meaning-of-bite-your-lip', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'GeniusVideoClient', 'raw_data': {}, 'title': 'Halle-breaks-down-the-meaning-of-bite-your-lip', 'cover_url': 'https://cf-images.us-east-1.prod.boltdns.net/v1/static/4863540648001/961d8e32-d67f-4573-8ee1-33a9769e1091/a6fbee46-eef6-45a7-bbb5-9b87b71ba9ca/1280x720/match/image.jpg', 'err_msg': '', 'download_url': 'http://house-fastly-signed-us-east-1-prod.brightcovecdn.com/media/v1/pmp4/static/clear/4863540648001/961d8e32-d67f-4573-8ee1-33a9769e1091/ed93d7cf-6e1e-4b60-b295-ccaf5d36d5c2/main.mp4?fastly_token=NjlmNDViNzNfZTgwOTA3YWEzZWVjNzE4ODNlYjk3NDVmMDYyODU4YjFmNzQ2OTRmNDg1NTE0ODIwMjdhYTRlZjZiOWUyMmJhOV8vL2hvdXNlLWZhc3RseS1zaWduZWQtdXMtZWFzdC0xLXByb2QuYnJpZ2h0Y292ZWNkbi5jb20vbWVkaWEvdjEvcG1wNC9zdGF0aWMvY2xlYXIvNDg2MzU0MDY0ODAwMS85NjFkOGUzMi1kNjdmLTQ1NzMtOGVlMS0zM2E5NzY5ZTEwOTEvZWQ5M2Q3Y2YtNmUxZS00YjYwLWIyOTUtY2NhZjVkMzZkNWMyL21haW4ubXA0', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\GeniusVideoClient\\Halle-breaks-down-the-meaning-of-bite-your-lip.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '6385323870112', 'chunk_size': 1048576}}, {'name': 'GeniusVideoClient', 'test_url': 'https://genius.com/videos/Ashnikko-breaks-down-the-meaning-of-sticky-fingers', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'GeniusVideoClient', 'raw_data': {}, 'title': 'Ashnikko-breaks-down-the-meaning-of-sticky-fingers', 'cover_url': 'https://cf-images.us-east-1.prod.boltdns.net/v1/static/4863540648001/eaba2f9f-7980-441b-a5ed-9e4cfda46597/fb1ca34e-5f96-41e6-8f60-a719a068cca3/1280x720/match/image.jpg', 'err_msg': '', 'download_url': 'http://house-fastly-signed-us-east-1-prod.brightcovecdn.com/media/v1/pmp4/static/clear/4863540648001/eaba2f9f-7980-441b-a5ed-9e4cfda46597/a88de6e6-02e9-48e9-a5d9-969c31fb778b/main.mp4?fastly_token=NjlmNDViMDlfZGE1Njk0NjZjYzQ4YmEyZjM2MjI5MTJlYjcyZTZhZmY5YTg2MWM0MGE0NjEyN2MyNGFjNDRmZTJiNWYwNjJiY18vL2hvdXNlLWZhc3RseS1zaWduZWQtdXMtZWFzdC0xLXByb2QuYnJpZ2h0Y292ZWNkbi5jb20vbWVkaWEvdjEvcG1wNC9zdGF0aWMvY2xlYXIvNDg2MzU0MDY0ODAwMS9lYWJhMmY5Zi03OTgwLTQ0MWItYTVlZC05ZTRjZmRhNDY1OTcvYTg4ZGU2ZTYtMDJlOS00OGU5LWE1ZDktOTY5YzMxZmI3NzhiL21haW4ubXA0', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\GeniusVideoClient\\Ashnikko-breaks-down-the-meaning-of-sticky-fingers.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '6384979708112', 'chunk_size': 1048576}}]},
    'RedditVideoClient': {'name': 'RedditVideoClient', 'display_name': 'RedditVideoClient', 'success_count': 3, 'total_count': 3, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'RedditVideoClient', 'test_url': 'https://www.reddit.com/r/videos/comments/6rrwyj/that_small_heart_attack/', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'RedditVideoClient', 'raw_data': {}, 'title': 'That small heart attack', 'cover_url': 'https://b.thumbs.redditmedia.com/sYbg5-j-7x_3-n0WnEWv4SzenbXj-9-2yWCvB-OywDE.jpg', 'err_msg': '', 'download_url': 'https://v.redd.it/zv89llsvexdz/HLSPlaylist.m3u8?a=1777793302%2CYjJlNWE3MGM0ZGMyZDQ2ODBiZmQwYjhjZTM5YjhhZDIzYTYxM2EzZjYzNGExNTZlNWQxYmE0MDkwMGE4OWY1Mg%3D%3D&amp%3Bv=1&amp%3Bf=sd&f=hd%2CsubsAll', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\RedditVideoClient\\That small heart attack.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '6rrwyj', 'chunk_size': 1048576}}, {'name': 'RedditVideoClient', 'test_url': 'https://old.reddit.com/r/ketamine/comments/degtjo/when_the_k_hits/', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'RedditVideoClient', 'raw_data': {}, 'title': 'When the K hits', 'cover_url': 'https://a.thumbs.redditmedia.com/gjA8nH1AAnCnXviJf6IfhwKJ8Ty7xptzU2oZO_QUYq8.jpg', 'err_msg': '', 'download_url': 'https://v.redd.it/gqsbxts133r31/HLSPlaylist.m3u8?a=1777793317%2CNWY1ZDkxMDYyNjA0NGUyZGVmNDJhOTM2YTkwZWJkZGNjOGI3NzJlMmQ3NDI5OTNkMzUyNTJjNDExMmRmZjg3Mw%3D%3D&amp%3Bv=1&amp%3Bf=sd&f=hd%2CsubsAll', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\RedditVideoClient\\When the K hits.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'degtjo', 'chunk_size': 1048576}}, {'name': 'RedditVideoClient', 'test_url': 'https://www.reddit.com/r/KamenRider/comments/wzqkxp/finale_kamen_rider_revice_episode_50_family_to/', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'RedditVideoClient', 'raw_data': {}, 'title': 'ep1-[Finale] Kamen Rider Revice Episode 50 Family to the End, Until the Day We Meet Again Discussion', 'cover_url': 'https://a.thumbs.redditmedia.com/1vMxqp7yt-0mNTHJ04h73mB3iS21EomcnDZxFW42dh4.jpg', 'err_msg': '', 'download_url': 'https://v.redd.it/link/wzqkxp/asset/cpvjun0zyhk91/HLSPlaylist.m3u8?a=1777793333%2COTFkZDdiZDAyNzJmMzFmODJmZWQ4Mjc5ZDk0YzIyMjc0ODA2ZDhiMGE4ODFjYjlhZDdkZjkwNzIyYjhkNjg3ZQ%3D%3D&amp%3Bv=1&amp%3Bf=sd&f=hd%2CsubsAll', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\RedditVideoClient\\ep1-[Finale] Kamen Rider Revice Episode 50 Family to the End, Until the Day We Meet Again Discussion.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 'cpvjun0zyhk91', 'chunk_size': 1048576}}]},
    'MGTVVideoClient': {'name': 'MGTVVideoClient', 'display_name': 'MGTVVideoClient', 'success_count': 3, 'total_count': 3, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'MGTVVideoClient', 'test_url': 'https://www.mgtv.com/l/100026064/19868457.html?fpa=1684&fpos=&lastp=ch_home&cpid=5', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'MGTVVideoClient', 'raw_data': {}, 'title': '年度 高能名场面盘点', 'cover_url': 'https://ugc.hitv.com/3/231008125923CF89B5145A1D5DA0BB1BC95385542MUMx/jo7W7u0.jpg', 'err_msg': '', 'download_url': 'https://pcvideotx.titan.mgtv.com/c1/ugc/2023/10/08/2B4FC4B9655D48DF0321B770C139A70F_20231008_1_1_1122_mp4/2B4FC4B9655D48DF0321B770C139A70F.m3u8?arange=0&pm=660NzcvsZ8jGWmP~6tI3mRL_4wPpomV~iYqZrsAt~SXpYceogARC4eImmqBpWKGPA9lFsKeJidpmIQv7gD5DoTQpWD0oE3jcu~4zjYFZ0EgFQfmbHIvVI4KPGgCm1a~xGYRlxrX~elWOTm~nvP4luWn1ECbzwuxm~_9m9DlS9mKaTrSepSq8i3yfuGg0X63HXNcjXB0kyUFk2rnUZrla3xhH3qqZz2oi~RJ3oCk51wAC~ayUqRWeH7cNqs4VFvujXbtoQFk8ujfSlddCD9SZwZb7S2ApOk5G8DSM0dXLgCFM96pj9b8azkDtI1Qx5V1~MCGf_QYJCBKo80J7y3rHIaHSHwFfiCx125LclsZbzVJjcSg3ZvOyWxIrzUMH46V83w71OeeiXeudcKhd~qnbr9oj68KsOjZ4DndSVMYeWktjhkSgPWBIAWKx5UON3UrQ1UC7Og--&mr=M6lev7znSOwnLHGfhIGaVM2hXdCVX0YlFFqMN7VZjdr8a_qRNbumFNDZDDgexcsmRErVAZPaezwYAOhYWnEKzCLxB3PfVQ~r2c3oa~DWpfhSVSFc8FhFwH3KaycgRJqe6bZApmVvNSYzN2OduniY1Ib4E2jZQ~eTWTK2plbkvmMbpi_qyldvTPBcoKglYTNu7CwUuRK_6MlwsWDdYn7GuVtDcJsaPTs4lz~Vnhi_9goJmrIi1WiIH5TChkaLGxhDqegCG1KD0vB2SOdwse8UOqotT~bx1n4N_d7V_UeS_KwixvpX6Cv4Dyp3MidF~Asjr1Xw11vpeRlhFbEvfvr6zamhasn8WeWi7WTwXbUDKJtBfGtyPawZ9JVZjJKlV0mAi39cuPjBiP5mhYkIl13o8Q9DsNcEWMxmmq1YX0gNCwfl1TpL~RoNBglMrPGOMOZNzAdBFpLvB4_S2kfd8PkOFfty538VliTHy2uicFVn25lBgBeJ9jC1ykNmJKFBTaTkNfrnPskfHua20KBZ3GM0DdL2hfMKJrsPyyzboDfon0fNe35eh0QgneNDzQl3nfvTw88goEPCIgLNDXqKqKmP~59~_PFfqh14mmURLOhJvAJ07yn_5cXgkMVfQ3gYPIwrWzwNaWKjSa8RqBLmZq4Bsg--&uid=null&term=4&def=3&vc=AVC&scid=25015&cpno=6i06rp&ruid=d242d7351c7c4730&sh=1', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\MGTVVideoClient\\年度高能名场面盘点.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '19868457.html', 'chunk_size': 1048576}}, {'name': 'MGTVVideoClient', 'test_url': 'https://www.mgtv.com/b/788366/23780111.html?fpa=1756&fpos=&lastp=ch_home', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'MGTVVideoClient', 'raw_data': {}, 'title': '声鸣远扬2025', 'cover_url': 'https://2img.hitv.com/preview/sp_images/2025/11/16/202511161954521627756.jpg', 'err_msg': '', 'download_url': 'https://pcvideocmobile.titan.mgtv.com/c1/2025/11/19_0/FB6E9667FF44CD022A563C9FEDDEE70E_20251120_1_1_1086_mp4/B9441A7EE03DBCCDBD79238EC6F21AD7.m3u8?arange=0&pm=ikS576QuqDCmV~JXEDgXE6ltK6CuroOZD7RcAMQmGjiTnTkr~s9TRpPtmsWW0z9RjXke5spOq976NDneVverIrPRAL~2lcTaqCegKP5GBHAU2nV0N4SG9qJhMBuI20l6C5QUGxvWDhz5x_z7GYz92bhz1_8Ejgh2ZpXU6HonLWtQMZyNoVM4G38xai5ttP_t_d2hSMSfRgLGZuBXD1RZ_ljqVfd78bsH~4eqhSO7t~4~TTr~Q6rUAGLGLesgB4Pj0Hi2mnOkscVoHMgSiwIOEZ74e4zbCCKn_kkAwTPdsvJTm0KX2lHQnuNGJwRTwNExZuy7Ln0~j~qEe__2NkoOM5GXi3KubI0zjvI3dlcj1_tNJjtE6HZKSsZFNqR1oxyiir7AuamkyCpMjfyQCzf77p6nWP_AmaTTQgvJSRbJioEEGeEMr3Qg1en7a5wra0HMlz3aHqOg7lAdcMT5gwUTjg--&mr=wMV00y5xhP_kpFZhKdavvwQmz_f0pOOpRZ~yGINzUXJKK_xrm0yx_XOGw7km0aLkY1TWqOyYtq2KuTZKPnOzXUB2ofArmWyYQwxxIrwyVY5iluoPqqErN81ojlz6s_bpP4fiQIDx8RjVKEfpV8_AeGxpyIZ87yRrwAZd1KCZWUlpEfHcOHSNiPo~UtGQANixYqPpqaIJrOHrUrxTUGYTuD_tdOJxrO3DbwU9CG7ksSXiQLDs6o801snOAjxV32L5Y6HzAti2cZe5PNlipVIzZGslK2fhVJEVdjPdoMz3zayujjElFbPmzElAauPDIioJuJM6vzVHrr3H47mfyexCzJd6w6IpqbGEym~BVYU77qhMvf21jhnCBQ63FEoRIYY9AvNnecRnfMh35evt8zZSBh5hMZn2G11~orEnVjunEudHUZh75WUrlRa0Fr8Dim1sj1BHtRzzC8w_LZq8annAwYHY0z5drZSraVqR9KDk_sEIFY7~P7O84zH1lS9ND4UKHDsh42mH3ZpcOyiZEt51P8yFN70tfEV65lgLiGUXjYAvKLvx5UNz_P~Wqb4b08sve1ALv9qHgHIxCfTVMsIahTyVAqVQf~uVqIGQHaOx9iyVUEVU8e~A58mRHfZ14hAwp6s2TH0Hue67IxLwvJ1fQw--&uid=null&term=4&def=3&vc=AVC&scid=25151&cpno=6i06rp&ruid=52609ee3ada44f9b&sh=1', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\MGTVVideoClient\\声鸣远扬2025.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '23780111.html', 'chunk_size': 1048576}}, {'name': 'MGTVVideoClient', 'test_url': 'https://www.mgtv.com/b/805972/23756299.html?fpa=1261&fpos=&lastp=ch_home&cpid=5', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'MGTVVideoClient', 'raw_data': {}, 'title': '乌蒙深处', 'cover_url': 'https://0img.hitv.com/preview/sp_images/2025/11/11/202511112153438822446.jpg', 'err_msg': '', 'download_url': 'https://pcvideotx.titan.mgtv.com/c1/2026/03/01_0/1DAAF3A72D3A33154E5A416683B12847_20260302_1_1_914_mp4/FDE464FB33618231AD2EABA8ADEB6076.m3u8?arange=0&pm=2f9FyaltXztuyWWN5kBHHFao2pBRO9ep_I3A1TCm6BEG~zUZS3iNQh2PH7OuCIbyUiJ89SdO_q~11kcCW4lOSNqo5qFc7_d4VM7HgeM2rVN8znEbZ5c8A6xhZCdpYO9DJT9MTPaHJuZFUEooFZjUSZRyMwUIEdtQGyXp2prV4hjHOqmy3KrM_1qfNM_57m6cBznlO5R5CBQCTu7ZxgiUKmaOlMB_1wSRWTdBV9HiEvKg9hoFi3Gbedz~21~yyyIiJiOuTw95j4k5Qwr0yyv9GdOXEkMKMltXyg0JO~pWqF5k_Jpd4TiEO5IFVQ4NIHoCRFTIJahh4gcTw5NwP5X3uT4pFy7fYGNf7j72hj4G3o4SdWHMmiEJr95yQ0B9r0AJWtifT8CPJpH5FxvqXPHrKmW7MRHSCeCz1zQh9Sb_orBMrA9pZqsBtdlm3sRtI2a3SJfl8g--&mr=4qLouA13nZAnBAxWix60qNYYXMGvrtjeK9ueViMkY4hiVEylY8PGuni7EX4PNxAL5VhDErJGlsPIlAcjVvr_V3O2EsqXQK8Jnwwd_Fky3xvNp4v8PVFiBA5HGC9EVebKR325YKI_NneMjvVl2l1OngUUAH16ZDO3q9jMZ2vnv6aX9bm6ODY2g0TGqQmok87XQvcy6YYl~LBh7ZJv4jZ7kYEqR7vwqIwq0s5XsI8Qaq9aqQ3Jd9O4acipqCr5BC9GnWKAF3tRtY_tjtD4p969QifGd8eDem~2qoQh~6L0f9UjNsAqWTEGUlGOqt4lBTllwiFO5cb8zG00zzivwUP9Ya_76sT0AsPuJqgpdeOdTXSrfsRuleTOfXFrekeKAlt1Cvv2Ds1Al3Hh2C3LnQYJtcCR2t8r94~r1Gt_YiixqGuhBG_vJ869eJYAr_CnFukFYSDuYAK2tUfAF~xRtJRRV8_zUHJx8hf_RIuKDmDz9_tJavOiXqV5bh_dwQ9_YGDoGoW9Q1xxMzz45G4PgNZlGzDd1xDsZPvOl~EEUmuKU_ZARS0ffL_i2OZwJ0w_YuLZGJItnjIbhlWk6qi4LcGJI4_WAMU~pZZCG5cWUZE~Ffx1AhiIbwKXgEkP2ddKR5GBjxtTyk4J53OMEsRW&uid=null&term=4&def=3&vc=AVC&scid=25015&cpno=6i06rp&ruid=ce1e523a76214983&sh=1', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'm3u8', 'save_path': 'videodl_tmp_outputs\\MGTVVideoClient\\乌蒙深处.m3u8', 'guess_video_ext_result': {'ext': 'm3u8', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '23756299.html', 'chunk_size': 1048576}}]},
    'IQiyiVideoClient': {'name': 'IQiyiVideoClient', 'display_name': 'IQiyiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'IQiyiVideoClient', 'test_url': 'https://www.iqiyi.com/v_1wc7muawbrc.html', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'IQiyiVideoClient', 'raw_data': {}, 'title': '天才老舅重拳出击', 'cover_url': 'https://pic1.iqiyipic.com/image/20260104/ea/93/a_100721215_m_601_m17_579_772.avif', 'err_msg': '', 'download_url': 'videodl_tmp_outputs\\IQiyiVideoClient\\6998596211753700.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\IQiyiVideoClient\\天才老舅重拳出击.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 6998596211753700, 'chunk_size': 1048576}}, {'name': 'IQiyiVideoClient', 'test_url': 'https://www.iqiyi.com/v_1y6z93cf2qw.html', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'IQiyiVideoClient', 'raw_data': {}, 'title': '正片｜刺杀小说家2', 'cover_url': 'https://pic6.iqiyipic.com/image/20251211/77/76/v_184727354_m_601_m4_120_160.avif', 'err_msg': '', 'download_url': 'videodl_tmp_outputs\\IQiyiVideoClient\\7079614962197700.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\IQiyiVideoClient\\正片｜刺杀小说家2.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': 7079614962197700, 'chunk_size': 1048576}}]},
    'M1905VideoClient': {'name': 'M1905VideoClient', 'display_name': 'M1905VideoClient', 'success_count': 5, 'total_count': 5, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'M1905VideoClient', 'test_url': 'https://www.1905.com/video/play/1751538.shtml', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'M1905VideoClient', 'raw_data': {}, 'title': '《寻秦记》释出终极预告 古天乐林峯师徒 反目陷情义之战', 'cover_url': 'https://image11.m1905.cn/uploadfile/2025/1225/20251225012307886408.jpg', 'err_msg': '', 'download_url': 'https://m3u8.vodfile.m1905.com/202604040332/e2b0d5a172c0d4a9595e8cc17ca00af1/video/moss/2025/12/25/v20251225PAPR76BFZFLMV6MH/v20251225PAPR76BFZFLMV6MH.m3u8', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\M1905VideoClient\\《寻秦记》释出终极预告 古天乐林 峯师徒反目陷情义之战.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '1751538', 'chunk_size': 1048576}}, {'name': 'M1905VideoClient', 'test_url': 'https://www.1905.com/vod/play/1573197.shtml?fr=vodhome_zxdp_tj', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'M1905VideoClient', 'raw_data': {}, 'title': '岁岁平安', 'cover_url': 'https://image11.m1905.cn/uploadfile/2022/0412/20220412053828471015.jpg', 'err_msg': '', 'download_url': 'https://m3u8i1.vodfile.m1905.com/movie/2022/04/12/m202204126XE92P1ZWOYZPJ5J/66D6971B5E005005CC9A6BBB6.m3u8?tm=1775244746&sign=39d09d1bd4dc0858ee80ef6d67ff0d6e', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\M1905VideoClient\\岁岁平安.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '1573197', 'chunk_size': 1048576}}, {'name': 'M1905VideoClient', 'test_url': 'https://vip.1905.com/play/535547.shtml', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'M1905VideoClient', 'raw_data': {}, 'title': '暴风骤雨', 'cover_url': 'https://image11.m1905.cn/uploadfile/2016/0726/20160726024034717862.jpg', 'err_msg': '', 'download_url': 'https://m3u8i1.vodfile.m1905.com/movie/2019/12/11/m201912111LP6Z6LHYQ82WIAV/78071719EDF1D65B227567B58.m3u8?tm=1775244757&sign=267bd51305e97a5ca14a36145764fd31', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\M1905VideoClient\\暴风骤雨.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '525455', 'chunk_size': 1048576}}, {'name': 'M1905VideoClient', 'test_url': 'https://www.1905.com/mdb/film/2245563', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'M1905VideoClient', 'raw_data': {}, 'title': '盗御马', 'cover_url': 'https://image11.m1905.cn/uploadfile/2018/0611/20180611012648750947.jpg', 'err_msg': '', 'download_url': 'https://m3u8i1.vodfile.m1905.com/movie/2018/06/06/m20180606MBTGMTGQY7DROSOQ/C406BAA77204CE621E9FBFF59.m3u8?tm=1775244773&sign=05f56be44a966e5c1d4028b403ab805c', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\M1905VideoClient\\盗御马.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '1287886', 'chunk_size': 1048576}}, {'name': 'M1905VideoClient', 'test_url': 'https://www.1905.com/vod/play/1287886.shtml', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'M1905VideoClient', 'raw_data': {}, 'title': '盗御马', 'cover_url': 'https://image11.m1905.cn/uploadfile/2018/0611/20180611012648750947.jpg', 'err_msg': '', 'download_url': 'https://m3u8i1.vodfile.m1905.com/movie/2018/06/06/m20180606MBTGMTGQY7DROSOQ/C406BAA77204CE621E9FBFF59.m3u8?tm=1775244787&sign=1bd159c2126618a843920a629ec65f5d', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\M1905VideoClient\\盗御马.m3u8', 'guess_video_ext_result': {}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': True, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '1287886', 'chunk_size': 1048576}}]},
    'KugouMVVideoClient': {'name': 'KugouMVVideoClient', 'display_name': 'KugouMVVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'KugouMVVideoClient', 'test_url': 'https://www.kugou.com/mv/8cwxy96/', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'KugouMVVideoClient', 'raw_data': {}, 'title': 'K歌之王 AIR', 'cover_url': 'http://imge.kugou.com/mvhdpic/480/20251106/20251106172407302232.jpg', 'err_msg': '', 'download_url': 'https://mvwebfs.kugou.com/202604031533/5952ac55cee7f7b6efc5ae0da77a3c6f/KGTX/CLTX002/48c10c9580d414854fd2632a8da59485.mp4', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\KugouMVVideoClient\\K歌之王 AIR.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '8cwxy96', 'chunk_size': 1048576}}, {'name': 'KugouMVVideoClient', 'test_url': 'https://www.kugou.com/mv/8gtun15/', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'KugouMVVideoClient', 'raw_data': {}, 'title': '美女泳装系列 10', 'cover_url': 'http://imge.kugou.com/mvhdpic/480/20251220/20251220204009364283.jpg', 'err_msg': '', 'download_url': 'https://mvwebfs.kugou.com/202604031533/f36b31672bce138976f7054a5e7bf273/KGTX/CLTX002/2fef98deb3f0e6c8b0f4b9f98bdd7b79.mp4', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\KugouMVVideoClient\\美女泳装系列 10.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '8gtun15', 'chunk_size': 1048576}}]},
    'KuaishouVideoClient': {'name': 'KuaishouVideoClient', 'display_name': 'KuaishouVideoClient', 'success_count': 4, 'total_count': 4, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'KuaishouVideoClient', 'test_url': 'https://www.kuaishou.com/short-video/3xwzr5dveyqc5fa?authorId=3xv7d3j7hqqpksi', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'KuaishouVideoClient', 'raw_data': {}, 'title': '#萌妹子', 'cover_url': 'https://p2.a.yximgs.com/upic/2025/07/03/20/BMjAyNTA3MDMyMDM1NDdfMTY5MjQxNDg4M18xNjg0MjI2Mzg2MzJfMV8z_B1e22a51c6f9a4c307fa3cf24c5217d3f.jpg?tag=1-1775201682-xpcwebdetail-0-hiq1odlxyv-919312270ee3ecc8&clientCacheKey=3xwzr5dveyqc5fa.jpg&di=725cc0a9&bp=10004', 'err_msg': '', 'download_url': 'https://v23-3.kwaicdn.com/bs2/photo-video-mz/5239938337230174402_72b0730c7718f525_7850_hd15.mp4?pkey=AAUwwAICbRyxB9YIxigm63PwihDx-XCy4oN-eKv8mV-SOU_2vPt4X9RqYDY1mdhSoX9mxS1d_fy2Ix7tY9MH3T14LV-Xqq9G8FbE9EhLsmbywQ1jbhMe6Uqj7MP-OOW6xBw&tag=1-1775201682-unknown-0-c3oy0vwfwj-e7bfff1e3574f218&clientCacheKey=3xwzr5dveyqc5fa_8b20bd99&di=725cc0a9&bp=10004&kwai-not-alloc=40&tt=hd15&ss=vpm', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\KuaishouVideoClient\\#萌妹子.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '3xwzr5dveyqc5fa', 'chunk_size': 1048576}}, {'name': 'KuaishouVideoClient', 'test_url': 'https://www.kuaishou.com/short-video/3xjpwzyparcgnck?authorId=3xbbsmxr7cdmhqs', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'KuaishouVideoClient', 'raw_data': {}, 'title': '带领男女老少共练传统技艺宫廷盘杠，看着大家的进步我很欣慰！ #快成长计划#文娱百科明日之星#宫廷盘杠#公园健身', 'cover_url': 'https://p2.a.yximgs.com/upic/2025/10/26/18/BMjAyNTEwMjYxODQxMTBfNTM5MTc3Nl8xNzgzNDk1NTk4OTRfMV8z_Ba9a4f4058c21a953cc4648f4fa88e772.jpg?tag=1-1775201695-xpcwebdetail-0-qlczycci9a-ddc47caafc0164f3&clientCacheKey=3xjpwzyparcgnck.jpg&di=725cc0a9&bp=10004', 'err_msg': '', 'download_url': 'https://k0u3dyaay3ay1bzw240ex96cx6400x305xx1bz.djvod.ndcimgs.com/upic/2025/10/26/18/BMjAyNTEwMjYxODQxMTBfNTM5MTc3Nl8xNzgzNDk1NTk4OTRfMV8z_b_B912fef93dee07a30da9063b5201811ed.mp4?tag=1-1775201695-unknown-0-uclkwlwi30-317b2c2fae7bbea8&provider=self&clientCacheKey=3xjpwzyparcgnck_b.mp4&di=725cc0a9&bp=10004&x-ks-ptid=178349559894&kwai-not-alloc=self-cdn&kcdntag=p:Shanghai;i:ChinaTelecom;ft:UNKNOWN;h:COLD;pn:kuaishouVideoProjection&ocid=300000489&tt=b&ss=vps', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\KuaishouVideoClient\\带领男女老少共练传统技艺宫廷盘杠，看着大家的进步我很欣慰！ #快成长计划#文娱百科明日之星#宫廷盘杠#公园健身.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '3xjpwzyparcgnck', 'chunk_size': 1048576}}, {'name': 'KuaishouVideoClient', 'test_url': 'https://www.kuaishou.com/short-video/3x5k4yswvs3k9r9?authorId=3x9uj94tctww7fy', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'KuaishouVideoClient', 'raw_data': {}, 'title': '#正常穿搭无不良引 导#喜爱度激励计划#已成年#甜也是妹@你头发乱了^@我爱一个鞍山人@阴雨天', 'cover_url': 'https://p2.a.yximgs.com/upic/2025/11/08/07/BMjAyNTExMDgwNzUxNTlfMzk4Mzk3MTU4M18xNzkzMjU5NDA3ODFfMl8z_B72b3e1efeca987155a304e45e585458c.jpg?tag=1-1775201714-xpcwebdetail-0-h7xbz4inhd-098dee174d0f2ae8&clientCacheKey=3x5k4yswvs3k9r9.jpg&di=725cc0a9&bp=10004', 'err_msg': '', 'download_url': 'https://k0u3dyaay3ay1azw240ex96cx6400x305xx1az.djvod.ndcimgs.com/upic/2025/11/08/07/BMjAyNTExMDgwNzUxNTlfMzk4Mzk3MTU4M18xNzkzMjU5NDA3ODFfMl8z_b_B546a71c0f574a48148e080bcda789c17.mp4?tag=1-1775201714-unknown-0-uovpqkvfrb-81cdcad9cc974a22&provider=self&clientCacheKey=3x5k4yswvs3k9r9_b.mp4&di=725cc0a9&bp=10004&x-ks-ptid=179325940781&kwai-not-alloc=self-cdn&kcdntag=p:Shanghai;i:ChinaTelecom;ft:UNKNOWN;h:COLD;pn:kuaishouVideoProjection&ocid=300000489&tt=b&ss=vps', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\KuaishouVideoClient\\#正常穿搭无不良引导#喜爱度激励计划#已成年#甜也是妹@你头发乱了^@我爱一个鞍山人@阴雨天.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '3x5k4yswvs3k9r9', 'chunk_size': 1048576}}, {'name': 'KuaishouVideoClient', 'test_url': 'https://v.kuaishou.com/8qIlZu', 'ok': True, 'err_msg': '', 'parse_result': {'source': 'KuaishouVideoClient', 'raw_data': {}, 'title': '#短剧推荐#短剧', 'cover_url': 'https://p2.a.yximgs.com/upic/2024/03/21/13/BMjAyNDAzMjExMzIzMThfMjM4MzgxMjQwMl8xMjc4MjA1MjI0OThfMV8z_Be46362091c4bc1d580a9083a07fac879.jpg?tag=1-1775201733-xpcwebdetail-0-oxedaqz48v-44faaca55fb9b04f&clientCacheKey=3xi5u3rzf5qrgq4.jpg&di=725cc0a9&bp=10004', 'err_msg': '', 'download_url': 'https://v4.oskwai.com/ksc2/PmhgtVQ3IkWX8RgeiHo8_0OLzQCkh48TfyxEffX60I1hdUztVghfsWh6Y3YNUYEDzlvPADGjhtoJznUqcSWSGifuMzdfGaQyTewmZMaB-xTR0hLe0bJ4B4Ke-YBbn_2k5BekmnD76dI3q6kHx8R8jMYRvTDG3TkgKSn9vnUb8oYI86ghtw1i2afHWo2tZ6zi.mp4?pkey=AAXF_MeRki0RCNAh9bFhgUkXuSwO50-NKqnW-O1dHMq_FxYr6aEw9IvnZXI7KcUXD5mn5yY-ScI695sX3QLqYwe1CwaiI6qmpkkp9ynsIo2Lsx_M2A3MeHnus0iUFwzZPBw&tag=1-1775201733-unknown-0-oqfqkt9daq-31aad8ea74ff3751&clientCacheKey=3xi5u3rzf5qrgq4_b.mp4&di=725cc0a9&bp=10004&kwai-not-alloc=40&tt=b&ss=vps', 'default_download_headers': None, 'default_download_cookies': None, 'audio_download_url': '', 'default_audio_download_headers': None, 'default_audio_download_cookies': None, 'ext': 'mp4', 'save_path': 'videodl_tmp_outputs\\KuaishouVideoClient\\#短剧推荐#短剧.mp4', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}, 'audio_ext': 'm4a', 'audio_save_path': '', 'guess_audio_ext_result': {}, 'download_with_ffmpeg': False, 'ffmpeg_settings': {}, 'enable_nm3u8dlre': None, 'nm3u8dlre_settings': {}, 'download_with_aria2c': False, 'aria2c_settings': {}, 'identifier': '8qIlZu', 'chunk_size': 1048576}}]},
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
    video_info = VideoInfo.fromdict(sample["parse_result"])
    print(f"[Preview] Downloading via {client_name}: {sample['test_url']}")
    try:
        video_info = client.download([video_info])[0]
    except Exception as err:
        print(f"[Preview] client.download failed: {err!r}")
    src_path = video_info.save_path
    download_url = video_info.download_url
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
                    status["parse_result"] = video_info.todict() if isinstance(video_info, VideoInfo) else {}
                    err_msg = (video_info or {}).get("err_msg")
                    ok = bool(video_info.with_valid_download_url)
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
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSaved test results to {output_path}")
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