#!/usr/bin/python
# -*- coding: utf-8 -*-
from textSolve.langconv import *
import os
import chardet
import codecs
'''
脚本剧本拆分合并代码适用范围：
	脚本融合在一起的剧本如神树之馆
	检查方法：首个字符是英文字符的是脚本，否则为剧本
	
'''
def is_scr(char):
    if char >= '\u0000' and char <= '\u007F':
        return True
    else:
        return False

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

# for files in dirlist("M:/神樹の館/SNRTest",[]):
# if __name__ == "__main__":
for files in dirlist("M:/神樹の館/SNRTest-utf-8", []):
    src = files
    dst1 = os.path.split(src)[0] + "-CatScr/" + os.path.split(src)[1]
    dst2 = os.path.split(src)[0] + "-CatWrd/" + os.path.split(src)[1]
    if os.path.exists(os.path.split(dst1)[0]) == 0:
        os.makedirs(os.path.split(dst1)[0])
    if os.path.exists(os.path.split(dst2)[0]) == 0:
        os.makedirs(os.path.split(dst2)[0])
    fp = open(dst1,"w",encoding="utf-8")
    fq = open(dst2,"w",encoding="utf-8")
    with codecs.open(src, "r", "utf-8") as f:
        for line in f.readlines():
            if is_scr(line[0]):
                fp.write(line.replace("\r\n","\n"))
                fq.write("\n")
            else:
                fq.write(line.replace("\r\n","\n"))
                fp.write("\n")
    f.close()
    fp.close()
    fq.close()

