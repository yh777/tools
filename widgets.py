#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/4/27 17:01

"""
基于一些假设(比如扩展),将小组件的结构打包到函数中,以方便使用;使用**extras来控制
宽度,字体,颜色等.后期使用时,如有需要可手动对结果进行重新打包,覆盖缺省值
"""

from tkinter import *

def frame(root,side=TOP,**extras):
    widget = Frame(root)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras: widget.config(**extras)
    return widget

def label(root,side,text,**extras):
    widget = Label(root,text=text,relief=RIDGE)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras: widget.config(**extras)
    return widget

def button(root,side,text,command,**extras):
    widget = Button(root,text=text,command=command)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras: widget.config(**extras)
    return widget

def entry(root,side,linkvar,**extras):
    widget = Entry(root,relief=SUNKEN,textvariable=linkvar)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras: widget.config(**extras)
    return widget

if __name__ == '__main__':
    app =Tk()
    frm = frame(app,TOP)
    label(frm,LEFT,'SPAM')
    button(frm,BOTTOM,'Press',lambda :print('Pushed'))
    mainloop()