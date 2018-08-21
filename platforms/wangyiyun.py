# 作者： Charles
# 公众号： Charles的皮卡丘
# 网易云课堂视频下载:
# 	-https://study.163.com/
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
class wangyiyun():
	def __init__(self):
		self.info_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
							}
		self.video_headers = {
								'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
								'Host': 'vod.study.163.com',
								'Origin': 'http://study.163.com',
								'Accept': '*/*',
								'Accept-Encoding': 'gzip, deflate',
								'Accept-Language': 'zh-CN,zh;q=0.9',
								'Connection': 'keep-alive',
								'Content-Length': '346',
								'Content-Type': 'application/x-www-form-urlencoded',
								'Referer': None
							}
		self.info_url1 = 'http://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?1534053024193'
		self.info_url2 = 'http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr?1534053176205'
		self.video_url = 'http://vod.study.163.com/eds/api/v1/vod/video'
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
		name = Vurlinfos[1]
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			urllib.request.urlretrieve(download_url, os.path.join(savepath, 'wyy_'+name+'.mp4'))
			return 200
		except:
			with closing(requests.get(download_url, headers=self.info_headers, stream=True, verify=False)) as res:
				if res.status_code == 200:
					with open(os.path.join(savepath, 'wyy_'+name+'.mp4'), "wb") as f:
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
		with closing(requests.get(download_url, headers=self.info_headers, stream=True, verify=False)) as res:
			total_size = int(res.headers['content-length'])
			if res.status_code == 200:
				label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
				with click.progressbar(length=total_size, label=label) as progressbar:
					with open(os.path.join(savepath, 'wyy_'+name+'.mp4'), "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
								progressbar.update(1024)
			else:
				print('[ERROR]:Connect error...')
			return res.status_code
	# 获得视频信息
	def _getvideoinfos(self, url):
		Vid = re.findall(r'courseId=(.*)', url)[0]
		data = {
				'callCount': '1',
				'scriptSessionId': '${scriptSessionId}190',
				'c0-scriptName': 'PlanNewBean',
				'c0-methodName': 'getPlanCourseDetail',
				'c0-id': '0',
				'c0-param0': 'string:' + Vid,
				'c0-param1': 'number:0',
				'c0-param2': 'null:null',
				'batchId': '1534053018270'
				}
		res = requests.post(self.info_url1, data=data, headers=self.info_headers)
		LessonInfo = re.findall(r's\w*?\.id=(.*?);.*?s(\w*?)\.lessonName="(.*?)";', res.text)
		Vurlinfos = []
		i = 0
		for info in LessonInfo:
			i += 1
			Vnum = info[0]
			Vname = str(i) + '_' + info[2].encode('utf-8').decode('unicode_escape', 'ignore')
			data = {
					'callCount': '1',
					'scriptSessionId': '${scriptSessionId}190',
					'c0-scriptName': 'LessonLearnBean',
					'c0-methodName': 'getVideoLearnInfo',
					'c0-id': '0',
					'c0-param0': 'string:' + Vnum,
					'c0-param1': 'string:' + Vid,
					'batchId': '1534053176093'
					}
			res = requests.post(self.info_url2, data=data, headers=self.info_headers)
			videoId = re.findall(r's1\.videoId=(.*?);', res.text)[0]
			signature = re.findall(r's1\.signature="(.*?)";', res.text)[0]
			self.video_headers['Referer'] = 'http://study.163.com/course/courseLearn.htm?courseId={}'.format(Vid)
			data = 'videoId={}&signature={}&clientType=1'.format(videoId, signature)
			res = requests.post(self.video_url, data=data, headers=self.video_headers)
			try:
				download_url = re.findall(r'"videoUrl":"(.*?)"', res.text)[0]
			except:
				download_url = None
			Vurlinfos.append([download_url, Vname])
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'http://study.163.com/course/courseMain.htm?courseId=1003842018'
	# wangyiyun().get(url, savepath='./videos', app='demo')
	wangyiyun().get(url, savepath='./videos', app='cmd')