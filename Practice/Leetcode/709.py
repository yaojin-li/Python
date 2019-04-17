"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 实现函数 ToLowerCase()，该函数接收一个字符串参数 str，并将该字符串中的大写字母转换成小写字母，之后返回新的字符串。
 示例 1：
 输入: "Hello"
 输出: "hello"
 示例 2：
 输入: "here"
 输出: "here"
 示例 3：
 输入: "LOVELY"
 输出: "lovely"
 --------------------------------
 @Time    : 2019/4/17 23:06
 @File    : 709.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class SolutionOne:
    def toLowerCase(self, str: str) -> str:
        return str.lower()


class SolutionTwo:
    def toLowerCase(self, str: str) -> str:
        result = []
        for char in str:
            if 'A' <= char <= 'Z':  # Unicode编码是大写字母
                result.append(chr(ord(char) + 32))
            else:
                result.append(char)
        return "".join(result)


string = "Hello WORD"
# print(SolutionOne().toLowerCase(string))
print(SolutionTwo().toLowerCase(string))
