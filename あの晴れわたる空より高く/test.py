# -*- coding: utf-8 -*-
import MjoParser
import bytefile
import os

def dirlist(path, allfile, ext):
    filelist = os.listdir(path)

    for filename in filelist: #广义
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile, ext)

        elif filepath.endswith(ext):
            filepath = filepath.replace("\\","/")
            allfile.append(filepath)
    return allfile


# fname='start'
flist = dirlist("O:/git/Py3_mytool/GalgameSolve/parser/uncry",[],"mjo")

for fname in flist:
    fs = open(fname, 'rb')
    stm = bytefile.ByteFile(fs.read())
    mp = MjoParser.MjoParser(stm)
    txt = mp.Parse()
    fs = open(fname + '.txt', 'wb')
    fs.write(txt.encode('u16'))
    fs.close()
    fs = open(fname + '.dec', 'wb')
    fs.write(mp.vmcode[0:])
    fs.close()
