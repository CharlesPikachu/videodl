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
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
		self.info_url = 'http://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?1530406230904'
		self.video_url = 'http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr?1530407525366'
	# 外部调用
	def get(self, url, savepath='./videos', app='demo'):
		Vurlinfos = self._getvideoinfos(url)
		if app == 'cmd':
			for Vurlinfo in Vurlinfos:
				res = self._download_cmd(Vurlinfo, savepath)
		elif app == 'demo':
			for Vurlinfo in Vurlinfos:
				res = self._download_demo(Vurlinfo, savepath)
		else:
			res = None
		return res
	# Demo用
	def _download_demo(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = Vurlinfos[1]
		download_url = Vurlinfos[0]
		try:
			urllib.request.urlretrieve(download_url, os.path.join(savepath, 'wyy_'+name+'.flv'))
			return 200
		except:
			with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
				if res.status_code == 200:
					with open(os.path.join(savepath, 'wyy_'+name+'.flv'), "wb") as f:
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
					with open(os.path.join(savepath, 'wyy_'+name+'.flv'), "wb") as f:
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
				'batchId': '1530406230876'
				}
		res = requests.post(self.info_url, data=data, headers=self.headers)
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
					'batchId': '1530407525332'
					}
			res = requests.post(self.video_url, data=data, headers=self.headers)
			try:
				download_url = re.findall(r'flvHdUrl="(.*?)"', res.text)[0]
			except:
				download_url = None
			Vurlinfos.append([download_url, Vname])
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'http://study.163.com/course/courseMain.htm?courseId=1003842018'
	# wangyiyun().get(url, savepath='./videos', app='demo')
	wangyiyun().get(url, savepath='./videos', app='cmd')