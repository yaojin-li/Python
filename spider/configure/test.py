"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 
 --------------------------------------
 @File        : test.py
 @Time        : 2019/3/3 10:00
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import requests
from bs4 import BeautifulSoup as bs
req = requests.get("https://www.xicidaili.com/nn/")
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
urls = ["https://www.xicidaili.com/nn/1"]
# 获取ip加入到队列
def get_ips():
    pool = []

    for url in urls:
        res = requests.get(url,headers=headers)
        # print(res.text)
        soup = bs(res.text, "lxml")
        ips = soup.find_all("tr")
        for i in range(1, len(ips) - 50):
            ip = ips[i]
            tds = ip.find_all("td")
            ip_temp = str(tds[5].contents[0]).lower() + "://" + tds[1].contents[0] + ":" + tds[2].contents[
                0]
            speed = float(tds[6].div.get("title")[:-1])
            connectTime = float(str(tds[7].div.get("title"))[:-1])
            print(speed)
            if speed < 0.5 and connectTime < 0.5:
                pool.append(ip_temp)
    return pool

def get_ip():
    pool = []

    for url in urls:
        res = requests.get(url,headers=headers)
        # print(res.text)
        soup = bs(res.text, "lxml")
        ips = soup.find_all("tr")
        for i in range(1, len(ips) - 50):
            ip = ips[i]
            tds = ip.find_all("td")
            ip_temp = str(tds[5].contents[0]).lower() + "://" + tds[1].contents[0] + ":" + tds[2].contents[
                0]
            pool.append(ip_temp)
    return pool

print(get_ips())
# import configure.userAgent as userAgent
# print(userAgent.UserAgent().getRandomHeaders())