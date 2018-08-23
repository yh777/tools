#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/5/4 11:42

# 将命令行脚本包装到图形界面重定向工具中,输出显示到弹出式窗口中

from tkinter import *
from packdlg import runPackDialog
from guiStreams import redirectedGuiFunc

def runPackDialog_wrapped():
    redirectedGuiFunc(runPackDialog)

if __name__ == '__main__':
    root = Tk()
    Button(root,text='pop',command=runPackDialog_wrapped).pack(fill=X)
    root.mainloop()