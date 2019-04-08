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
import userAgent
import randomIp

url = 'https://news.hao123.com/wangzhi'
re = requests.get(url, headers=userAgent.UserAgent().getRandomHeaders(), proxies = randomIp.RandomIp().getOneProxies())
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