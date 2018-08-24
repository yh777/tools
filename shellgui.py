#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/5/2 16:23

"""
工具启动器,使用guimaker模板,guimixin标准quit对话框;本程序只是一个类库,要显示图形界面,
请运行mytools脚本;
"""

from tkinter import *            # 获取小组件
from guimixin import GuiMixin    # 获取quit(未实现)
from guimaker import *           # 菜单/工具栏生成器

class ShellGui(GuiMixin,GuiMakerWindowMenu):    # 框架 + maker + mixins
    def start(self):                            # 如果是组件,使用GuiMaker
        self.setMenuBar()
        self.setToolBar()
        self.master.title('Shell Tools Listbox')
        self.master.iconname('Shell Tools')

    def handleList(self,event):                    # 双击列表框时
        label = self.listbox.get(ACTIVE)           # 获取选中的文本
        self.runCommand(label)                     # 并调用此处的操作

    def makeWidgets(self):                         # 在中部添加列表框
        sbar = Scrollbar(self)                     # 交叉链接栏(sbar),列表
        list = Listbox(self,bg='white')            # 也可使用Tour.ScrolledList
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT,fill=Y)                   # 先pack的后裁减
        list.pack(side=LEFT,expand=YES,fill=BOTH)      # 最先clip的列表
        for (label,action) in self.fetchCommands():    # 添加至列表框
            list.insert(END,label)                     # 和菜单/工具栏
        list.bind('<Double-1>',self.handleList)        # 设置事件处理器
        self.listbox = list

    def forToolBar(self,label):                        # 是否放到工具栏上?
        return True # default = all

    def setToolBar(self):
        self.toolBar = []
        for (label, action) in self.fetchCommands():
            if self.forToolBar(label):
                self.toolBar.append((label,action,dict(sid=LEFT)))
        self.toolBar.append(('Quit',self.quit,dict(side=RIGHT)))

    def setMenuBar(self):
        toolEntries = []
        self.menuBar= [
            ('File',0,[('Quit',-1,self.quit)]),        # 下拉菜单名称
            ('Tools',0,toolEntries)                    # 菜单项目列表
        ]                                              # 标签,下划线,操作
        for (label,action) in self.fetchCommands():
            toolEntries.append((label,-1,action))        # 将各项添加至菜单

# 针对特定模板类型的子类而设计,后者又针对特定应用工具集的子类而设计

class ListMenuGui(ShellGui):
    def fetchCommands(self):                  # 子类别:设置"myMenu"
        return self.myMenu                    # 列表(label,callback)
    def runCommand(self,cmd):
        for (label,action) in self.myMenu:
            if label == cmd: action()

class DictMenuGui(ShellGui):
    def fetchCommands(self):
        return self.myMenu.items()
    def runCommand(self,cmd):
        self.myMenu[cmd]()