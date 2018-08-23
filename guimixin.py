#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/4/28 10:30

"""
用于其他框架的'mixin'类:针对预制对话框,具有生成能力的程序,简易文本查看器等
的共用方法;针对quit方法,本类必须与一个Frame(或者一个从Frame中派生出来的子类)搭配使用
"""

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from scrolledtext import ScrolledText              # 也可用tkinter.scrolledtext
from launchmodes import PortableLauncher,System    # 也可以使用多重处理

class GuiMixin:
    def infobox(self,title,text,*args):            # 使用标准对话框
        return showinfo(title,text)                # *args来实现向后兼容

    def errorbox(self,text):
        showerror('Error!',text)

    def question(self,title,text,*args):
        return askyesno(title,text)                # 返回True或者False

    def notdone(self):
        showerror('Not implemented','Option not available')

    def quit(self):
        ans = self.question('Verify quit','Are you sure you want to quit?')
        if ans:
            Frame.quit(self)

    def help(self):
        self.infobox('RTFM','See figure 1...')     # 建议重写

    def selectOpenFile(self,file='',dir=''):
        return askopenfilename(initialdir=dir,initialfile=file)

    def selectSaveFile(self,file='',dir='.'):
        return asksaveasfilename(initialdir=dir,initialfile=file)

    def clone(self,args=()):                      # 可选的方法参数
        new = Toplevel()                          # 生成一个新的进程中的版本
        myclass = self.__class__                  # 实例的(最低级)class对象
        myclass(new,*args)                        # 将实例附加到一个新窗口中

    def spawn(self,pycmdline,wait=False):
        if not wait:                                   # 启动新进程
            PortableLauncher(pycmdline,pycmdline)()    # 运行Python程序
        else:
            System(pycmdline,pycmdline)()              # 等待程序退出

    def browser(self,filename):
        new = Toplevel()                                  # 新建窗口
        view = ScrolledText(new,file=filename)            # 带有滚动条的文本框
        view.text.config(height=30,width=85)              # 在框架中显示配置文件
        view.text.config(font=('courier',10,'normal'))    # 使用宽度固定的字体
        new.title('Text Viewer')                          # 设置窗口管理器的属性
        new.iconname('browser')                           # 自动添加文本文件

    """
    def browser(self,filename):
        new = Toplevel()                                  # 针对tkinter.scrolledtext
        text = ScrolledText(new,height=30,width=85)       # 供参考
        text.config(font=('courier',10,'normal'))
        text.pack(expand=YES,fill=BOTH)
        new.title('Text Viewer')
        new.iconname('browser')
        text.insert('0.0',open(filename,'r').read())
    """

if __name__ == '__main__':
    class TestMixin(GuiMixin,Frame):                      # 独立测试
        def __init__(self,parent=None):
            Frame.__init__(self,parent)
            self.pack()
            Button(self,text='quit',command=self.quit).pack(fill=X)
            Button(self,text='help',command=self.help).pack(fill=X)
            Button(self,text='clone',command=self.clone).pack(fill=X)
            Button(self,text='spawn',command=self.other).pack(fill=X)
            Button(self,text='infobox',command=lambda :self.infobox('infobox','infobox')).pack(fill=X)
            Button(self,text='errorbox',command=lambda :self.errorbox('ERROR,ERROR!!!')).pack(fill=X)
            Button(self,text='question',command=lambda :self.question('Question','Question!!!')).pack(fill=X)
            Button(self,text='notdone',command=self.notdone).pack(fill=X)
            Button(self,text='selectOpenFile',command=self.selectOpenFile).pack(fill=X)
            Button(self,text='selectSaveFile',command=self.selectSaveFile).pack(fill=X)
            Button(self,text='browser',command=lambda file='../jack.txt': self.browser(file)).pack(fill=X)

        def other(self):
            self.spawn('guimixin.py')             # 将self生成独立进程

    TestMixin().mainloop()