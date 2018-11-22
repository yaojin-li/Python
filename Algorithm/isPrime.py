"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 题目：判断101-200之间有多少个素数，并输出所有素数。
 程序分析：判断素数的方法：
 用一个数分别去除2到sqrt(这个数)，如果能被整除， 则表明此数不是素数，反之是素数。
 --------------------------------
 @Time    : 2018/11/22 9:18
 @File    : isPrime.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import math


def isPrime(num):
    flag = True
    for i in range(2, int(math.sqrt(num) + 1)):     # <=， +1表示判断math.sqrt(num)这个数是否为素数
        if num % i == 0:
            flag = False
            break
    return flag

if __name__ == '__main__':
    beginNum = 101
    endNum = 200
    count = 0
    for i in range(beginNum, endNum):
        if isPrime(i):
            count += 1
            print(i, end=" ")
    print("总数：", count)
