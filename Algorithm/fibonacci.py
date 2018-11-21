"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 斐波那契数
 1、1、2、3、5、8、13、21、…… 斐波那契数列以递归的方法定义：F0=0，F1=1，Fn=Fn-1+Fn-2（n>=2，n∈N*）
 即：斐波那契数列由 0 和 1 开始，之后的斐波那契数列系数就由之前的两数相加。
 --------------------------------
 @Time    : 2018/11/21 17:07
 @File    : fibonacci.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class fibonacci():
    def __init__(self, num):
        self.num = num

    # 建立数组
    def getFibonacciList_three(self):
        result = []
        result.insert(0, 1)
        result.insert(1, 1)
        for i in range(2, self.num):
            result.insert(i, result[i-1] + result[i-2])
        print(result)

    # 直接打印
    def getFibonacciList_two(self):
        one, two = 1, 1
        print(one, two, end="\t")
        for i in range(2, self.num):
            three = one + two
            one, two = two, three
            print(three, end="\t")


# 递归
def getFibonacciList_one(num):
    if num in [0, 1]:
        return 1
    else:
        return getFibonacciList_one(num - 1) + getFibonacciList_one(num - 2)


if __name__ == '__main__':
    num = 10
    fibonacci = fibonacci(num)
    for i in range(num):
        print(getFibonacciList_one(i), end="\t")

    fibonacci.getFibonacciList_two()

    fibonacci.getFibonacciList_three()
