#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/3/28 10:08

"""
用法:"python diffall.py dir1 dir2"
递归的目录树比较:报告仅在dir1而非dir2中存在的特有文件,报告dir1和dir2同名但内容不同的文件,
报告dir1和dir2中同名但不同类型的情况,并对dir1和dir2下所有同名子目录及其目录进行相同操作.
输出的末尾打印差异的总结,不过其中的细节请在重定向的输出中搜索"DIFF"和"unique"字符串.
特性:将大文件的读取限制在每次1MB,捕获文件和目录同名的情况,通过在这个版本里传入结果以
避免在dirdiff.comparedirs()中再次调用os.listdir()
"""
import os,dirdiff

blocksize = 1024 * 1024    #每次最多至多读取1MB

def intersect(seq1,seq2):
    """
    返回seq1和seq2的所有共有项
    也可以使用set(seq1) & set(seq2),不过集合内的顺序是随机的,故而
    可能丢失任何依赖于平台的目录顺序
    """
    return [item for item in seq1 if item in seq2]

def comparetrees(dir1,dir2,diffs,verbose=False):
    """
    比较两个目录树中的所有子目录和文件,使用二进制文件来阻止Unicode解码和换行符转换,因为目录树可能含有二进制
    文件和文本文件;可能需要listdir的bytes参数来处理某些平台上不可解码的文件名
    """
    #比较文件列表
    print('-' * 20)
    names1 = os.listdir(dir1)
    names2 = os.listdir(dir2)
    if not dirdiff.comparedirs(dir1,dir2,names1,names2):
        diffs.append('unique files at %s - %s' % (dir1,dir2))
    print('Comparing contents')
    common = intersect(names1,names2)
    missed = common[:]

    #比较共有文件的内容
    for name in common:
        path1 = os.path.join(dir1,name)
        path2 = os.path.join(dir2,name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            file1 = open(path1,'rb')
            file2 = open(path2,'rb')
            while True:
                bytes1 = file1.read(blocksize)
                bytes2 = file2.read(blocksize)
                if (not bytes1) and (not bytes2):
                    if verbose:print(name,'matches')
                    break
                if bytes1 != bytes2:
                    diffs.append('file differ at %s - %s' % (path1,path2))
                    print(name,'DIFFERS')
                    break

    #递归比较共有目录
    for name in common:
        path1 = os.path.join(dir1,name)
        path2 = os.path.join(dir2,name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparetrees(path1,path2,diffs,verbose)

    #同名但一个是文件,另一个是目录
    for name in missed:
        diffs.append('file missed at %s - %s:%s' % (dir1,dir2,name))
        print(name,'DIFFERS')

if __name__ == '__main__':
    dir1,dir2 = dirdiff.getargs()
    diffs = []
    comparetrees(dir1,dir2,diffs,True)
    print('=' * 40)
    if not diffs:
        print('No diffs found.')
    else:
        print('Diff found:',len(diffs))
        for diff in diffs:print('-',diff)