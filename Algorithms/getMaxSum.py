"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 寻找数组的最大子列和，从第一个位置起，时间复杂度为O(N)
 --------------------------------------
 @File        : getMaxSum.py
 @Time        : 2018/4/16 15:55
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

def maxSubseqSum(A):
    thisSum, maxSum = 0, 0
    for i in range(len(A)):
        thisSum += A[i]     # 对当前和向右进行累加
        if thisSum > maxSum:
            maxSum = thisSum    # 发现更大的和则更新当前结果
        elif thisSum < 0:   # 如果当前子列和为负
            thisSum = 0     # 不可能使后面的部分和增大，抛弃之
    print(maxSum)

def main():
    A = [-1, 3, -1, 4, -6, 1, 8, -1]
    maxSubseqSum(A)

if __name__ == '__main__':
    main()


