#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 针对解压程序的参数,弹出图形化界面对话框,运行程序

from tkinter import *                             # 小组件类
from unpacker import unpack                       # 使用解压脚本/模块
from formrows import makeFormRow                  # 表单域构造程序

def unpackDialog():                   
    win = Toplevel()
    win.title('Enter Unpack Parameters')
    var = makeFormRow(win, label='Input file', width=11)
    win.bind('<Key-Return>', lambda event: win.destroy())
    win.grab_set()
    win.focus_set()                  # 处理动作,直到窗口销毁
    win.wait_window()                # 或者
    return var.get()                 # 通过wm操作关闭

def runUnpackDialog():
    input = unpackDialog()                    # 从图形界面获得输入
    if input != '':                           # 处理非图形界面化的东西
        print('Unpacker:', input)             # 从对话框获得输入,运行程序
        unpack(ifile=input, prefix='')

if __name__ == "__main__":
    Button(None, text='popup', command=runUnpackDialog).pack()
    mainloop()
