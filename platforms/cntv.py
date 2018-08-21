# 作者：Charles
# 公众号：Charles的皮卡丘
# CNTV视频下载:
# 	-http://tv.cntv.cn/
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
requests.packages.urllib3.disable_warnings()


'''
Input:
	-url: 视频地址
	-savepath: 视频下载后保存的路径
	-app: 在cmd窗口运行还是在Demo中调用该类
Output:
	-返回下载响应码
'''
class cntv():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
		self.info_url = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={}'
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
		name = 'cntv_' + Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_tms(download_url, name, savepath='./videos')
			return 200
		except:
			return 404
	# Cmd用
	def _download_cmd(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'cntv_' + Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_tms(download_url, name, savepath='./videos')
			return 200
		except:
			return 404
	# 获得视频信息
	def _getvideoinfos(self, url):
		pid = url.split('/')[-1]
		res = requests.get(self.info_url.format(pid), headers=self.headers)
		res_json = json.loads(res.text)
		if res_json['ack'] == 'yes':
			title = res_json['title'].replace('\\', '').replace('/', '')
			videos_choice = res_json['video']
			# 选质量最好的下
			for quality in ['chapters4', 'chapters3', 'chapters2', 'chapters', 'lowChapters']:
				if quality in videos_choice:
					quality_infos = videos_choice.get(quality)
					download_url = []
					for qi in quality_infos:
						download_part = qi.get('url')
						if download_part:
							download_url.append(download_part)
					break
		else:
			title = None
			download_url = None
		Vurlinfos = [download_url, title]
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'http://tv.cntv.cn/video/C10881/4ec8c6c1bdd941b0b11280769b036e8b'
	# cntv().get(url, savepath='./videos', app='demo')
	cntv().get(url, savepath='./videos', app='cmd')