"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2018/11/23 11:37
 @File    : daffodil.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

def getDaffodil():
    beginNum = 101
    endNum = 1000
    for i in range(beginNum, endNum):
        a = int(i%10)           # int()取整数，否则计算浮点数
        b = int(i/10%10)
        c = int(i/100)
        if a**3 + b**3 + c**3 == i:
            print(i)

if __name__ == '__main__':
    getDaffodil()
