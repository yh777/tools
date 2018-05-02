#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/5/2 10:35

"""
GUI实现演示
"""

import sys,os
from tkinter import *     # 小组件
from guimixin import *    # guimixin.py中的方法,包括quit,spawn等
from guimaker import *    # 框架,菜单,工具栏生成器

class Hello(GuiMixin, GuiMakerWindowMenu):   # 或者GuiMakerFrameMenu
    def start(self):
        self.hellos = 0
        self.master.title("GuiMaker Demo")
        self.master.iconname("GuiMaker")
        def spawnme(): self.spawn('big_gui.py')        # 推迟调用和lambda表达式

        self.menuBar = [                               # 有3个下拉菜单
          ('File', 0,                                  # 下拉菜单
              [('New...',  0, spawnme),
               ('Open...', 0, self.fileOpen),          # 菜单下的项目列表
               ('Quit',    0, self.quit)]              # 菜单下的标签,加下划线,单击后的操作
          ),

          ('Edit', 0,
              [('Cut',    -1, self.notdone),           # 不加下划线操作
               ('Paste',  -1, self.notdone),           # 使用lambda:0也可以
               'separator',                            # 添加分隔线
               ('Stuff',  -1,
                   [('Clone', -1, self.clone),         # 级联式子菜单
                    ('More',  -1, self.more)]
               ),
               ('Delete', -1, lambda:0),
               [5]]                                    # 禁用 'Delete'项
          ),

          ('Play', 0,
              [('Hello',     0, self.greeting),
               ('Popup...',  0, self.dialog),
               ('Demos',     0,
                  [('Toplevels', 0,
                       lambda: self.spawn(r'..\toplevel2.py')),
                   ('Frames',    0,
                       lambda: self.spawn(r'..\demoAll-frm-ridge.py')),
                   ('Images',    0,
                       lambda: self.spawn(r'..\buttonpics.py')),
                   ('Alarm',     0,
                       lambda: self.spawn(r'..\alarm.py', wait=False)),
                   ('Other...', -1, self.pickDemo)]
               )]
          )]

        self.toolBar = [                                     # 添加3个按钮
          ('Quit',  self.quit,     dict(side=RIGHT)),        # 也可以使用{'side':RIGHT}
          ('Hello', self.greeting, dict(side=LEFT)),
          ('Popup', self.dialog,   dict(side=LEFT, expand=YES)) ]

    def makeWidgets(self):                                   # 重载构建窗口中部的函数
        middle = Label(self, text='Hello maker world!',
                       width=40, height=10,
                       relief=SUNKEN, cursor='pencil', bg='white')
        middle.pack(expand=YES, fill=BOTH)

    def greeting(self):
        self.hellos += 1
        if self.hellos % 3:
            print("hi")
        else:
            self.infobox("Three", 'HELLO!')    # 每按3次按钮

    def dialog(self):
        button = self.question('OOPS!',
                               'You typed "rm*" ... continue?',  # 经典风格
                               'questhead', ('yes', 'no'))       # 忽略多个参数
        [lambda: None, self.quit][button]()

    def fileOpen(self):
        pick = self.selectOpenFile(file='big_gui.py')
        if pick:
            self.browser(pick)     # 浏览自己的源文件,或其他文件

    def more(self):
        new = Toplevel()
        Label(new,  text='A new non-modal window').pack()
        Button(new, text='Quit', command=self.quit).pack(side=LEFT)
        Button(new, text='More', command=self.more).pack(side=RIGHT)

    def pickDemo(self):
        pick = self.selectOpenFile(dir='..')
        if pick:
            self.spawn(pick)    # 生成任意Python程序

if __name__ == '__main__':  Hello().mainloop()   # 构建并运行