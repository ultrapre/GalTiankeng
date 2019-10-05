import sys
import os
import json  # 导入json模块
import urllib  # 导入urllib模块
from urllib import request, parse
from urllib.error import URLError, HTTPError
import _md5
import time
import datetime
from lxml import etree
import os
import chardet
import codecs
'''
脚本剧本拆分合并代码适用范围：
	通用于有多行CRLF而被百度翻译返回成一行CRLF的
'''

def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist: #广义
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)

        elif filepath.endswith("txt"):
            filepath = filepath.replace("\\","/")
            allfile.append(filepath)
    return allfile



if __name__ == '__main__':

	# 通用于有多行CRLF而被百度翻译返回成一行CRLF的
	
    # 先檢查是utf-8格式
    for files in dirlist("M:/Liar/BKOUT-utf-8/tst",[]):
    # for files in ["M:/Liar/Forest/scripts/NewSc/2100.txt"]:
        print(files)
        
		
		# 检查多行换行建立索引
		src = files
        inx = os.path.split(src)[0] + "-inx/" + os.path.split(src)[1].replace("txt","inx")
        dst = os.path.split(src)[0] + "-inx/" + os.path.split(src)[1]
        if os.path.exists(os.path.split(inx)[0]) == 0:
            os.makedirs(os.path.split(inx)[0])
        if os.path.exists(os.path.split(dst)[0]) == 0:
            os.makedirs(os.path.split(dst)[0])

        dic = {}
        lines = open(src, "r", encoding="utf-8").readlines()
        fp = open(dst, "w", encoding="utf-8")
        fi = open(inx, "w", encoding="utf-8")
        i = 0
        j = 0
        while i < len(lines):
            if lines[i] != "\n":
                dic[str(j+1)] = i
                fp.write(lines[i])
                j = j + 1
            else:
                dic[str(j + 1)] = "crlf"
                j = j + 1
            i = i +1

        js = json.dumps(dic)
        fi.write(js)
        fi.close()
        fp.close()
		
		
		###########################
		'''
		百度翻译部分，自行插入TransGalDirText.py
		'''
		
		
		###########################
		
		# 合并前面多行换行建立的索引和翻译后的剧本部分
		
		dstchs = os.path.split(dst)[0] + "-merge/" + os.path.split(dst)[1]
        if os.path.exists(os.path.split(dstchs)[0]) == 0:
            os.makedirs(os.path.split(dstchs)[0])
        ff = open(dst, "r", encoding="utf-8")
        fi = open(inx, "r", encoding="utf-8")
        fp = open(dstchs, "w", encoding="utf-8")

        js = fi.read()
        dic = json.loads(js)
        for i in dic:
            if dic[i] == "crlf":
                fp.write("\n")
            else:
                fp.write(ff.readline())
		fi.close()
        fp.close()
		ff.close()