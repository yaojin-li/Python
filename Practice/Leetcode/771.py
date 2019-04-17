"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 给定字符串J 代表石头中宝石的类型，和字符串 S 代表你拥有的石头。S 中每个字符代表了一种你拥有的石头的类型，
 你想知道你拥有的石头中有多少是宝石。
 J 中的字母不重复，J 和 S中的所有字符都是字母。字母区分大小写，因此"a"和"A"是不同类型的石头。
 示例 1:
 输入: J = "aA", S = "aAAbbbb"
 输出: 3
 示例 2:
 输入: J = "z", S = "ZZ"
 输出: 0
 注意:
 S 和 J 最多含有50个字母。
 J 中的字符不重复。
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
