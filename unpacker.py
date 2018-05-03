#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 解包由packer.py创建的文件(简单文本文件存档)

import sys
from packer import marker             # 使用共同的分隔符
mlen = len(marker)                    # 标记之后的文件名

def unpack(ifile, prefix='new-'):
    for line in open(ifile):                # 所有输入的行
        if line[:mlen] != marker:
            output.write(line)              # 写出各行的内容
        else:
            name = prefix + line[mlen:-1]   # 创建新的文件
            print('creating:', name)
            output = open(name, 'w')

if __name__ == '__main__': unpack(sys.argv[1])
