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
        'https://tieba.baidu.com/p/6098286801', 
        'https://tieba.baidu.com/p/7280373361'
    ],
    'MGTVVideoClient': [
        'https://www.mgtv.com/l/100026064/19868457.html?fpa=1684&fpos=&lastp=ch_home&cpid=5',
        'https://www.mgtv.com/b/788366/23780111.html?fpa=1756&fpos=&lastp=ch_home', # requires pass VIP login-in cookies by default_download_cookies to download full video
        'https://www.mgtv.com/b/805972/23756299.html?fpa=1261&fpos=&lastp=ch_home&cpid=5', # requires pass login-in cookies by default_download_cookies to download full video
    ],
    'ZhihuVideoClient': [
        'https://www.zhihu.com/question/38557752/answer/2280634747',
        'https://www.miguvideo.com/p/detail/958634941?lastLocation=b1c29dcd91f94a0289bf6295140f43b2%23261fe51d763b4a86bb272aaa9de47b49',
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
        'https://www.huya.com/video/play/1084317636.html',
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
}
PARSE_SUPPLEMENT = {
    'Ku6VideoClient': {'name': 'Ku6VideoClient', 'display_name': 'Ku6VideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'Ku6VideoClient', 'test_url': 'https://www.ku6.com/video/detail?id=McZoSe_hgG_jwzy7pQLqvMJ3IoI.', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'Ku6VideoClient', 'download_url': 'https://rbv01.ku6.com/wifi/o_1f9dtdubn8l8154lddtcdtdusm', 'title': '看到泪崩！微视频百年风华', 'file_path': 'videodl_tmp_outputs\\Ku6VideoClient\\看到泪崩！微视频百年风华.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'requests.head', 'ok': True}}}, {'name': 'Ku6VideoClient', 'test_url': 'https://www.ku6.com/video/detail?id=HE3lfhcp13Gd0qND4zfzXYQONMY.', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'Ku6VideoClient', 'download_url': 'https://rbv01.ku6.com/wifi/o_1evr90gl2sdhjs4nn31bad1v3ue', 'title': '微视频｜领航新征程', 'file_path': 'videodl_tmp_outputs\\Ku6VideoClient\\微视频｜领航新征程.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': 'NULL', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'requests.head', 'ok': True}}}]},
    'WeishiVideoClient': {'name': 'WeishiVideoClient', 'display_name': 'WeishiVideoClient', 'success_count': 2, 'total_count': 2, 'success_rate': 1.0, 'status': 'ok', 'tests': [{'name': 'WeishiVideoClient', 'test_url': 'https://h5.weishi.qq.com/weishi/feed/76EaWNkEF1IqtfYVH/', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'WeishiVideoClient', 'download_url': 'http://v.weishi.qq.com/tjg_2012262636_1047_e167370371ca4988a45e2b0ed039vide.f30.mp4?dis_k=1ff643abe43d47772c6fcd1e0c6504c5&dis_t=1764139343&fromtag=0&pver=5.8.5&weishi_play_expire=1764182543&wsadapt=_1126144223__367349920_0_0_0_2_8_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW&wsadapt=_1126144223__367349920_0_0_0_2_0_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW', 'title': '自己烤的串，果然比外面卖的便宜又好吃！', 'file_path': 'videodl_tmp_outputs\\WeishiVideoClient\\自己烤的串，果然比外面卖的 便宜又好吃！.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': '76EaWNkEF1IqtfYVH', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}, {'name': 'WeishiVideoClient', 'test_url': 'https://isee.weishi.qq.com/ws/app-pages/share/index.html?wxplay=1&id=7siJelmUp1MkDSPeo&spid=3704775550396963513&qua=v1_and_weishi_8.81.0_590_312026001_d&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011', 'ok': True, 'err_msg': 'NULL', 'parse_result': {'source': 'WeishiVideoClient', 'download_url': 'http://v.weishi.qq.com/gzc_1594_1047_0bc35eac6aaamuaip6jm7fqrp2ief7uqal2a.f70.mp4?dis_k=6cfc9fe3c0374579f29d72756e638ff0&dis_t=1764139358&fromtag=0&pver=1.0.0&weishi_play_expire=1764182558&wsadapt=_1126144238__160236066_0_0_0_27_2_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW&wsadapt=_1126144238__160236066_0_0_0_27_0_0_0_0_0_0&qua=V1_HT5_QZ_3.0.0_001_IDC_NEW', 'title': '古装片，就是这样排出来的', 'file_path': 'videodl_tmp_outputs\\WeishiVideoClient\\古装片，就是这样排出来的.mp4', 'ext': 'mp4', 'download_with_ffmpeg': False, 'err_msg': 'NULL', 'identifier': '7siJelmUp1MkDSPeo', 'guess_video_ext_result': {'ext': 'mp4', 'sniffer': 'urllib.parse', 'ok': True}}}]}
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