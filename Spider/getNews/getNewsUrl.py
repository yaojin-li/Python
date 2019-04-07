"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/4/5 19:39
 @File    : getNewsUrl.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 'Referer': 'http://www.mzitu.com'}
Picreferer = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 'Referer': 'http://i.meizitu.net'}

url = 'https://news.hao123.com/wangzhi'
re = requests.get(url, headers=headers)
html = re.text
struct = etree.HTML(html)

# with open("newUrl.txt",'w',encoding='utf-8') as f:
#     f.write(html)

for i in range(1, 21):
    newName = struct.xpath('//*[@id="bd"]/div[1]/div/ul/li[' + str(i) + ']/h3/div/a/text()')
    href = struct.xpath('//*[@id="bd"]/div[1]/div/ul/li[' + str(i) + ']/h3/div/a/@href')
    print(newName, href)

for i in range(1, 25):
    newName1 = struct.xpath('//*[@id="bd"]/div[2]/div/ul/li[' + str(i) + ']/h3/div/a/text()')
    href1 = struct.xpath('//*[@id="bd"]/div[2]/div/ul/li[' + str(i) + ']/h3/div/a/@href')
    print(newName1, href1)