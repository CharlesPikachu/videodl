# 作者：Charles
# 公众号：Charles的皮卡丘
# TED演讲视频下载:
# 	-https://www.ted.com/talks?language=zh-cn
import os
import re
import json
import click
import urllib
import requests
from contextlib import closing
requests.packages.urllib3.disable_warnings()


'''
Input:
	-url: 视频地址
	-savepath: 视频下载后保存的路径
	-app: 在cmd窗口运行还是在Demo中调用该类
Output:
	-返回下载响应码
'''
class ted():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
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
		name = Vurlinfos[1]
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			urllib.request.urlretrieve(download_url, os.path.join(savepath, 'ted_'+name+'.mp4'))
			return 200
		except:
			with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
				if res.status_code == 200:
					with open(os.path.join(savepath, 'ted_'+name+'.mp4'), "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
				return res.status_code
	# Cmd用
	def _download_cmd(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = Vurlinfos[1]
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
			total_size = int(res.headers['content-length'])
			if res.status_code == 200:
				label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
				with click.progressbar(length=total_size, label=label) as progressbar:
					with open(os.path.join(savepath, 'ted_'+name+'.mp4'), "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
								progressbar.update(1024)
			else:
				print('[ERROR]:Connect error...')
			return res.status_code
	# 获得视频信息
	def _getvideoinfos(self, url):
		res = requests.get(url, headers=self.headers)
		temp = '{' + re.findall(r'"__INITIAL_DATA__"\s*:\s*\{(.+)\}', res.text)[0] + '}'
		temp_json = json.loads(temp)
		title = temp_json['talks'][0]['title']
		if not title:
			title = 'vid' + str(temp_json['talks'][0]['downloads']['id'])
		videos_dict = temp_json['talks'][0]['downloads']['nativeDownloads']
		# 选择质量最好的视频下载
		for quality in ['high', 'medium', 'low']:
			if quality in videos_dict:
				download_url = videos_dict[quality]
				break
		Vurlinfos = [download_url, title]
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'https://www.ted.com/talks/tina_seelig_the_little_risks_you_can_take_to_increase_your_luck?language=zh-cn'
	# ted().get(url, savepath='./videos', app='demo')
	ted().get(url, savepath='./videos', app='cmd')