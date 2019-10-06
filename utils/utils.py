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
import sys
import time
import click
import requests
import subprocess
import urllib.parse as urlparse
from contextlib import closing


'''进度条下载'''
# -------------------------------------------------------------------------------------------
def downloadBASE(url, savename, savepath, headers, stream=True, verify=False):
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
	outname = outname.replace(' ', '')
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
	if not video_urls:
		return False
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
		flag = downloadBASE(video_url, savename='temp_%d.%s' % (i, savename.split('.')[-1]), savepath=savepath, headers=headers, stream=True, verify=False)
		if not flag:
			i -= 1
			max_retries -= 1
		else:
			videos_dict[i] = savepath + '/temp_%d.%s' % (i, savename.split('.')[-1])
	return is_success
# -------------------------------------------------------------------------------------------


'''
Function:
	m3u8视频下载
Input:
	--video_url: 视频地址
	--savepath: 视频下载后的保存路径
	--savename: 视频保存名称
Output:
	--is_success: 下载是否成功的Bool值	
'''
# -------------------------------------------------------------------------------------------
class m3u8Parser():
	def __init__(self, pool_size=50, max_retries=3, **kwargs):
		self.pool_size = pool_size
		self.max_retries = max_retries
		self.session = self.__createSession()
		self.downed = {}
		self.fail_down = []
		self.savepath = None
		self.savename = None
	'''外部调用'''
	def run(self, video_url, savename, savepath):
		self.savepath = savepath
		self.savename = savename
		res = self.session.get(video_url, timeout=60)
		if res.ok:
			content = res.content
			if content:
				content = content.decode()
				ts_list = [urlparse.urljoin(video_url, line.strip()) for line in content.split('\n') if line and not line.startswith("#")]
				self.num_ts = len(ts_list)
				if ts_list:
					ts_zip = zip(ts_list, [i for i in range(self.num_ts)])
					self.__download(ts_zip)
			print()
			self.__mergeFile()
			return True
		else:
			return False
	'''下载传输流文件(全部)'''
	def __download(self, ts_zip):
		for ts_tuple in ts_zip:
			self.__worker(ts_tuple)
		if self.fail_down:
			ts_list = self.fail_down
			self.fail_down = []
			self.__download(ts_list)
		return True
	'''下载传输流文件(单个)'''
	def __worker(self, ts_tuple):
		url = ts_tuple[0]
		idx = ts_tuple[1]
		max_retries = self.max_retries
		while max_retries:
			try:
				res = self.session.get(url, timeout=30)
				if res.ok:
					filename = url.split('/')[-1].split('?')[0].replace('\\', '').replace('/', '')
					with open(os.path.join(self.savepath, filename), 'wb') as f:
						f.write(res.content)
					self.downed[idx] = filename
					self.__showProgressBar(len(self.downed), self.num_ts)
					return True
			except:
				max_retries -= 1
		self.fail_down.append((url, idx))
		return False
	'''合并下载的流文件'''
	def __mergeFile(self):
		idx = 0
		outfile = ''
		while idx < self.num_ts:
			filename = self.downed.get(idx)
			if filename:
				infile = open(os.path.join(self.savepath, filename), 'rb')
				if not outfile:
					outfile = open(os.path.join(self.savepath, self.savename), 'wb')
				outfile.write(infile.read())
				infile.close()
				os.remove(os.path.join(self.savepath, filename))
				idx += 1
			else:
				time.sleep(1)
		if outfile:
			outfile.close()
		return True
	'''创建Session'''
	def __createSession(self):
		session = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=self.pool_size, pool_maxsize=self.pool_size, max_retries=self.max_retries)
		session.mount('https://', adapter)
		session.mount('http://', adapter)
		return session
	'''简单实现进度条'''
	def __showProgressBar(self, num, total):
		rate_num = int((float(num) / float(total)) * 100)
		progress_bar = '\rTS流文件下载进度: [%s%s]%d%%' % ('#'*(rate_num//2), ' '*(50-rate_num//2), rate_num)
		sys.stdout.write(progress_bar)
		sys.stdout.flush()

def downloadM3U8(video_url, savename, savepath='videos'):
	if not video_url:
		return False
	checkFolder(savepath)
	try:
		is_success = m3u8Parser().run(video_url=video_url, savename=savename, savepath=savepath)
	except:
		os.system('ffmpeg -i {} -c copy {}'.format('"%s"' % video_url, os.path.join(savepath, savename)))
		is_success = True
	return is_success
# -------------------------------------------------------------------------------------------