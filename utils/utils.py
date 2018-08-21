# 作者：Charles
# 公众号：Charles的皮卡丘
# 一些工具函数/类
import os
import re
import sys
import time
import requests
import urllib.parse as urlparse


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
	progress_bar = '\r[%s%s]%d%%\n' % ('#'*(rate_num//2), ' '*(50-rate_num//2), rate_num)
	sys.stdout.write(progress_bar)
	sys.stdout.flush()
#########################################################################################################################