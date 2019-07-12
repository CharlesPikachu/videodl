'''
Function:
	知乎视频下载: https://www.zhihu.com/
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import json
import requests
from utils.utils import *


'''
Input:
	--url: 视频地址
	--savepath: 视频下载后保存的路径
Output:
	--is_success: 下载是否成功的BOOL值
'''
class zhihu():
	def __init__(self):
		self.headers = {
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'Authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
					}
		self.video_url = 'https://lens.zhihu.com/api/videos/{}'
	'''外部调用'''
	def get(self, url, savepath='videos'):
		video_infos = self.__getvideoinfos(url)
		for info in video_infos:
			is_success = self.__download(info, savepath)
		return is_success
	'''下载'''
	def __download(self, video_infos, savepath):
		checkFolder(savepath)
		download_url = video_infos[0]
		video_name = 'zhihu_' + video_infos[1] + '.mp4'
		try:
			is_success = downloadM3U8(video_url=download_url, savename=video_name, savepath=savepath)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		res = requests.get(url=url, headers=self.headers)
		vids = re.findall(r'zhihu\.com/video/(\d*?)</span>', res.text)
		video_infos = []
		for vid in vids:
			res = requests.get(url=self.video_url.format(vid), headers=self.headers)
			res_json = json.loads(res.text)
			try:
				video_name = res_json['title']
				if not video_name.strip():
					video_name = str(vid)
			except:
				video_name = str(vid)
			download_url = None
			# 有多种视频质量(下载质量最高的)
			if 'hd' in res_json['playlist']:
				download_url = res_json['playlist']['hd']['play_url']
			if 'sd' in res_json['playlist'] and download_url is None:
				download_url = res_json['playlist']['hd']['play_url']
			if 'ld' in res_json['playlist'] and download_url is None:
				download_url = res_json['playlist']['hd']['play_url']
			video_infos.append([download_url, video_name])
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'https://www.zhihu.com/question/21395276/answer/425130152'
	zhihu().get(url, savepath='videos')