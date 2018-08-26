"""
 !/usr/bin/python3
 -*- coding: utf-8 -*-
 --------------------------------------
 @File    	  : getURLContent.py
 @Time    	  : 2018/8/26 16:10
 @Software	  : PyCharm
 --------------------------------------
 @Description :
 --------------------------------------
 @Author  	  : lixj
 @Email	  	  : lixj_zj@163.com

"""


import requests
from lxml import etree
import random
from time import sleep
from selenium import webdriver


def getHTMLText(url):
    driver = webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs')  # phantomjs的绝对路径
    driver.set_page_load_timeout(5)
    time.sleep(2)
    driver.get(url)  # 获取网页
    time.sleep(2)
    return driver.page_source


def getContent(headers, html):
    print(html)

    # options = webdriver.ChromeOptions()
    #
    # options.add_argument('--headless')
    #
    # driver = webdriver.Chrome(options =options)
    # driver.get(url)
    # print(url)
    # print(driver.page_source)




if __name__ == '__main__':
    headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
    id_list = ['281239195']

    url = "http://localhost:92/zx/cont.html?id=" + id_list[0] + "&type=jrtt"
    html = getHTMLText(url)
    getContent(headers, html)






