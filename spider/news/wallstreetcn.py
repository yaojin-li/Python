"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 华尔街见闻
 --------------------------------
 @Time    : 2019/5/13 22:16
 @File    : wallstreetcn.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests

# 先拿到网页中要爬取部分的所有链接
# url去重
# scarpy-reids
# 读取字段写到数据库

# targetUrl = "https://wallstreetcn.com/kechuang"
#
# re = requests.get(targetUrl)
# re.encoding=re.apparent_encoding
# html = re.text
#
# with open("html.txt","w",encoding="utf-8") as f:
#     f.write(str(html))

import re
import json


def getWallstreetData():
    with open("html.txt", "r", encoding="utf-8") as f:
        html = f.read()

    # 匹配获取文章列表页数据
    parten = r'<script>window.__IVANKA_API_CACHE__=(.*)</script>'
    res = re.findall(parten, html)

    # 匹配结果转换成字典
    dictinfo = str2dict(res[0])
    cachedResponseDic = dictinfo['cachedResponse']

    # 遍历字典，匹配key
    for key, value in cachedResponseDic.items():
        if "information-flow" in key:
            nextCursor = value.get('value').get('next_cursor')
            items = value.get('value').get('items')
            return nextCursor, items


# json格式的字符串转换成字典（json）
def str2dict(str):
    return json.loads(str)


# dict中的数据入库
def data2oracle(dict):
    print(dict)


# 获取url的text
def requestUrl(url):
    re = requests.get(url)
    re.encoding = re.apparent_encoding
    return re.text


# 爬取指定个数的数据
def getLimitData(url):
    returnJsonStr = requestUrl(url)
    jsonDict = str2dict(returnJsonStr)
    items = jsonDict['data']['items']
    return items


# 解析文章的详细信息，返回详细信息的字典
def getArticleDetail(url):
    html = requestUrl(url)
    pass


if __name__ == '__main__':
    nextCursor, pre20Items = getWallstreetData()

    # limit = 10  # 返回个数
    # url = "https://api.wallstreetcn.com/apiv1/content/information-flow?channel=kechuang&accept=article%2Cad&cursor=" + nextCursor + "&limit=" + str(limit)
    # allItems = pre20Items.extend(getLimitData(url))
    # print(allItems)


    allItems = []

    # 遍历所有items，合并所有信息，入库
    for itemDic in allItems:
        print(itemDic)
        detailDic = getArticleDetail(itemDic['resource']['uri'])

        # 合并两个字典itemDic与detailDic，返回最终结果入库
        result = {}

        # 已有的信息与详细信息合并后，数据入库
        data2oracle(result)
