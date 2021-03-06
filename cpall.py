#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
用法:"python cpall.py dirFrom dirTo"
递归地复制目录树.和Unix命令cp -r dirFrom/* dirTo效果类似,其中假定dirFrom和dirTo都是目录
为了避开Windows下拖放复制中的致使错误消息而编写(复制操作在遇到第一个不符合要求的文件时立即终止),并且
可以用Python对更特殊的复制操作进行定制编程
"""
import os,sys,time
maxfileload = 1000000
blksize = 1024 * 500

backupbasedir = r'/backup/web_update_bak' # 备份文件根目录

def copyfile(pathFrom,pathTo,maxfileload=maxfileload):
    """
    将单个文件逐字节从pathFrom复制到pathTo;使用二进制文件模式阻止Unicode解码及换行符换行
    """
    if os.path.getsize(pathFrom) <= maxfileload:
        bytesFrom = open(pathFrom,'rb').read()    #对于所有小文件均一次性读入
        open(pathTo,'wb').write(bytesFrom)
    else:
        fileFrom = open(pathFrom,'rb')                #逐块读取大文件
        fileTo = open(pathTo,'wb')                    #读写都需要b模式
        while True:
            bytesFrom = fileFrom.read(blksize)        #读取一个小块,最后一块可能稍小
            if not bytesFrom: break                   #最后一个小块之后为空字符
            fileTo.write(bytesFrom)

def copytree(dirFrom,dirTo,verbose=2):
    """
    将dirFrom下的内容复制到dirTo,返回(文件,目录)数目形式的元组
    为避免在某些平台上目录名不可解码,可能需要为其使用字节;
    在Unix下可能需要更多文件类型检查,跳过链接,fifo之类
    """
    fcount = dcount = 0
    for filename in os.listdir(dirFrom):             #针对这里的文件/目录
        pathFrom = os.path.join(dirFrom,filename)
        pathTo = os.path.join(dirTo,filename)        #两个路径都补全
        if not os.path.isdir(pathFrom):              #复制简单文件
            try:
                if verbose > 1: print('copying',pathFrom,'to',pathTo)
                copyfile(pathFrom,pathTo)
                fcount += 1
            except:
                print('Error copying',pathFrom,'to',pathTo,'--skipped')
                print(sys.exc_info()[0],sys.exc_info()[1])
        else:
            if verbose:print('copying dir',pathFrom,'to',pathTo)
            try:
                if not os.path.exists(pathTo):
                    os.mkdir(pathTo)                 #创建新的子目录
                below = copytree(pathFrom,pathTo)    #递归进入子目录
                fcount += below[0]                   #加上子目录的文件数
                dcount += below[1]
                dcount += 1
            except:
                print('Error creating',pathTo,'--skipped')
                print(sys.exc_info()[0],sys.exc_info()[1])
    return (fcount,dcount)

def cpsamefile(dir1,dir2):
    """
    备份被覆盖的文件
    """
    # 在目录末尾添加目录分隔符
    if not dir1.endswith(os.sep):
        dir1 = dir1 + os.sep
    if not dir2.endswith(os.sep):
       dir2 = dir2 + os.sep

    if not os.path.exists(backupbasedir):
       os.makedirs(backupbasedir)
    backupdir = backupbasedir + r'/' + time.strftime("%Y%m%d%H%M%S",time.localtime())
    backupdir = os.path.normpath(backupdir)
    backupdir = os.path.normcase(backupdir)
    if not os.path.exists(backupdir):
        os.mkdir(backupdir)
    for item in os.walk(dir1):
        for file0 in item[2]:
            file1 = os.path.join(item[0],file0)
            file2 = os.path.join(dir2,file1.replace(dir1,''))
            file2 = os.path.normpath(file2)
            file2 = os.path.normcase(file2)
            file3 = os.path.join(backupdir,file2.replace(dir2,''))
            file3 = os.path.normpath(file3)
            file3 = os.path.normcase(file3)
            if os.path.exists(file2):
                if not os.path.exists(os.path.split(file3)[0]):
                    os.makedirs(os.path.split(file3)[0])
                copyfile(file2,file3)

def listfiles(dir1,dir2):
    """
    显示要操作的文件
    """
    files = []    # 文件列表
    for (thisDir,subsHere,filesHere) in os.walk(dir1):
        for file in filesHere:
            files.append(os.path.join(thisDir,file))

    return files

def getargs():
    """
    获取并验证文件目录名参数,碰到错误时默认返回None
    """
    try:
        dirFrom,dirTo = sys.argv[1:]
    except:
        print('Usage error: cpall.py dirFrom dirTo')
    else:
        if not os.path.isdir(dirFrom):
            print('Error: dirFrom is not a directory')
        elif not os.path.exists(dirTo):
            os.mkdir(dirTo)
            print('Note: dirTo was created')
            return (dirFrom,dirTo)
        else:
            print('Warning: dirTo already exists')
            if hasattr(os.path,'samefile'):
                same = os.path.samefile(dirFrom,dirTo)
            else:
                same = os.path.abspath(dirFrom) == os.path.abspath(dirTo)
            if same:
                print('Error: dirFrom same as dirTo')
            else:
                return (dirFrom,dirTo)

if __name__ == '__main__':
    import time
    dirstuple = getargs()                         # 获取源和目标目录
    if dirstuple:
        print('被操作的文件:')                     # 显示被操作的文件
        for file in listfiles(*dirstuple):
            print(file)
        if sys.version[0] == '3':                 # 等待是否继续完成操作
            answer = input('输入y或n:')
        else:
            answer = raw_input('输入y或n:')
        if answer != 'y':
            sys.exit()
        cpsamefile(*dirstuple)
        print('Copying...')
        start = time.clock()
        fcount,dcount = copytree(*dirstuple)
        print('copied', fcount,'files',dcount,'directories')
        print('in',time.clock() - start,'seconds')
