#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/3/29 10:00

"""
返回某个目录及其子目录下所有匹配某个文件名模式的文件:

find()是一个生成器,利用os.walk()生成产生匹配的文件名,可使用findlist()强制生成结果列表
"""
import fnmatch,os

def find(pattern,startdir=os.curdir):
    for (thisDir,subsHere,filesHere) in os.walk(startdir):
        for name in subsHere + filesHere:
            if fnmatch.fnmatch(name,pattern):
                fullpath = os.path.join(thisDir,name)
                yield fullpath

def findlist(pattern,startdir=os.curdir,dosort=False):
    matches = list(find(pattern,startdir))
    if dosort: matches.sort()
    return matches

if __name__ == '__main__':
    import sys
    namepattern,startdir = sys.argv[1],sys.argv[2]
    for name in find(namepattern,startdir):print(name)