#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 弹出图形化对话框,供选择打包脚本参数的输入,并运行

from glob import glob                           # 文件扩展名
from tkinter import *                           # GUI小组件
from packer import pack                         # 使用packer脚本中的模块
from formrows import makeFormRow                # 使用表单构建工具

def packDialog():                               # 新的顶层窗口
    win = Toplevel()                            # 有两行图文框,还带有有'OK'按钮
    win.title('Enter Pack Parameters')
    var1 = makeFormRow(win, label='Output file')
    var2 = makeFormRow(win, label='Files to pack', extend=True) 
    Button(win, text='OK', command=win.destroy).pack()         # destroy方法只关闭一个窗口,而不是全使用sys.exit关闭整个程序
    win.grab_set()                   
    win.focus_set()                  # 动作:鼠标选取数据;键盘获得焦点;等待
    win.wait_window()                # 等到窗口销毁,否则立即退出
    return var1.get(), var2.get()    # 获取相关联的变量值

def runPackDialog():
    output, patterns = packDialog()                  # 弹出图形化对话框
    if output != "" and patterns != "":              # 直到'OK'或窗口销毁
        patterns = patterns.split()                  # 现在处理图形界面以外的部分
        filenames = []
        for sublist in map(glob, patterns):          # 手动添加扩展名
            filenames += sublist                     # Unix shell自动执行此步
        print('Packer:', output, filenames)
        pack(ofile=output, ifiles=filenames)         # 消息也以图形化方式呈现

if __name__ == '__main__':
    root = Tk()
    Button(root, text='popup', command=runPackDialog).pack(fill=X)
    Button(root, text='bye',   command=root.quit).pack(fill=X)
    root.mainloop()
