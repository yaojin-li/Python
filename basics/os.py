"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/5/26 10:12
 @File    : os.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import os
import shutil

current_path = "D:\ZX_workspace\Python\Basics\osRelated.py"

# 1.获取当前文件绝对路径
print(os.path.abspath(__file__))
print(os.path.abspath("osRelated1.py"))

# 2.获取当前文件夹绝对路径
print(os.path.dirname(__file__))
print(os.path.dirname(os.path.abspath(__file__)))
#   os.path.sep为 \\
print(os.path.abspath(os.path.dirname(__file__) + os.path.sep + "."))
print(os.path.abspath(os.path.dirname(current_path) + os.path.sep + "."))

# 3.切换目录 参数为目录路径，非文件路径
print(os.chdir(os.path.dirname(current_path)))

# 4.拼接路径与文件
print(os.path.join(os.path.abspath(os.path.dirname(__file__)), "aa.txt"))

# 5. . .. \\ ; 等标记在ntpath.py中已经封装
print(os.path.pardir)

# 6.
print(os.getcwd())

# 7.返回指定目录下的所有文件和目录名
print(os.listdir(os.path.dirname(current_path)))

