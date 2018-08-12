# 作者：Charles
# 公众号：Charles的皮卡丘
# 音悦台MV下载:
# 	-http://www.yinyuetai.com
import os
import re
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
class yinyuetai():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
		self.info_url = 'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId={}'
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
			urllib.request.urlretrieve(download_url, os.path.join(savepath, 'yyt_'+name+'.mp4'))
			return 200
		except:
			with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
				if res.status_code == 200:
					with open(os.path.join(savepath, 'yyt_'+name+'.mp4'), "wb") as f:
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
		with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
			total_size = int(res.headers['content-length'])
			if res.status_code == 200:
				label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
				with click.progressbar(length=total_size, label=label) as progressbar:
					with open(os.path.join(savepath, 'yyt_'+name+'.mp4'), "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
								progressbar.update(1024)
			else:
				print('[ERROR]:Connect error...')
			return res.status_code
	# 获得视频信息
	def _getvideoinfos(self, url):
		mvid = url.split('/')[-1]
		res = requests.get(self.info_url.format(mvid), headers=self.headers)
		pattern = re.compile(r'http://\w*?\.yinyuetai\.com/uploads/videos/common/.*?(?=&br)')
		re_result = re.findall(pattern, res.text)
		# 选择质量最佳的视频
		download_url = re_result[-1]
		Vurlinfos = [download_url, mvid]
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'http://v.yinyuetai.com/video/3247548'
	# yinyuetai().get(url, savepath='./videos', app='demo')
	yinyuetai().get(url, savepath='./videos', app='cmd')