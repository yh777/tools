#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/4/28 14:20

"""
一个能自动创建窗口中菜单和工具栏的扩展框架.使用GuiMakerFrameMenu生成嵌入式组件
(创建于框架的菜单).使用GuiMakerwindowMenu生成顶层窗口.
布局树格式示例请参看自测代码
"""

import sys
from tkinter import *                      # 导入组件的类
from tkinter.messagebox import showinfo

class GuiMaker(Frame):
    menuBar = []          # 类的默认值
    toolBar = []          # 在子类中依实例而改变
    helpButton = True     # 需要self时,在start()中设置

    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)    # 让框架可延伸
        self.start()                       # 针对子类:设置菜单/工具栏
        self.makeMenuBar()                 # 至此完成菜单栏的创建
        self.makeToolBar()                 # 至此完成工具栏的创建
        self.makeWidgets()                 # 针对子类:增加中间部分

    def makeMenuBar(self):
        """
        在顶部创建菜单栏
        expand=no,fill=x,调整时保持宽度一致
        """
        menubar = Frame(self,relief=RAISED,bd=2)
        menubar.pack(side=TOP,fill=X)

        for (name,key,items) in self.menuBar:
            mbutton = Menubutton(menubar,text=name,underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.addMenuItems(pulldown,items)
            mbutton.config(menu=pulldown)

        if self.helpButton:
            Button(menubar,text='Help',
                   cursor='gumby',
                   relief = FLAT,
                   command=self.help).pack(side=RIGHT)

    def addMenuItems(self,menu,items):
        for item in items:                # 扫描嵌套项列表
            if item == 'separator':       # 对于字符串,添加分隔符
                menu.add_separator({})
            elif type(item) == list:      # 对于列表,将状态变为DISABLED
                for num in item:
                    menu.entryconfig(num,state=DISABLED)
            elif type(item[2]) != list:
                menu.add_command(label=item[0],         # 对于命令
                                 underline=item[1],     # 创建子菜单
                                 command=item[2])       # 添加层叠
            else:
                pullover = Menu(menu)
                self.addMenuItems(pullover,item[2])
                menu.add_cascade(label=item[0],
                                 underline=item[1],
                                 menu=pullover)

    def makeToolBar(self):
        """
        在底部创建按钮栏(如果有)expand=no,fill=x调整时保持宽度一致
        此处也可支持图片,需要有事先创建的gif图片或者PIL库以供生成缩略图
        """
        if self.toolBar:
            toolbar = Frame(self,cursor='hand2',relief=SUNKEN,bd=2)
            toolbar.pack(side=BOTTOM,fill=X)
            for (name,action,where) in self.toolBar:
                Button(toolbar,text=name,command=action).pack(where)

    def makeWidgets(self):
        """
        最后创建"中间"部分,以使菜单或者工具栏总是位于顶部或者底部,最后裁减;
        重写默认值,对中间部分的任意一边进行pack;对于网格:将pack后的框架的中间
        部分进行网格处理
        """
        name = Label(self,
                     width=40,height=10,
                     relief=SUNKEN,bg='white',
                     text = self.__class__.__name__,
                     cursor = 'crosshair')
        name.pack(expand=YES,fill=BOTH,side=TOP)

    def help(self):
        """
        在子类中对此进行重写
        """
        showinfo('Help','sorry, no help for ' + self.__class__.__name__)

    def start(self):
        """
        子类中对此进行重写: 使用self来对菜单或者工具栏进行设置
        """
        pass

GuiMakerFrameMenu = GuiMaker

class GuiMakerWindowMenu(GuiMaker):
    def makeMenubar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        for (name,key,items) in self.menuBar:
            pulldown = Menu(menubar)
            self.addMenuItems(pulldown,items)
            menubar.add_cascade(label=name,underline=key,menu=pulldown)

        if self.helpButton:
            if sys.platfor[:3] == 'win':
                menubar.add_command(label='Help',command=self.help)
            else:
                pulldown = Menu(menubar)
                pulldown.add_command(label='About',command=self.help)
                menubar.add_cascade(label='Help',menu=pulldown)

# 用于自测,单独运行文件python guimaker.py

if __name__ == '__main__':
    from guimixin import GuiMixin
    menuBar = [
        ('File',0,
         [('Open',0,lambda:0),       # lambda:0 不进行任何操作
          ('Quit',0,sys.exit)]),     # 这里使用sys,不使用self
        ('Edit',0,
         [('Cut',0,lambda :0),
          ('Paste',0,lambda:0)])
    ]
    toolBar = [('Quit',sys.exit,{'side': LEFT})]

    class TestAppFrameMenu(GuiMixin,GuiMakerFrameMenu):
        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    class TestAppWindowMenu(GuiMixin,GuiMakerWindowMenu):
        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    class TestAppWindowMenuBasic(GuiMakerWindowMenu):
        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    root = Tk()
    TestAppFrameMenu(parent=Toplevel())
    TestAppWindowMenu(parent=Toplevel())
    TestAppWindowMenuBasic(parent=Toplevel())
    root.resizable(width=False,height=False)
    root.mainloop()