'''
Function:
    Implementation of Quickly Validating The Effectiveness Of "videodl.parsefromurl"
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import pickle
from tqdm import tqdm
from videodl.modules import VideoClientBuilder, BaseVideoClient


'''constants'''
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
        'http://xhslink.com/o/6us6UGep1Zw',
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
    'ChinaDailyVideoClient': [
        'https://www.chinadaily.com.cn/a/202604/07/WS69d4c582a310d6866eb42089.html',
        'https://cnews.chinadaily.com.cn/a/202604/08/WS69d5d5b4a310942cc49a6b84.html',
        'https://www.chinadaily.com.cn/a/202603/29/WS69c858cba310d6866eb40728.html',
        'https://cn.chinadaily.com.cn/a/202604/02/WS69ce24d5a310942cc49a632e.html',
    ],
    'EastDayVideoClient': [
        'https://nw.eastday.com/bjzx/20260403/cc9f70957fd8439da55c921920a6f73a.html',
        'https://nw.eastday.com/bjzx/20260405/c526eb2abb2d4fcdb1d96ea9f69fef18.html',
    ],
    'CCTVNewsVideoClient': [
        'https://content-static.cctvnews.cctv.com/snow-book/video.html?item_id=15184105708774284671',
        'https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=7331185547682467513',
    ],
    'WWW163VideoClient': [
        'https://www.163.com/v/video/VDHQNAVSD.html?clickfrom=video_like',
        'https://www.163.com/v/video/VKP3BLEQV.html?clickfrom=video_hot',
        'https://www.163.com/v/video/VIN2DAA00.html?clickfrom=video_like',
    ],
}


'''main'''
def main(save_path='test_results.pkl'):
    modules_summary = []
    for client_name, client_module in VideoClientBuilder.REGISTERED_MODULES.items():
        print(f"\n[Module] {client_name}")
        client: BaseVideoClient = client_module()
        num_valid = 0
        for candidate_url in tqdm(VIDEODL_TEST_SAMPLES[client_name]):
            video_info = client.parsefromurl(candidate_url)[0]
            status = {"name": client_name, "ok": False, "error_msg": None, "test_url": candidate_url, "parse_result": video_info.todict()}
            if not video_info.with_valid_download_url:
                status.update(dict(error_msg=video_info['err_msg'], ok=False))
            else:
                num_valid += 1
                status.update(dict(ok=True))
            modules_summary.append(status)
        print(f"  Parsed video urls: {num_valid}/{len(VIDEODL_TEST_SAMPLES[client_name])}")
    with open(save_path, 'wb') as fp:
        pickle.dump(modules_summary, fp)
    print(f"Saved test results to {save_path}")


'''tests'''
if __name__ == '__main__':
    main()