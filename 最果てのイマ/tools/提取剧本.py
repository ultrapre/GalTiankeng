import os

srcdir = "M:/PSP/run/text-TST"
'''
需要重新设计的文件
//a_cmn_00.BIP.txt
CHAPTER00.BIP.txt
CHAPTER01.BIP.txt
CHAPTER02.BIP.txt
CHAPTER03.BIP.txt
CHAPTER04.BIP.txt
CHAPTER05.BIP.txt
CHAPTER06.BIP.txt
CHAPTER07.BIP.txt
CHAPTER08.BIP.txt
SHORTCUT.BIP.txt
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

for src in dirlist(srcdir,[]):
# for src in ["M:/PSP/run/text-TST/a_cmn_00.bip.txt"]:
    outfile = os.path.split(src)[0] + "-Out/" + os.path.split(src)[1]
    print(src)
    totalsize = os.path.getsize(src)
    fp = open(outfile, "wb") #, encoding="utf-8")
    size = 0
    flag = 0
    with open(src, "rb") as f:
        while size < totalsize:
            a = f.read(8)
            size += 8
            if a == b'\xff\xff\xff\xff\xff\xff\xff\xff':
                a = f.read(8)
                size += 8
                if a == b'\xff\xff\xff\xff\xff\xff\xff\xff':
                    flag = 1
            if flag == 1:
                a = f.read(totalsize - size)
                size = totalsize
                a = a.replace(b"\x00", b"").replace(b"\x25\x4B\x25\x50", b"\x0D\x0A").replace(b"\x25\x4E", b"\x0D\x0A")
                fp.write(a)
    fp.close()


