#!/usr/bin/python
#-*- coding:utf-8 -*-
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

'''
脚本剧本拆分合并代码适用范围：
	适用于如每一句前面都有"　"或者句尾都有"$"或者游戏人物名前固定有"#"等固定剧本格式如俺翼
'''

def translate(valueText, target):
    # 自定义翻译方法

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




def TransAll(scrDir):
	# 翻译卡住可以检查已经翻译的，不需要重新翻译
    expDir = scrDir.replace("utf-8", "utf-8-CatScr-chs-CatMrg")
    if os.path.exists(expDir) == 0:
        os.makedirs(expDir)
    exceptlist = dirlist(expDir, [])

    for src in dirlist(scrDir, []):
        if src.replace("utf-8", "utf-8-CatScr-chs-CatMrg") in exceptlist:
            continue
        print(src)
		
		# 按格式拆分
        fp = open(src, "r", encoding="utf-8")

        dst1 = os.path.split(src)[0] + "-CatPgm/" + os.path.split(src)[1]
        dst2 = os.path.split(src)[0] + "-CatScr/" + os.path.split(src)[1]

        if os.path.exists(os.path.split(dst1)[0]) == 0:
            os.makedirs(os.path.split(dst1)[0])
        if os.path.exists(os.path.split(dst2)[0]) == 0:
            os.makedirs(os.path.split(dst2)[0])
        fx = open(dst1, "w", encoding="utf-8")
        fy = open(dst2, "w", encoding="utf-8")
        for line in fp.readlines():
            if line[0] == "#":
                fx.write(line.split("&", 1)[0] + "\n")
                fy.write(line.split("&", 1)[1][:-2] + "\n")
            else:
                fx.write("\n")
                fy.write(line[:-2] + "\n")
        fp.close()
        fx.close()
        fy.close()
        ###########################
		# 翻译部分

        dst = os.path.split(dst2)[0] + "-chs/" + os.path.split(dst2)[1]
        if os.path.exists(os.path.split(dst)[0]) == 0:
            os.makedirs(os.path.split(dst)[0])
        lines = open(dst2, "r", encoding="utf-8").readlines()
        with open(dst, "w", encoding="utf-8") as fp:
            text = ""
            tmptext = ""
            i = 0
            # j = 1
            print(len(lines))

            linenum = 20
            lineflag = 0
            totalline = len(lines)
            maxtext = 900

            floattext = ""
            floatflag = 0
            lasptime = 1
            while i < len(lines):
                if len(tmptext + lines[i]) > maxtext:
                    floattext = lines[i]
                    floatflag = 1
                    tmptext = ""
                    text = text
                    time.sleep(lasptime)
                    fin = translate(text, "zh")
                    fp.write(fin)
                    print(i)
                else:
                    tmptext = tmptext + lines[i]
                    text = tmptext
                    floattext = text
                    i = i + 1
                    floatflag = 1
            if floatflag == 1:
                text = floattext
                time.sleep(lasptime)
                fin = translate(text, "zh")
                fp.write(fin)
        fp.close()

        ###########################
		# 合并格式
        try:
            merge = os.path.split(dst)[0] + "-CatMrg/" + os.path.split(src)[1]
            if os.path.exists(os.path.split(merge)[0]) == 0:
                os.makedirs(os.path.split(merge)[0])
            fz = open(merge, "w", encoding="utf-8")
            fx = open(dst1, "r", encoding="utf-8")
            fy = open(dst, "r", encoding="utf-8")
            lines = fy.readlines()
            i = 0
            for line in fx.readlines():
                if line != "\n":
                    fz.write(line[:-1] + "&" + lines[i][:-1] + "$" + "\n")
                else:
                    fz.write("　" + lines[i].replace("\r\n", "").replace("\n", "") + "$" + "\n")
                i += 1
            fx.close()
            fy.close()
            fz.close()
        except:
            print(src + " make merge error")


if __name__ == "__main__":
    TransAll("M:/oretachinitsubasahanai/scripts-utf-8")
