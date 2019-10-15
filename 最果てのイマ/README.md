---
title: 如何破解最果てのイマ
date: 2019-10-15 19:09:14
tags:
---

# 如何破解最果てのイマ

how to extract / depack / unpack Saihate no Ima?

参考到这条残念的[不能解包的记录](<https://blog.ztjal.info/acg/acg-data/galgame-can-not-unpack-record> )

我燃起了无论如何也要找到解包最果的办法。作为伪田中厨子，怎么能不去了解一下这个仅次于樱之诗的“汉化天坑”&&“日语白学”巨作呢？

为什么我知道已经有解包前例了？第一，Famille曾经接手说明肯定能解。

其次在VN STATs 中有这条记录。



| Game title     | Developer | Game engine | [VNDB                                                        | Unique kanji | Line count | MB size | Writer       |
| -------------- | --------- | ----------- | ------------------------------------------------------------ | ------------ | ---------- | ------- | ------------ |
| Saihate no Ima | Xuse      |             | [vndb](https://web.archive.org/web/20170708071728/http://vndb.org/v1278) | 2578         |            | 1.84    | Tanaka Romeo |

可以见到Engine这行是空的，很恶心。



废话不多说，谈谈解包方法。

我的目标是拿到文本而不是完全汉化封包，所以我绕过PC版引擎的奇特，使用PSP版本`最果てのイマ PORTABLE`解决。

脚本在`"Q:\PSP_GAME\USRDIR\mac.afs"`中，使用crass可以解包出如下文件：

```
a_boot.BIP
a_cmn_00.BIP
a_epl_00.BIP
a_epl_01.BIP
a_epl_02.BIP
a_epl_03.BIP
a_prl_01.BIP
a_prl_02.BIP
...
```

你也可以使用AFSExplorer或者exafs.exe或者<https://github.com/dreambottle/R11-psp-english/blob/master/unpack-afs.sh> 

针对*.bip，可以使用以下代码解开，这个地址是我使用谷歌`PSP "afs" "t2p"`才搜索到的：

<https://github.com/dreambottle/R11-psp-english/blob/master/src/decompressbip.c> 

另外，还有一个类似的PSP项目也可以研读：<https://github.com/uyjulian/e17p#formats-and-parsers-remember11> 

我使用的是Ubuntu14.04，`gcc -o exbip decompressbip.c lzss.c`

生成exbip

然后新建一个`run.sh`:

```shell
for line in `cat file.txt`
do
echo $line
exbip bip/$line $line.txt
done
```

然后新建一个file.txt，写入所有的bip文件:

```
a_boot.BIP
a_cmn_00.BIP
a_epl_00.BIP
a_epl_01.BIP
a_epl_02.BIP
a_epl_03.BIP
a_prl_01.BIP
a_prl_02.BIP
...
```

将所有的*.bip文件放入bip文件夹中，然后修改执行权限，执行run.sh

得到的*.txt文件，其中a_wr1_01.BIP.txt显示如下：

```d
Offset      0  1  2  3  4  5  6  7   8  9  A  B  C  D  E  F

000022A0   01 00 00 00 FF FF FF 23  FF FF FF FF 01 00 00 00       #    
000022B0   FF 7F 00 00 FF 7F 00 00  00 00 00 00 00 00 00 18                 
000022C0   00 00 00 00 1E 00 00 00  00 00 00 00 00 00 00 00                   
000022D0   6E 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   n               
000022E0   FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF   
000022F0   82 BB 82 B5 82 C4 94 45  82 CD 81 41 91 90 8C B4   そして忍は A?原
00002300   82 C9 98 C8 82 F1 82 C5  82 A2 82 BD 81 42 25 4B   に佇んでいた B%K
00002310   25 50 00 89 F9 82 A9 82  B5 82 A2 8F EA 8F 8A 82   %P 懐かしい ?鰍
00002320   BE 81 42 25 4E 82 A2 82  AD 82 C2 82 A9 82 CC 8E   ?B%Nいくつかの?
00002330   76 82 A2 8F 6F 82 AA 82  A0 82 E9 81 42 25 4B 25   vい oがある B%K%
00002340   50 00 82 BD 82 C6 82 A6  82 CE 95 97 82 F0 8E E8   P たとえば風を手
00002350   8C 4A 82 E9 8F 70 82 F0  8A 6F 82 A6 82 BD 82 CC   繰る pを覚えたの

```

可以看到，几乎所有txt都是这样子，前面为索引，后面为shift-jis表示的日文明文，由于我只需要文本，暂时不考虑封包，，而且由于我程序渣，所以直接抽取文本，方法是循环读取8字节，如果结果是`b'\xff\xff\xff\xff\xff\xff\xff\xff'`，而且下面的8个也是`b'\xff\xff\xff\xff\xff\xff\xff\xff'`，然后就标记写入日文，并且去掉其中的`'\x00'`，而且把`b"\x25\x4B\x25\x50"`也就是`%K%P`以及`b"\x25\x4E"`也就是`%N`替换为`b"\x0D\x0A"`也就是`\n`。

批量编程的方法如下：

```python
srcdir = "M:/PSP/run/text-TST/1.bip.txt"
outfile = os.path.split(src)[0] + "-Out/" + os.path.split(src)[1]
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
```

剩余的如下文本单独处理：

```
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
```



最终得到如下文本：

```
そして忍は、草原に佇んでいた。
懐かしい場所だ。
いくつかの思い出がある。
……
```

翻译即可完成。

---

# 走过的弯路（其实是我菜）

**针对PC版：**

PC版有以下文件类型：

```
*.bin *.004 *.arc *.cd *.xsa
```

用我收集的解包库用everything搜索一遍上面的后缀名，然后试验

例如chinesize中的Xuse，由于找不到`strfile`是什么鬼模块只好放弃

```
chinesize
Fragment-master
FuckGalEngine
gal_tools
galgame解包
GALgame解压工具大全
```

在我剪藏的网页文件夹中搜索一遍上面的后缀名，然后试验

crass用Xuse参数试了所有一遍（可以解出很小一部分）；

asmodean tools找出所有可以解*.arc的，然后对arc全试一遍。

搜索“saihate no ima”+“unpack”/“extract”等等变着方法搜索。

得知厂商为Xuse和Cyberfront，搜索其解包方法。

用https://blog.ztjal.info/里面包含Xuse的方法全试一遍。

尝试通过VN stats的[https://vnscripts.neocities.org](https://vnscripts.neocities.org/) 或者http://wiki.wareya.moe/Stats找到别人拿到的文本

联系曾经接手的Famille组，然后联系到Azure前辈，但是由于其太忙没时间翻记录。

**针对PSP版：**

根据网上随处可见的教程尝试使用WQSG解决bip文件或者afs文件。

