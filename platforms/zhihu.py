# 作者：Charles
# 公众号：Charles的皮卡丘
# 知乎视频下载:
# 	-https://www.zhihu.com/
import os
import re
import sys
import json
import click
import urllib
import requests
from contextlib import closing
sys.path.append('..')
from utils.utils import *


'''
Input:
	-url: 视频地址
	-savepath: 视频下载后保存的路径
	-app: 在cmd窗口运行还是在Demo中调用该类
Output:
	-返回下载响应码
'''
class zhihu():
	def __init__(self):
		self.headers = {
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'Authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
					}
		self.video_url = 'https://lens.zhihu.com/api/videos/{}'
	# 外部调用
	def get(self, url, savepath='./videos', app='demo'):
		Vurlinfos = self._getvideoinfos(url)
		res = None
		if app == 'cmd':
			for Vurlinfo in Vurlinfos:
				res = self._download_cmd(Vurlinfo, savepath)
		elif app == 'demo':
			for Vurlinfo in Vurlinfos:
				res = self._download_demo(Vurlinfo, savepath)
		return res
	# Demo用
	def _download_demo(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		try:
			download_m3u8(download_url, name)
			return 200
		except:
			return None
	# Cmd用
	def _download_cmd(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		download_m3u8(download_url, name)
		try:
			download_m3u8(download_url, name)
			return 200
		except:
			return None
	# 获得视频信息
	def _getvideoinfos(self, url):
		res = requests.get(url=url, headers=self.headers)
		vids = re.findall(r'zhihu\.com/video/(\d*?)</span>', res.text)
		Vurlinfos = []
		for vid in vids:
			res = requests.get(url=self.video_url.format(vid), headers=self.headers)
			res_json = json.loads(res.text)
			try:
				Vname = res_json['title']
				if not Vname.strip():
					Vname = str(vid)
			except:
				Vname = str(vid)
			download_url = None
			# 有多种视频质量(下载质量最高的)
			if 'hd' in res_json['playlist']:
				download_url = res_json['playlist']['hd']['play_url']
			if 'sd' in res_json['playlist'] and download_url is None:
				download_url = res_json['playlist']['hd']['play_url']
			if 'ld' in res_json['playlist'] and download_url is None:
				download_url = res_json['playlist']['hd']['play_url']
			Vurlinfos.append([download_url, Vname])
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'https://www.zhihu.com/question/21395276/answer/425130152'
	# zhihu().get(url, savepath='./videos', app='demo')
	zhihu().get(url, savepath='./videos', app='cmd')