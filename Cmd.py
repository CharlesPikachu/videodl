# 代码仅供学习交流，不得用于商业/非法使用
# 作者：Charles
# 公众号：Charles的皮卡丘
# 视频下载器-Cmd版
# 目前支持的平台:
# 	网易云课堂: wangyiyun.wangyiyun()
# 	音悦台: yinyuetai.yinyuetai()
# 	B站: bilibili.bilibili()
from platforms import *


def Cmd(options):
	print('-'*36 + '<Welcome>' + '-'*36)
	print('[简介]:视频下载器V1.0')
	print('[Author]:Charles')
	print('[公众号]: Charles的皮卡丘')
	print('[退出方式]: 输入q或者按Ctrl+C键退出')
	print('[目前支持的平台]:')
	for option in options:
		print('*' + option)
	print('-'*81)
	choice = input('请输入平台号(1-3):')
	if choice == 'q' or choice == 'Q':
		print('Bye...')
		exit(-1)
	url = input('请输入视频链接:\n')
	if url == 'q' or url == 'Q':
		print('Bye...')
		exit(-1)
	savepath = './videos'
	if choice == '1':
		try:
			res = wangyiyun.wangyiyun().get(url, savepath, app='cmd')
			if res != 200:
				raise RuntimeError('url request error...')
			print('[INFO]: 视频下载完成，视频保存在{}...'.format(savepath))
		except:
			print('[Error]: 链接解析失败...')
	elif choice == '2':
		try:
			res = yinyuetai.yinyuetai().get(url, savepath, app='cmd')
			if res != 200:
				raise RuntimeError('url request error...')
			print('[INFO]: 视频下载完成，视频保存在{}...'.format(savepath))
		except:
			print('[Error]: 链接解析失败...')
	elif choice == '3':
		try:
			res = bilibili.bilibili().get(url, savepath, app='cmd')
			if res != 200:
				raise RuntimeError('url request error...')
			print('[INFO]: 视频下载完成，视频保存在{}...'.format(savepath))
		except:
			print('[Error]: 链接解析失败...')
	else:
		print('[Error]: 平台号输入错误，必须在(1-3)之间...')


if __name__ == '__main__':
	options = ["1.网易云课堂", "2.音悦台", "3.B站"]
	while True:
		try:
			Cmd(options)
		except KeyboardInterrupt:
			print('Bye...')
			exit(-1)