#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/4/17 11:22
# @Author  : jiangysh
"""
渠道csv加密(多进程),选项提供所有需要加密的渠道号,脚本自行区分Android或iPhone
使用方法: multi_jiami.py qdNumber qdNumber ......
"""

import os,sys,time
from multiprocessing import Process

basicDir = '/opt/web/soonyo_yx/game_download/by'    # 渠道资源所在的根目录
shellScriptAn = '/root/sh/android_jiami_md5.sh'     # 安桌加密脚本
shellScriptIp = '/root/sh/iphone_jiami_md5.sh'      # iphone加密脚本

def whatSys(qdNum):                                 # 判断渠道是啥系统
    return os.listdir(basicDir + '/' + qdNum)[0]

def run(qdNum):                       # 加密函数
    sysName = whatSys(qdNum)
    if sysName == 'Android':
        os.system(shellScriptAn + ' ' + qdNum)
    elif sysName == 'iPhone':
        os.system(shellScriptIp + ' ' + qdNum)
    else:
        print(('%s 渠道目录不规范,未执行加密') % qdNum)

if len(sys.argv) > 1:
    qdNums = sys.argv[1:]         # 要加密的渠道
else:
    print('使用方法: multi_jiami.py qdNumber qdNumber ......')
    sys.exit()

processes = []
for qdNum in qdNums:
    p = Process(target=run,args=(qdNum,))
    p.start()
    processes.append(p)
    time.sleep(2)

for p in processes:
    p.join()