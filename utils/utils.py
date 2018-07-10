# 作者：Charles
# 公众号：Charles的皮卡丘
# 一些工具函数
import os
import re


'''
Input:
	-origin_file: 待转换的视频文件
	-target_format: 目标格式
	-savepath: 转换后的视频文件保存路径
Output:
	-表示转换是否成功的Bool值
'''
# 视频格式转换
def transfer(origin_file, target_format, savepath='results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pattern = re.compile('\..*')
	temp = pattern.sub('.%s' % target_format, origin_file.split('/')[-1])
	target_file = os.path.join(savepath, temp)
	try:
		os.system('{}/utils/ffmpeg.exe -i {} {}'.format(os.getcwd(), origin_file, target_file))
		return True
	except:
		return False