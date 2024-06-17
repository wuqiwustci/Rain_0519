import struct
file_path='D:\\program_0519rain\\data\\radar组合反射率\\Z_RADA_C_BABJ_20240518160615_P_DOR_ACHN_CREF_20240518_160000.bin'
def read_header(file_path):
	with open(file_path,'rb') as file:
		model=struct.unpack('4s',file.read(4))[0]
		sample_rate=struct.unpack('H',file.read(2))[0]
		return model,sample_rate
model,sample_rate=read_header(file_path)
print(model,sample_rate)

# 在anaconda prompt中使用以下命令行代码运行此程序
# python D:\program_0519rain\read_radar_file.py
