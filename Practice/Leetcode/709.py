"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
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
