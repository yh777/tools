#!/usr/bin/env python
#-*- coding: utf-8 -*-

# @Time    : 2018/4/17 10:46

"""
###################################################################################
用命令行和可复用的启动方案类来启动Python程序;在命令开头自动向Python可执行文件插入
"python"和/或路径;这个模块的某些部分可能假定'python'在你的系统路径中(参考Launcher.py);

使用supprocess模块也可行,不过os.popen()在内部调用这个模块,目标是在这里启动一个独立运行的
程序,而非连接到它的流;multiprocessing模块也是一个选择,不过这里处理命令行非函数,为实现
这里的选项之一而开始一个进程不是很合理

这一版本的更新:脚本文件名称路径将经过normpath()处理,必要时将所有/改成\以供Windows工具使用;
pyEdit和其他工具继承这个修正;在Windows下,一般允许在文件打开中用/,但并非所有启动工具
###################################################################################
"""

import sys, os
pyfile = (sys.platform[:3] == 'win' and 'python.exe') or 'python'
pypath = sys.executable     # 使用较新的pys中的sys

def fixWindowsPath(cmdline):
    """
    将cmdline开头的脚本文件名路径里的所有/改成\;Windowsgh ,仅为运行需要这种处理的
    工具的类所使用;在其他平台上,这么做也没有坏处(比如Unix下的os.system);
    """
    splitline = cmdline.lstrip().split(' ')           # 在空格处分隔字符串,lstrip()返回截掉字符串左边的空格或指定字符后生成的新字符串,rstrip()返回截掉字符串右边的空格或指定字符后生成的新字符串
    fixedpath = os.path.normpath(splitline[0])        # 解决斜杠的问题
    return ' '.join([fixedpath] + splitline[1:])      # 把路径重新拼起来

class LaunchMode:
    """
    在实例中待命,声明标签并运行命令;子类按照run()中的需要格式化命令行;命令应当以
    装备运行的Python脚本名开头,而且不带"python"或脚本的完整路径;
    """
    def __init__(self, label, command):
        self.what  = label
        self.where = command
    def __call__(self):                     # 等待调用,执行按钮按下的回调动作
        self.announce(self.what)
        self.run(self.where)                # 子类必须定义run()
    def announce(self, text):               # 子类可以重新定义announce()
        print(text)                         # 用方法代替if/else逻辑
    def run(self, cmdline):
        assert False, 'run must be defined'

class System(LaunchMode):
    """
    运行shell命令行中指定的Python脚本;小心,可能阻塞调用者,除非在
    Unix下带上&操作符
    """
    def run(self, cmdline):
        cmdline = fixWindowsPath(cmdline)
        os.system('%s %s' % (pypath, cmdline))

class Popen(LaunchMode):
    """
    在新进程中运行shell命令行;小心:可能阻塞调用者,因为管道关闭得太快
    """
    def run(self, cmdline):
        cmdline = fixWindowsPath(cmdline)
        os.popen(pypath + ' ' + cmdline)           # 假设没有数据可读取

class Fork(LaunchMode):
    """
    显式地创建的新进程中运行命令,仅在类Unix系统下可用
    """
    def run(self, cmdline):
        assert hasattr(os, 'fork')
        cmdline = cmdline.split()                  # 把字符串转换成列表
        if os.fork() == 0:                         # 开始新的子进程
            os.execvp(pypath, [pyfile] + cmdline)  # 在子进程中运行新程序

class Start(LaunchMode):
    """
    独立于调用者运行程序;仅在Windows下可用:使用了文件名关联
    """
    def run(self, cmdline):
        assert sys.platform[:3] == 'win'
        cmdline = fixWindowsPath(cmdline)
        os.startfile(cmdline)

class StartArgs(LaunchMode):
    """
    仅在Windows下可用:args可能需要用到真正的start命令:斜杠在这里没问题
    """
    def run(self, cmdline):
        assert sys.platform[:3] == 'win'
        os.system('start ' + cmdline)              # 可能会创建弹出窗口

class Spawn(LaunchMode):
    """
    在独立于调用者的新进程中运行python;在Windows和Unix下都可用;
    DOS中使用P_NOWAIT;斜杠在这里没问题
    """
    def run(self, cmdline):
        os.spawnv(os.P_DETACH, pypath, (pyfile, cmdline))

class Top_level(LaunchMode):
    """
    在新窗口中运行,进程是同一个;
    """
    def run(self, cmdline):
        assert False, 'Sorry - mode not yet implemented'

#
# 为这个平台挑选一个"最佳"启动器
# 可能需要在其他地方细化这个选项
#

if sys.platform[:3] == 'win':
    PortableLauncher = Spawn
else:
    PortableLauncher = Fork

class QuietPortableLauncher(PortableLauncher):
    def announce(self, text):
        pass

def selftest():
    file = 'echo.py'
    input('default mode...')
    launcher = PortableLauncher(file, file)
    launcher()                                             # 不阻塞

    input('system mode...')
    System(file, file)()                                   # 阻塞

    if sys.platform[:3] == 'win':
        input('DOS start mode...')                         # 不阻塞
        StartArgs(file, file)()

if __name__ == '__main__': selftest()