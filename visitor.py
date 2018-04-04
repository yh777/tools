#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/3/29 13:57
"""
测试:"python visitor.py testmask dir [string]".使用类和子类封装os.walk调用手法某些细节,以便
进行遍历和搜索;testmask是一个整数比特掩码,每个可用的自我测试占1位;
框架中一般应当使用__X作为伪局部名称,不过为了在子类和客户端的使用,这里的所有名称都将导出;
可重新定义reset以支持需要更新子类的相互独立的遍历操作
"""

import sys, os


class FileVisitor:
    """
    访问startDir(默认为'.')下所有非目录文件;可通过重载visit*方法定制文件/目录处理器;情意参数/属性为
    可选的子类特异的状态;追踪开头:0代表关闭,1代表显示目录,2代表显示目录及文件
    """

    def __init__(self, context=None, trace=2):
        self.fcount = 0
        self.dcount = 0
        self.context = context
        self.trace = trace

    def run(self, startDir=os.curdir, reset=True):
        if reset: self.reset()
        for (thisDir, dirsHere, filesHere) in os.walk(startDir):
            self.visitdir(thisDir)
            for fname in filesHere:  # 对非目录文件进行迭代
                fpath = os.path.join(thisDir, fname)  # fname不带路径
                self.visitfile(fpath)

    def reset(self):  # 为了重复使用遍历器
        self.fcount = self.dcount = 0  # 为了相互独立的遍历操作

    def visitdir(self, dirpath):
        self.dcount += 1  # 待重写或扩展
        if self.trace > 0: print(dirpath, '...')

    def visitfile(self, filepath):
        self.fcount += 1  # 待重写或扩展
        if self.trace > 1: print(self.fcount, '=>', filepath)


class SearchVisitor(FileVisitor):
    """
    在startDir及其子目录下的文件中搜索字段;子类:根据需要重新定义visitmatch,扩展列表和候选;
    子类可以使用testexts来指定进行搜索的文件类型(还可以重定义候选以对文本内容使用mimetypes)
    """
    #skipexts = []
    testexts = ['.txt', '.py', '.pyw', '.html', '.c', '.h']  # 搜索带有这些扩展名的文件

    skipexts = ['.gif','.jpg','.pyc','.o','.a','.exe']   #或者跳过带有这些扩展名的文件

    def __init__(self, searchkey, trace=2):
        FileVisitor.__init__(self, searchkey, trace)
        self.scount = 0

    def reset(self):  # 进行相互独立的时
        self.scount = 0

    def candidate(self, fname):  # 重新定义mimetypes
        ext = os.path.splitext(fname)[1]
        if self.testexts:
            return ext in self.testexts  # 在测试列表中时
        else:  # 或者不在跳过列表中时
            return ext not in self.skipexts

    def visitfile(self, fname):
        FileVisitor.visitfile(self, fname)
        if not self.candidate(fname):
            if self.trace > 0: print('Skipping', fname)
        else:
            text = open(fname).read()  # 如果不能解码则使用'rb'模式
            if self.context in text:  # 也可以用text.find() != -1
                self.visitmatch(fname, text)
                self.scount += 1

    def visitmatch(self, fname, text):  # 处理一个匹配文件
        print('%s has %s' % (fname, self.context))  # 在低一级的水平重写


if __name__ == '__main__':
    dolist = 1
    dosearch = 2  # 3进行列出和搜索
    donext = 4  # 添加了下一个测试时


    def selftest(testmask):
        if testmask & dolist:
            visitor = FileVisitor(trace=2)
            visitor.run(sys.argv[2])
            print('Visited %d files and %d dirs' % (visitor.fcount, visitor.dcount))

        if testmask & dosearch:
            visitor = SearchVisitor(sys.argv[3], trace=0)
            visitor.run(sys.argv[2])
            print('Fount in %d files,visited %d' % (visitor.scount, visitor.fcount))


    selftest(int(sys.argv[1]))  # 例如,3 = dolist | dosearch