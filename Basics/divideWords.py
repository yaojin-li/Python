"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : HanLP, baiduNLP, jieba分词对比
 --------------------------------------
 @File        : divideWords.py
 @Time        : 2018/8/25 22:10
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

# import hanlp
from aip import AipNlp
from jieba import *

class baidu_nlp:
    def __init__(self):
        self.APP_ID = "020e0df2b55441d9b90861ea2b457ddf"
        self.API_KEY = "51fa55f6feb94a0fb7d4de49f111d6c2"
        self.SECRET_KEY = "129ba31afdaa439da5cf9ab0cd07d8f4"
        self.client = AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def cifa(self, text):
        cifa = self.client.lexer(text)
        print(cifa)

class jieba:
    pass


if __name__ == '__main__':
    text = "你好，欢迎在Python中使用百度NLP"
    baidu_nlp = baidu_nlp()
    baidu_nlp.cifa(text)

# print(HanLP.segment("你好，欢迎在Python中调用HanLP的API"))
#
# testCase = [
#     "商品和服务",
#     "结婚的和尚未结婚的确实在干扰分词啊",
#     "买水果然后来世博园最后去世博会",
#     "中国的首都是北京",
#     "欢迎新老师生前来就餐",
#     "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作",
#     "随着页游兴起到现在的页游繁盛，依赖于存档进行逻辑判断的设计减少了，但这块也不能完全忽略掉。"]
# for sentence in testCase:
#     print(HanLP.segment(sentence))













