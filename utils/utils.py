'''
Function:
	工具函数
Author:
	Charles
微信公众号:
	Charles的皮卡丘
声明:
	代码仅供学习交流，不得用于商业/非法使用
'''
import os
import click
import requests
import subprocess
from contextlib import closing


'''进度条下载'''
# -------------------------------------------------------------------------------------------
def downloaderBASE(url, savename, savepath, headers, stream=True, verify=False):
	checkFolder(savepath)
	with closing(requests.get(url, headers=headers, stream=stream, verify=verify)) as res:
		total_size = int(res.headers['content-length'])
		if res.status_code == 200:
			label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
			with click.progressbar(length=total_size, label=label) as progressbar:
				with open(os.path.join(savepath, savename), "wb") as f:
					for chunk in res.iter_content(chunk_size=1024):
						if chunk:
							f.write(chunk)
							progressbar.update(1024)
			return True
		else:
			return False
# -------------------------------------------------------------------------------------------


'''检查是否有目标文件夹, 若无, 则创建'''
# -------------------------------------------------------------------------------------------
def checkFolder(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)
	return True
# -------------------------------------------------------------------------------------------


'''
Function:
	视频合并
Input:
	--videos_dict: 待合并的视频集合, 格式为{idx: 'path+vname'}
	--outpath: 合并后的视频保存路径
	--outname: 合并后的视频文件名
Output:
	--is_success: 表示合并是否成功的Bool值	
'''
# -------------------------------------------------------------------------------------------
def mergeVideos(videos_dict, outpath, outname):
	checkFolder(outpath)
	try:
		filelistpath = 'filelist.txt'
		with open(filelistpath, 'w') as f:
			for i in range(len(videos_dict.keys())):
				f.write('file ' + videos_dict.get(i) + '\n')
		subprocess.call('ffmpeg -f concat -i %s -c copy %s' % (filelistpath, os.path.join(outpath, outname)), shell=True)
		while True:
			if os.path.isfile(os.path.join(outpath, outname)):
				for i in range(len(videos_dict.keys())):
					os.remove(videos_dict.get(i))
				os.remove(filelistpath)
				break
		is_success = True
	except:
		is_success = False
	return is_success
# -------------------------------------------------------------------------------------------


'''
Function:
	TMS视频下载
Input:
	--video_urls: 视频地址集合
	--savepath: 视频下载后的保存路径
	--savename: 视频保存名称
	--max_retries: 下载失败最大重试次数
Output:
	--is_success: 下载是否成功的Bool值	
'''
# -------------------------------------------------------------------------------------------
def downloadTMS(video_urls, savename, savepath='videos', max_retries=5, headers=None):
	checkFolder(savepath)
	if headers is None:
		headers = {
					'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
				}
	videos_dict = dict()
	i = -1
	is_success = False
	while True:
		i += 1
		if i == len(video_urls):
			is_success = mergeVideos(videos_dict=videos_dict, outpath=savepath, outname=savename)
			break
		if max_retries < 1:
			is_success = False
			break
		video_url = video_urls[i]
		flag = downloaderBASE(video_url, savename='temp_%d.%s' % (i, savename.split('.')[-1]), savepath=savepath, headers=headers, stream=True, verify=False)
		if not flag:
			i -= 1
			max_retries -= 1
		else:
			videos_dict[i] = savepath + '/temp_%d.%s' % (i, savename.split('.')[-1])
	return is_success
# -------------------------------------------------------------------------------------------