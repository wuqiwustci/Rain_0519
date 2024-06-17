#-*-coding: utf-8-*-  
#@Author: wq
#@E-mail: 1627453528@qq.com
#生成当前数据列表，标出缺失数据
#这个程序当前只是一个草稿，因为现在数据下载量不大，一般顶多几百个，很容易人工找出缺失数据，以后有需求再修改完善
#
################################################


import os
import re

###给定时间范围，生成相应的数据文件列表
starttime='2024051600'
endtime='2024052020'
forcast_times='2024051800'
work_path='D:\\program_0519rain\\data\\CPEFS数据'
out_file_name='应存在文件.txt'
filename_match_string='*.dat.xz'
#查找选取文件夹中符合命名的一个文件名，并以该文件名为基础构建应存在文件名
filename_lists=os.listdir(work_path)
filename_example=''
for filename_list in filename_lists:
	if re.match(filename_match_string,filename_list):
		filename_example=filename_list
	if filename_example !=''
	break
filename_full_lists=[]
for forcast_time in forcast_times:
	#查找替换起报时间的相关参数
	pattern_2='\d+_P_WMC'
	repl_2=forcast_time+'_P_WMC'
	filename_example=re.sub(pattern_2,repl_2,filename_example)
	for forcast_hour in [0:49]:
		#查找替换预报时间的相关参数
		pattern_1='ESWC_\d+'
		repl_1='ESWC_'+str(forcast_hour).zfill(2)
		filename_example=re.sub(pattern_1,repl_1,filename_example)
		filename_full_lists.append(filename_example)
		#输出生成的应有数据列表
with open(out_file_name,'w',encoding='utf-8') as out_file:
	for filename_full_list in filename_full_lists:
		out_file.write('%s\n'%filename_full_list)
out_file.close()
#依据文件列表逐一查找该文件是否存在，存在则写入当前数据列表，缺失则写入缺失数据列表
with open(out_file_name,'r',encoding='utf-8') as input_file:
	all_file_lists=input_file.read()
	for all_file_list in all_file_lists:
		filename_check=work_path+all_file_list
		if filename_check in filename_full_lists:
			input_file.write('%s\n'%filename_check)
		else:
			input_file.write('文件缺失：%s\n'%filename_check)

#读取缺失数据列表，逐一查找html文件，在文件中查找下载链接，然后调用下载函数下载