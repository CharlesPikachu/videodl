'''
Function:
	视频下载器v2.0.0-cmd版, 目前支持的平台:
		--tecent: 腾讯视频
		--yinyuetai: 音悦台MV
		--CNTV: 中国网络电视台
Author:
	Charles
微信公众号:
	Charles的皮卡丘
声明:
	代码仅供学习交流，不得用于商业/非法使用
'''
import sys
from platforms import *
sys.path.append('ffmpeg')


'''视频下载器'''
class VideoDownloader():
	def __init__(self, **kwargs):
		self.INFO = '''************************************************************
Author: Charles
微信公众号: Charles的皮卡丘
Function: 视频下载器 V2.0.0
操作帮助:
	输入r: 返回主菜单(即重新选择平台号)
	输入q: 退出程序
视频保存路径:
	当前路径下的videos文件夹内
************************************************************
'''
		self.RESOURCES = ['腾讯视频', '音悦台MV', 'CNTV中国网络电视台']
		self.platform_now = None
		self.platform_now_name = None
		self.is_select_platform = False
	'''外部调用'''
	def run(self):
		self.platform_now, self.platform_now_name = self.__selectPlatform()
		self.is_select_platform = True
		while True:
			print(self.INFO)
			url = self.__input('[%s-INFO]: 请输入视频链接 --> ' % self.platform_now_name)
			try:
				res = self.__download(url, 'videos')
				if not res:
					raise RuntimeError('error')
			except:
				print('<ERROR>--链接解析失败, 请确定输入的链接与平台对应--<ERROR>')
	'''下载视频'''
	def __download(self, url, savepath='videos'):
		return self.platform_now.get(url=url, savepath=savepath)
	'''选择平台'''
	def __selectPlatform(self):
		while True:
			print(self.INFO)
			print('目前支持的平台:')
			for idx, resource in enumerate(self.RESOURCES):
				print('--%d. %s' % ((idx+1), resource))
			platform_idx = self.__input('请选择平台号(1-%d):' % len(self.RESOURCES))
			if platform_idx == '1':
				return tecent.tecent(), 'tecent'
			elif platform_idx == '2':
				return yinyuetai.yinyuetai(), 'yinyuetai'
			elif platform_idx == '3':
				return cntv.cntv(), 'cntv'
			else:
				print('<ERROR>--平台号输入有误, 请重新输入--<ERROR>')
	'''处理用户输入'''
	def __input(self, tip=None):
		if tip is None:
			user_input = input()
		else:
			user_input = input(tip)
		if user_input.lower() == 'q':
			print('Bye...')
			sys.exit(-1)
		elif user_input.lower() == 'r':
			self.is_select_platform = False
			if not self.is_select_platform:
				self.platform_now, self.platform_now_name = self.__selectPlatform()
				self.is_select_platform = True
			return None
		else:
			return user_input


'''run'''
if __name__ == '__main__':
	try:
		VideoDownloader().run()
	except KeyboardInterrupt:
		print('Bye...')
		sys.exit(-1)