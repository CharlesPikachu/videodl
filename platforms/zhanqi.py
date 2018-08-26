# 作者：Charles
# 公众号：Charles的皮卡丘
# 战旗视频下载:
# 	-https://videos.zhanqi.tv/
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
class zhanqi():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						}
		self.info_url = 'https://www.zhanqi.tv/api/static/v2.2/video/{}.json'
	# 外部调用
	def get(self, url, savepath='./videos', app='demo'):
		Vurlinfos = self._getvideoinfos(url)
		res = None
		if app == 'cmd':
			res = self._download_cmd(Vurlinfos, savepath)
		elif app == 'demo':
			res = self._download_demo(Vurlinfos, savepath)
		return res
	# Demo用
	def _download_demo(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'zhanqi_' + Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_m3u8(download_url, name)
			return 200
		except:
			return 404
	# Cmd用
	def _download_cmd(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'zhanqi_' + Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_m3u8(download_url, name)
			return 200
		except:
			return 404
	# 获得视频信息
	def _getvideoinfos(self, url):
		vid = url.split('/')[-1].split('.')[0]
		res = requests.get(self.info_url.format(vid), headers=self.headers)
		res_json = json.loads(res.text)
		try:
			title = res_json['data']['title'].replace('\\', '').replace('/', '').replace('.', '')
			if not title:
				raise ValueError('title is None...')
		except:
			title = vid
		try:
			download_url = res_json['data']['playUrl']
		except:
			download_url = None
		Vurlinfos = [download_url, title]
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'https://www.zhanqi.tv/v2/videos/767817.html'
	# zhanqi().get(url, savepath='./videos', app='demo')
	zhanqi().get(url, savepath='./videos', app='cmd')