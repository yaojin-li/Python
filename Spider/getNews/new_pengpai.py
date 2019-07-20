"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/4/6 22:46
 @File    : new_pengpai.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
import random_ip
import user_agent
from lxml import etree
from bs4 import BeautifulSoup as bs

# url = "https://www.thepaper.cn/channel_25951"
#
# proxies = randomIp.RandomIp().getOneProxies()
# headers = userAgent.UserAgent().getRandomHeaders()
#
# re = requests.get(url, headers=headers, proxies=proxies)
# html = re.text
# with open("re.txt","w",encoding="utf-8") as f:
#     f.write(html)

with open("re.txt","r",encoding="utf-8") as f:
    content = f.read()

soup = bs(content,"html.parser")
aList = soup.find_all("a")
for a in aList:
    print(a.get('href'))
