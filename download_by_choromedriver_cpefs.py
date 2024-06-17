#-*-coding: utf-8-*-  
#@Author: wq
#@E-mail: 1627453528@qq.com
#使用python操作chrome自动下载天擎数据
#依据url列表下载CPEFS数据
#
################################################


import os
from bs4 import BeautifulSoup

import pandas as pd
from time import sleep
from selenium import webdriver
# Service一定要记得导入，要用它来指定调用的chromedriver路径
from selenium.webdriver.chrome.service import Service


###自定义函数，将存放文件夹中所有html文件的下载链接那一栏提取出来
#输入参数包括html文件存放文件夹radarData_url_folder,下载链接所在列数url_rowNumber，下载链接那列表头所含字符串thead_string
#输出完整的下载链接txt文件名
# #需要导入的库如下
# import os
# from bs4 import BeautifulSoup
def write_url_list_file(radarData_url_folder,url_rowNumber,thead_string):
    #列出该文件夹下所有文件
    radarData_url_filenames=os.listdir(radarData_url_folder)
    radarData_url_file_count=0
    #初始化下载链接列表数组
    column_datas=[]
    for filename in radarData_url_filenames:
        #只在html文件中查找下载链接
        if '.html' in filename:
            #构建完整的html文件名，在windows系统中涉及到文件地址一般都要用双引号而非单引号，用双斜杆而非单斜杠
            filename=radarData_url_folder+"\\"+filename
            #将数组中的文件名替换为完整文件名，方便后续代码验证查错
            radarData_url_filenames[radarData_url_file_count]=filename
            radarData_url_file_count+=1
            #输出html文件名，方便查错
            print('html文件: '+filename)
            #打开html文件，一定要记得设置编码，不然会以错误的编码方式打开
            with open(filename,'r',encoding='utf-8') as file:
                html_content=file.read()
            #读取html文件
            soup=BeautifulSoup(html_content,'lxml')
            ##是不是因为用beautifulsoup打开解析了这个文件，所以后面用find或find_all查找'tr'或'td'就能查找行或列
            #读取其中表格
            table=soup.find('table')
            #读取表格每一行
            rows=table.find_all('tr')
            for row in rows:
                #读取每一行中的每一列
                cells=row.find_all('td')
                #提取第url_rowNumber列，该列为下载链接
                cell=cells[url_rowNumber-1]
                #第一行为表头需要去掉，所以用是否含'文件'字符串作为条件将其去掉
                if cell and not(thead_string in str(cell)):
                    column_datas.append(cell.get_text())
            #关掉打开的html文件
            file.close()
    #将读取的下载链接字符串数组写成txt文件
    with open(radarData_url_folder+"\\"+url_filename,'w',encoding='utf-8') as outfile:
        #一行一行写入
        for column_data in column_datas:
            outfile.write("%s\n" % column_data)
    #写完关闭下载链接txt文件
    outfile.close()
    #返回完整的下载链接txt文件名
    return(radarData_url_folder+"\\"+url_filename)


###自定义函数，依据下载链接txt文件来调用chromedriver下载数据
#将下载链接一个个填入浏览器地址栏来下载数据
#输入下载数据保存文件夹rada_data_download_folder，chromedriver所在路径chromedriver_pat，下载链接txt文件路径url_file_path，下载时间间隔sleep_time_1、sleep_time_2、sleep_time_3
#输出下载链接个数
# #需要导入的库如下
# import pandas as pd
# from time import sleep
# from selenium import webdriver
# Service一定要记得导入，要用它来指定调用的chromedriver路径
# from selenium.webdriver.chrome.service import Service
def download_by_chrome_and_url_txt(rada_data_download_folder,chromedriver_path,url_file_path,sleep_time_1,sleep_time_2,sleep_time_3):
    #配置selenium的参数
    #是否是获取chrome浏览器默认参数的意思
    options = webdriver.ChromeOptions()
    #修改默认参数中的部分参数，如下载路径
    prefs = {'profile.default_content_settings.popups': 0,      #指定不弹出窗口
             'download.default_directory': rada_data_download_folder   #指定下载路径，注意使用双反斜杠
            }
    options.add_experimental_option('prefs', prefs)
    #指定chromedriver的存放路径，不然可能报错，因为找不到chromedriver
    service = Service(chromedriver_path)
    #使用设定的两项参数来设置chrome驱动器
    driver=webdriver.Chrome(service=service,options=options)

    # # 登录模块，当前不需要，以后其他数据下载可能用得上
    # # driver.get('http://10.159.90.120:8108/music-ws')
    # # username = driver.find_element_by_id("BENN_RYB_TIANGONG")
    # # password = driver.find_element_by_id("Tiangong@4208034")
    # # username.send_keys("用户名")   #程序在username文本框中填入用户名
    # # password.send_keys("密码")     #程序在password文本框中填入密码
    # # driver.find_element_by_name("commit").click() #程序自动点击Log In按钮,完成用户登录

    datalink=url_file_path  #数据下载链接txt文档，每行一个下载链接
    with open(datalink,'r') as fr:
        urlList=fr.readlines()
        n=0
        for url in urlList:
            driver.get(url)   #程序不断的在浏览器地址栏填入下载链接
            n=n+1
            #每个下载间隔多少秒，到达6个后间隔多少秒
            if n%6!=0:
                sleep(sleep_time_1)
            else:
                sleep(sleep_time_2)
        sleep(sleep_time_3)
        driver.quit()
    return(n)


#html文件存放文件夹，在windows系统中涉及到文件地址都要用双用双斜杆而非单斜杠，不知是否要用双引号
radarData_url_folder="D:\\program_0519rain\\data\\CPEFS下载链接"
#html文件中下载链接在第几列，是第几列就是几，后续自定义函数代码中已包含减1
url_rowNumber=4
#提取出来的下载链接txt文件名
url_filename='NAFP_CPEFS_CAMS_BIN.txt'
#下载链接那列的表头所含字符串，用来去除表头只保留下载链接
thead_string='路径'
#数据下载后储存文件夹
rada_data_download_folder='D:\\program_0519rain\\data\\CPEFS数据'
#指定要调用的chromedriver的存放路径，一般下载下来后放在与浏览器chrome.exe同一路径
chromedriver_path='C:\\Users\\Administrator\\AppData\\Local\\google\\Chrome\\Application\\chromedriver.exe'
#设定下载时间间隔，每个下载间隔sleep_time_1，每6个下载间隔sleep_time_2，下载提交完后间隔sleep_time_3再退出浏览器
sleep_time_1=10
sleep_time_2=120
sleep_time_3=300

url_file_path=write_url_list_file(radarData_url_folder,url_rowNumber,thead_string)
print('输出的下载链接txt文件: '+url_file_path)
download_data_num=download_by_chrome_and_url_txt(rada_data_download_folder,chromedriver_path,url_file_path,sleep_time_1,sleep_time_2,sleep_time_3)
print('共向浏览器提交%d个下载申请'%download_data_num)

# 在anaconda prompt中使用以下命令行代码运行此程序
# python D:\program_0519rain\download_by_choromedriver_cpefs.py



