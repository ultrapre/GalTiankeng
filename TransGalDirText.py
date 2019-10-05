#!/usr/bin/python
# -*- coding:utf-8 -*-
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
Galgame机翻核心

1.配置json的百度api

2.修改txt的输入目录，确保里面全是utf-8格式txt，而且每一行字长不要超过分割字长'maxtext = 800'

3.输出目录 = 输入目录 + "-chs"

4.运行结果错误，则调整发送分割字长'maxtext = 800'小一点，或者请求间隔时间'time.sleep(1)'大一点。

5.作为gal文本翻译的调整：可见于其他的脚本
	规则字符、脚本的拆分合并处理：
		通用于有多行CRLF而被百度翻译返回成一行CRLF的
		适用于如每一句前面都有"　"或者句尾都有"$"或者游戏人物名前固定有"#"等固定剧本格式；
		和脚本融合在一起的剧本；

'''
KEY_PATH = "../../keys/baidu_translation.json"
file = open(KEY_PATH, 'r')
js = file.read()
dic = json.loads(js)
myappId = dic["appId"]
mykey = dic["key"]

def translate(valueText, target):
    appId = myappId
    key = mykey
    salt = datetime.datetime.now().strftime('%m%d%H%M%S')
    quoteStr = parse.quote(valueText)
    md5 = _md5.md5()
    md5.update((appId + valueText + salt + key).encode())
    sign = md5.hexdigest()
    url = 'http://fanyi-api.baidu.com/api/trans/vip/translate?q=' + quoteStr + \
          '&from=auto&to=' + target + '&appid=' + \
          appId + '&salt=' + salt + '&sign=' + sign
    try:
        resultPage = request.urlopen(url)  # 调用百度翻译API进行批量翻译
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        return valueText
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return valueText
    except Exception as e:
        print('translate error.')
        print(e)
        return valueText

    # 取得翻译的结果，翻译的结果是json格式
    resultJason = resultPage.read().decode('utf-8')
    # print(resultJason)
    js = None
    try:
        # 将json格式的结果转换成Python的字典结构
        js = json.loads(resultJason)
        # print(js)
    except Exception as e:
        print('loads Json error.')
        print(e)
        return valueText

    key = u"trans_result"

    if key in js:
        dst = ""
        for line in js["trans_result"]:
            dst = dst + line["dst"] + "\n"  # 取得翻译后的文本结果
            # print(dst)
        return dst
    else:
        return valueText  # 如果翻译出错，则输出原来的文本

def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:  # 广义
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)

        elif filepath.endswith("txt"):
            filepath = filepath.replace("\\", "/")
            allfile.append(filepath)
    return allfile

if __name__ == '__main__':
    # 先檢查是utf8格式
    for files in dirlist("M:/tst", []):  # 默认只遍历txt文件
        # for files in ["M:/Liar/Forest/scripts/NewSc/2100.txt"]: #用于单文件翻译
        src = files
        dst = os.path.split(src)[0] + "-chs/" + os.path.split(src)[1]
        print(src)
        print(dst)
        if os.path.exists(os.path.split(dst)[0]) == 0:
            os.makedirs(os.path.split(dst)[0])
        lines = open(src, "r", encoding="utf-8").readlines()
        with open(dst, "w", encoding="utf-8") as fp:
            text = ""
            tmptext = ""
            i = 0
            print(len(lines))
            linenum = 20
            lineflag = 0
            totalline = len(lines)
            maxtext = 800
            floattext = ""
            floatflag = 0
            while i < len(lines):
                if len(tmptext + lines[i]) > maxtext:
                    floattext = lines[i]
                    floatflag = 1
                    tmptext = ""
                    text = text
                    time.sleep(1)
                    fin = translate(text, "zh")
                    # print(text)
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
                time.sleep(1)
                fin = translate(text, "zh")
                # print(text)
                fp.write(fin)
        fp.close()

        #####################


