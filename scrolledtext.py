"""
一个简单的文本或文件查看器组件
"""

print('PP4E scrolledtext')
from tkinter import *

class ScrolledText(Frame):
    def __init__(self,parent=None,text='',file=None):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)                  # 可扩展
        self.makewidgets()
        self.settext(text,file)

    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self,relief=SUNKEN)
        sbar.config(command=text.yview)                  # 连接sbar和text
        text.config(yscrollcommand=sbar.set)             # 移动一个就会移动另一个
        sbar.pack(side=RIGHT,fill=Y)
        text.pack(side=LEFT,expand=YES,fill=BOTH)
        self.text = text

    def settext(self,text='',file=None):
        if file:
            text = open(file,'r').read()
        self.text.delete('1.0',END)                      # 删除相当文本
        self.text.insert('1.0',text)                     # 在第一行的第一列添加
        self.text.mark_set(INSERT,'1.0')                 # 设置插入的光标位置
        self.text.focus()                                # 设置输入焦点

    def gettext(self):
        return self.text.get('1.0',END+'-1c')            # 获取文本内容

if __name__ == '__main__':
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1])              # 从命令行获取文件名
    else:
        st = ScrolledText(text='Words\ngo here')         # 或者输入默认的两行文本
    def show(event):
        print(repr(st.gettext()))                        # 获取字符串
    root.bind('<Key-Escape>',show)                       # 当按下ESC时,调用show函数
    root.mainloop()