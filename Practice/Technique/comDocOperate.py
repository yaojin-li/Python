"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/5/25 22:28
 @File    : comDocOperate.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import os


def getSameEndsFileInDir(fileDir, endStr):
    """
    遍历文件夹下所有后缀为endStr的文件，获取同一目录下所有文件的绝对路径
    :param fileDir:
    :return:
    """
    fileList = []
    for root, dirs, files in os.walk(fileDir):
        for filePath in files:
            if str(filePath).endswith(endStr):
                fileList.append(os.path.join(root, filePath))
    return fileList
