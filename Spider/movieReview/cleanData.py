"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 数据处理
 --------------------------------------
 @File        : cleanData.py
 @Time        : 2018/8/25 16:33
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import re

def cleanData(HTMLDic):
    # for key in HTMLDic.keys():
    print(type(HTMLDic[str(6)]))   # 内容
    content = HTMLDic[str(6)]
    for i in range(len(content)):
        content[i] = re.sub(r'\*|\'|\ |\\|\/', "", str(content[i]))
    print(content)
    '''
    jasdfj
    '''


def getHTMLDic():
    tempFile = "./cleanData.txt"
    with open(tempFile, "r", encoding = "utf-8") as f:
        tempStr = f.read()
    tempDic = eval(tempStr)     # str to dic
    return tempDic


def main():
    HTMLDic = getHTMLDic()
    cleanData(HTMLDic)

main()

