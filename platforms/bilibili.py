# 作者：Charles
# 公众号：Charles的皮卡丘
# B站视频下载:
# 	-https://www.bilibili.com/
import os
import re
import json
import click
import urllib
import requests
from contextlib import closing


'''
Input:
	-url: 视频地址
	-savepath: 视频下载后保存的路径
	-app: 在cmd窗口运行还是在Demo中调用该类
Output:
	-返回下载响应码
'''
class bilibili():
	def __init__(self):
		self.infoheaders = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'accept-encoding': 'gzip, deflate, br',
						'accept-language': 'zh-CN,zh;q=0.9',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
					}
		self.downheaders = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'accept': '*/*',
						'accept-encoding': 'gzip, deflate, br',
						'accept-language': 'zh-CN,zh;q=0.9',
						'Referer': 'https://search.bilibili.com/all?keyword='
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
		try:
			urllib.request.urlretrieve(download_url, os.path.join(savepath, 'bili_'+name+'.flv'))
			return 200
		except:
			with closing(requests.get(download_url, headers=self.downheaders, stream=True, verify=False)) as res:
				if res.status_code == 200:
					with open(os.path.join(savepath, 'bili_'+name+'.flv'), "wb") as f:
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
		with closing(requests.get(download_url, headers=self.downheaders, stream=True, verify=False)) as res:
			total_size = int(res.headers['content-length'])
			if res.status_code == 200:
				label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
				with click.progressbar(length=total_size, label=label) as progressbar:
					with open(os.path.join(savepath, 'bili_'+name+'.flv'), "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
								progressbar.update(1024)
			else:
				print('[ERROR]:Connect error...')
			return res.status_code
	# 获得视频信息
	def _getvideoinfos(self, url):
		res = requests.get(url=url, headers=self.infoheaders)
		pattern = '.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__='
		re_result = re.findall(pattern, res.text)[0]
		temp = json.loads(re_result)
		download_url = temp['durl'][0]['url']
		if 'mirrork' in download_url:
			vid = download_url.split('/')[6]
		else:
			vid = download_url.split('/')[7]
			if len(vid) >= 10:
				vid = download_url.split('/')[6]
		Vurlinfos = [download_url, vid]
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'https://www.bilibili.com/video/av26443123?spm_id_from=333.338.__bofqi.13'
	# bilibili().get(url, savepath='./videos', app='demo')
	bilibili().get(url, savepath='./videos', app='cmd')