# 作者：Charles
# 公众号：Charles的皮卡丘
# 一些工具函数/类
import os
import re
import sys
import time
import click
import requests
import urllib.parse as urlparse
from contextlib import closing


# 视频转换
#########################################################################################################################
'''
Function: 视频格式转换
Input:
	-origin_file: 待转换的视频文件
	-target_format: 目标格式
	-savepath: 转换后的视频文件保存路径
Output:
	-表示转换是否成功的Bool值
'''
def transfer(origin_file, target_format, savepath='results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pattern = re.compile('\..*')
	temp = pattern.sub('.%s' % target_format, origin_file.split('/')[-1])
	target_file = os.path.join(savepath, temp)
	try:
		os.system('{}/utils/ffmpeg.exe -i {} {}'.format(os.getcwd(), origin_file, target_file))
		return True
	except:
		return False
#########################################################################################################################


# 视频合并
#########################################################################################################################
'''
Function: 将下载的视频合并(CNTV中用到了)
Input:
	-videos_dict: 待合并的视频集合, 格式为{idx: 'path+vname'}
	-outpath: 合并后的视频保存路径
	-outname: 合并后的视频文件名
Output:
	-表示合并是否成功的Bool值	
'''
def videos_merge(videos_dict, outpath, outname):
	print('[INFO]: Start to merge video files...')
	if not os.path.exists(outpath):
		os.mkdir(outpath)
	outfile = ''
	for i in range(len(videos_dict.keys())):
		if not outfile:
			outfile = open(os.path.join(outpath, outname), 'wb')
		infile = open(videos_dict.get(i), 'rb')
		outfile.write(infile.read())
		infile.close()
		os.remove(videos_dict.get(i))
	if outfile:
		outfile.close()
		return True
	else:
		return False
#########################################################################################################################


# 切片格式(TMS)-视频下载
#########################################################################################################################
'''
Function: TMS-视频下载
Input:
	-video_urls: 视频地址集合
	-savepath: 视频下载后的保存路径
	-savename: 视频保存名称
	-max_retry: 下载失败最大重试次数
Output:
	-表示合并是否成功的Bool值	
'''
def download_tms(video_urls, savename, savepath='./videos', max_retry=5, headers=None):
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
			videos_merge(videos_dict=videos_dict, outpath=savepath, outname=savename)
			is_success = True
			break
		if max_retry < 1:
			is_success = False
			break
		video_url = video_urls[i]
		with closing(requests.get(video_url, headers=headers, stream=True, verify=False)) as res:
			total_size = int(res.headers['content-length'])
			tempfile = os.path.join(savepath, 'temp_%d.%s' % (i, savename.split('.')[-1]))
			if res.status_code == 200:
				label = '<%d>.[FileSize]:%0.2f MB' % (i, total_size/(1024*1024))
				with click.progressbar(length=total_size, label=label) as progressbar:
					with open(tempfile, "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
								progressbar.update(1024)
				videos_dict[i] = tempfile
			else:
				max_retry -= 1
				i -= 1
	return is_success
#########################################################################################################################


# m3u8-视频下载
#########################################################################################################################
# m3u8格式解析
class parse_download_m3u8():
	def __init__(self, pool_size=50, retry=3):
		self.pool_size = pool_size
		self.retry = retry
		self.session = self.__create_session()
		self.downed = {}
		self.fail_down = []
	# 外部调用
	def run(self, video_url, savepath, savename):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		if os.path.isfile(os.path.join(savepath, savename)):
			return False
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
		else:
			raise RuntimeError('Connect error...')
		self.__merge_file()
	# 下载传输流文件(全部)
	def __download(self, ts_zip):
		for ts_tuple in ts_zip:
			self.__worker(ts_tuple)
		if self.fail_down:
			ts_list = self.fail_down
			self.fail_down = []
			self.__download(ts_list)
	# 下载传输流文件(单个)
	def __worker(self, ts_tuple):
		url = ts_tuple[0]
		idx = ts_tuple[1]
		retry = self.retry
		while retry:
			try:
				res = self.session.get(url, timeout=30)
				if res.ok:
					filename = url.split('/')[-1].split('?')[0].replace('\\', '').replace('/', '')
					with open(os.path.join(self.savepath, filename), 'wb') as f:
						f.write(res.content)
					self.downed[idx] = filename
					show_progress_bar(len(self.downed), self.num_ts)
					return True
			except:
				retry -= 1
		self.fail_down.append((url, idx))
		return False
	# 合并下载的流文件
	def __merge_file(self):
		print('[INFO]: Start to merge video files...')
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
		print('[INFO]: Merge video files successfully...')
	# 创建Session
	def __create_session(self):
		session = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=self.pool_size, pool_maxsize=self.pool_size, max_retries=self.retry)
		session.mount('https://', adapter)
		session.mount('http://', adapter)
		return session

'''
Function: 下载m3u8格式的视频
Input:
	-video_url: 视频地址
	-savepath: 视频下载后的保存路径
	-savename: 视频保存名称
Output:
	-是否下载成功的Bool值
'''
def download_m3u8(video_url, savename, savepath='./videos'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	if os.path.isfile(os.path.join(savepath, savename)):
		return 200
	try:
		parse_download_m3u8().run(video_url, savepath, savename)
		return 200
	except:
		try:
			os.system('{}/utils/ffmpeg.exe -i {} -c copy {}'.format(os.getcwd(), '"%s"' % video_url, os.path.join(savepath, savename)))
			return 200
		except:
			return 404
#########################################################################################################################


# 简单实现进度条
#########################################################################################################################
def show_progress_bar(num, total):
	rate_num = int((float(num) / float(total)) * 100)
	progress_bar = '\r下载进度: [%s%s]%d%%' % ('#'*(rate_num//2), ' '*(50-rate_num//2), rate_num)
	sys.stdout.write(progress_bar)
	sys.stdout.flush()
#########################################################################################################################