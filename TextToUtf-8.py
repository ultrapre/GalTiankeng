import os
import chardet
import codecs
'''
批量转换文件夹内txt为utf-8
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

def EncodesAll(FilesDir):
    for src in dirlist(FilesDir, []):
        dst = os.path.split(src)[0] + "-utf-8/" + os.path.split(src)[1]
        if os.path.exists(os.path.split(dst)[0]) == 0:
            os.makedirs(os.path.split(dst)[0])
        f = open(src, "rb")
        coding = chardet.detect(f.read())["encoding"]
        print(coding)
        f.close()
        if coding != "utf-8":
            with codecs.open(src, "r", coding) as f:
                try:
                    with codecs.open(dst, "w", encoding="utf-8") as fp:
                        fp.write(f.read())
                    try:
                        print(src + "  " + coding + " to utf-8  converted!")
                    except Exception:
                        print("print error")
                except Exception:
                    print(src + "  " + coding + "  read error")

if __name__ == "__main__":
    EncodesAll("M:/oretachinitsubasahanai/scripts-utf-8")