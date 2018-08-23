#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/5/3 17:16

"""
粗略实现类似于文件的类.通过这些类能将输入输出重定向到图形界面上显示;输入来自于
通用的弹出式对话框(一个能将输入输出融合起来的界面,或者一个持续的,用于输入的数据
录入字段更好);对于字节数大于len(line)的读取请求,分行会出现问题;也可向GuiInput
里增加__iter__或者__next__以像文件一样支持行迭代,但会出现过多的弹窗;
"""

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText

class GuiOutput:
    font = ('courier',9,'normal')          # 在类里,适用于整体,而self只适用于个体
    def __init__(self,parent=None):
        self.text = None
        if parent: self.popupnow(parent)   # 先弹出或第一次写入parent窗口

    def popupnow(self,parent=None):        # 然后再到顶层窗口
        if self.text: return
        self.text = ScrolledText(parent or Toplevel())
        self.text.config(font=self.font)
        self.text.pack()
    def write(self,text):
        self.popupnow()
        self.text.insert(END,str(text))
        self.text.see(END)
        #self.text.update()                  # 每行结束后更新界面

    def writeline(self,lines):              # 有'\n'的行
        for line in lines: self.write(line) # 或者使用map(self.write,line)

class GuiInput:
    def __init__(self):
        self.buff = ''

    def inputLine(self):
        line = askstring('GuiInput','Enter input line + <crlf>(cancel=eof)')
        if line == None:
            return ''                 # 针对各行弹出对话框
        else:                         # 取消按钮表示文件末尾
            return line + '\n'        # 否则,添加行结束的标记

    def read(self,bytes=None):
        if not self.buff:
            self.buff = self.inputLine()
        if bytes:                            # 按照字节数读入
            text = self.buff[:bytes]         # 不分行
            self.buff = self.buff[bytes:]
        else:
            text = ''                        # 持续读入,直到行末
            line = self.buff
            while line:
                text = text + line
                line = self.inputLine()      # 直到cancel eof或者''
        return text

    def readline(self):
        text = self.buff or self.inputLine()    # 枚举文件读取方法
        self.buff = ''
        return text

    def readlines(self):
        lines = []                           # 读入所有的行
        while True:
            next = self.readline()
            if not next: break
            lines.append(next)
        return lines

def redirectedGuiFunc(func,*pargs,**kargs):
    import sys
    saveStreams = sys.stdin,sys.stdout        # 将函数中的流映射输入到弹出的窗口中
    sys.stdin = GuiInput()                    # 根据需要弹出对话框
    sys.stdout = GuiOutput()                  # 响应调用,创建新的输出窗口
    sys.stderr = sys.stdout

    result = func(*pargs,**kargs)             # 这里阻塞调用
    sys.stdin,sys.stdout = saveStreams
    return result

def redirectedGuiShellCmd(command):
    import os
    input = os.popen(command,'r')
    output = GuiOutput()
    def reader(input,output):                 # 显示一个shell命令的
        while True:                           # 标准输出
            line = input.readline()           # 在新的弹出式文件框组件中
            if not line: break                # 调用readline时可能阻塞
            output.write(line)
    reader(input,output)

if __name__ == '__main__':           # 运行时自测
    def makeUpper():                 # 使用标准流
        while True:
            try:
                line = input('Line? ')
            except:
                break
            print(line.upper())
        print('end of file')

    def makeLower(input,output):     # 使用显式文件
        while True:
            line = input.readline()
            if not line: break
            output.write(line.lower())
        print('end of file')

    root = Tk()
    Button(root,text='test streams',
           command=lambda: redirectedGuiFunc(makeUpper)).pack(fill=X)
    Button(root,text='test files',
           command=lambda: makeLower(GuiInput(),GuiOutput())).pack(fill=X)
    Button(root,text='test.popen',
           command=lambda: redirectedGuiShellCmd('dir *')).pack(fill=X)
    root.mainloop()