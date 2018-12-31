"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 
 --------------------------------------
 @File        : 00.py
 @Time        : 2018/12/31 17:52
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import os


# with open("F:\\a.html", "r+", encoding="utf-8") as f:
#     html = f.read()
#     pattern=r'<img .*?/>'
#     imgre = re.compile(pattern)
#     imglist=re.findall(imgre,html)
#     print(len(imglist),imglist)

html="123456"
imglist=['1','2','3','4']
pathlist=['a','b','c','d']
for img, path in zip(imglist, pathlist):
    if html.__contains__(img):
        new="-"+path
        a=html.replace(img, new)
        print(a)
        html=a
print(html)