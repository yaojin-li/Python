"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/4/15 22:05
 @File    : 771.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class SolutionOne:
    """
    两次for循环
    """
    def numJewelsInStones(self, J: str, S: str) -> int:
        num = 0
        for j in J:
            for s in S:
                if j == s:
                    num = num + 1
        return num


class SolutionTwo:
    """
    一层for循环 + 判断
    """
    def numJewelsInStones(self, J: str, S: str) -> int:
        num=0
        for s in S:
            if s in J:
                num+=1
        return num

class SolutionThree:
    """
    set()
    """
    def numJewelsInStones(self, J: str, S: str) -> int:
        jSet = set(J)
        return sum(s in jSet for s in S)

J = "aA"
S = "aAAbbbb"
print(SolutionTwo().numJewelsInStones(J, S))
