#!/usr/bin/python
# -*- coding: utf-8 -*-
from textSolve.langconv import *
import os
import chardet
import codecs
'''
脚本剧本拆分合并代码适用范围：
	脚本融合在一起的剧本如神树之馆
	
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
if __name__ == "__main__":
    # src = "M:/神樹の館/SNRTest-utf-8/オープニング.txt"
    for src in dirlist("M:/神樹の館/SNRTest-utf-8",[]):
        dst1 = os.path.split(src)[0] + "-CatScr/" + os.path.split(src)[1]
        dst2 = os.path.split(src)[0] + "-CatWrd-total-merge/" + os.path.split(src)[1]
        findst = os.path.split(src)[0] + "-CatOut/" + os.path.split(src)[1]
        print("scr_pgrm "+dst1)
        print("scr_src  "+dst2)
        print("scr_sum  "+findst)
        if os.path.exists(os.path.split(dst1)[0]) == 0:
            os.makedirs(os.path.split(dst1)[0])
        if os.path.exists(os.path.split(dst2)[0]) == 0:
            os.makedirs(os.path.split(dst2)[0])
        if os.path.exists(os.path.split(findst)[0]) == 0:
            os.makedirs(os.path.split(findst)[0])
        fq = open(dst1, "r", encoding="utf-8")
        fp = open(dst2, "r", encoding="utf-8")
        i = 0
        lines = fq.readlines()
        with codecs.open(findst, "w", "utf-8") as f:
            for line in fp.readlines():

                if (line == "\n"):
                    f.write(lines[i].replace("\n", "\r\n"))
                else:
                    f.write(line.replace("\n", "\r\n"))
                # f.write(lines[i].replace("\r\n", ""))
                i = i + 1
        f.close()
        fp.close()
        fq.close()

