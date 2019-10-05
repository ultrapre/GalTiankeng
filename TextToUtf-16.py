import os
import chardet
import codecs
'''
批量转换文件夹内txt为utf-16
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



if __name__ == "__main__":
    ucode16 = "utf-16"
    for src in dirlist("M:/Liar/BKOUT-utf-8/Trans-chs", []):
        dst = os.path.split(src)[0] + "-"+ucode16+"/" + os.path.split(src)[1]
        if os.path.exists(os.path.split(dst)[0]) == 0:
            os.makedirs(os.path.split(dst)[0])
        f = open(src, "rb")
        coding = chardet.detect(f.read())["encoding"]
        print(coding)
        f.close()
        if coding != ucode16:
            with codecs.open(src, "r", coding) as f:
                try:
                    with codecs.open(dst, "w", encoding=ucode16) as fp:
                        fp.write(f.read())
                    try:
                        print(src + "  " + coding + " to utf-16  converted!")
                    except Exception:
                        print("print error")
                except Exception:
                    print(src + "  " + coding + "  read error")