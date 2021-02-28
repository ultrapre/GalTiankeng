from slpp import slpp as lua

from silas import *

def solveArtemis(src):
    cnt = open(src, encoding="utf-8").read()
    c1 = cnt.split("\ntext=")[0]
    c2 = cnt.split("\ntext=")[1].split("\nlabel=")[0]
    c3 = cnt.split("\ntext=")[1].split("\nlabel=")[1]

    # cnt=cnt.replace("\"","'")
    data = lua.decode(c2)
    # print(data)
    # print(type(data))
    cnt = lua.encode(data)
    cnt = cnt.replace('[0] = "vo"', '"vo"').replace('["', '').replace('"]', '')
    s = c1 + "\ntext=" + cnt + ",\nlabel=" + c3

    lines = []
    for it in data:
        if "ja" in data[it]:
            if type(data[it]["ja"][0][0]) is str:
                lines.append(data[it]["ja"][0][0])
    # print(lines)
    writealllines(lines,src.replace(".ast",".txt"))
    # open(src,"w",encoding="utf-8").write(s)


for src in dirlist("G:/gal/終の空/script",".ast"):
    solveArtemis(src)
