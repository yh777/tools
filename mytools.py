#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/5/3 9:41

"""
针对具体类型,为应用提供具体的选项
"""

from shellgui import *                   # 与类型有关的gui选项
from packdlg import runPackDialog        # 用于数据输入
from unpkdlg import runUnpackDialog      # 二者都运行应用类

class TextPak1(ListMenuGui):
    def __init__(self):
        self.myMenu = [('Pack',runPackDialog),        # 简单函数
                       ('Unpack',runUnpackDialog),    # 这里使用相同的宽度
                       ('Mtool',self.notdone)]        # 来自guimixin的方法
        ListMenuGui.__init__(self)

    def forToolBar(self,label):
        return label in {'Pack','Unpack'}             # 3.x版本的语法

class TextPak2(DictMenuGui):
    def __init__(self):
        self.myMenu = {'Pack':runPackDialog,         # 这里也可以转入
                       'Unpack':runUnpackDialog,       # 输入也可不来自对话,而使用此处的
                       'Mtool':self.notdone}
        DictMenuGui.__init__(self)

if __name__ == '__main__':                    # 自测代码
    from sys import argv
    if len(argv) > 1 and argv[1] == 'list':
        print('list test')
        TextPak1().mainloop()
    else:
        print('dict test')
        TextPak2().mainloop()