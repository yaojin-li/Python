"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 下载图片
 --------------------------------------
 @File        : downDocPng.py
 @Time        : 2018/10/2 14:08
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

from selenium import webdriver
from lxml import etree
import requests
import time


def downOnePng(driver, url, i):
    # 获取页面全部内容
    driver.get(url)
    data = driver.page_source

    struct = etree.HTML(data)
    png = struct.xpath("//*[@id='main']/div[3]/div[2]/p/img/@src")
    url = "http://m.360docs.net" + png[0]
    print(url)

    img = requests.get(url)
    with open("C:\\Users\\lenovo\\Desktop\\png\\" + str(i) + ".png", "wb") as f:
        f.write(img.content)
    time.sleep(2)

if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path="../otherfiles/chromedriver/chromedriver.exe")

    url_base = "http://m.360docs.net/doc/info-eef589567ed5360cba1aa8114431b90d6c85892d"

    for i in range(2, 95):
        url = url_base + "-" + str(i) + ".html"
        downOnePng(driver, url, i)


