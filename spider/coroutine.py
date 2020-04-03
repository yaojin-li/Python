"""
 !/usr/bin/python3
 -*- coding: utf-8 -*-
 --------------------------------------
 @File    	  : coroutine.py
 @Time    	  : 2018/8/28 21:18
 @Software	  : PyCharm
 --------------------------------------
 @Description : 异步协程提高爬速
 --------------------------------------
 @Author  	  : lixj
 @Email	  	  : lixj_zj@163.com

"""

"""
## 1. 引入包asyncio
import asyncio
import requests

## 2. 自定义方法
async def request():
    url = "https://www.baidu.com"
    status = requests.get(url)
    return status

## 3. 调用方法返回协程对象
coroutine = request()

## 4. 将协程对象封装成task对象（显式声明）
task = asyncio.ensure_future(coroutine)
print(task)

## 5. 创建事件循环loop，将协程注册到事件循环中启动
loop = asyncio.get_event_loop()

loop.run_until_complete(task)
print("task", task)
print("task result:", task.result())
"""

## 1. 引入包asyncio
import asyncio
import time
import aiohttp
from lxml import etree

## 2. 自定义方法
async def getContent(url):
    # ！unclosed client session 错误；The client session supports the context manager protocol for self closing.
    # 此写法不需要session.close() 方法关闭session
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)   # requests换成session
        result = await response.text()
        struct = etree.HTML(result)
        content = struct.xpath("/html/body/div[1]/div[3]/ul/li[1]/div[4]/p/text()")
        return content

## 3. 调用自定义方法返回协程对象
async def request(url):
    result = await getContent(url)
    print(result)

# 创建事件循环loop
def even_loop(url_list):
    ## 4. 将协程对象再封装一层封装成task对象（显式声明）
    tasks = [asyncio.ensure_future(request(url)) for url in url_list]

    ## 5. 创建事件循环loop，将协程注册到事件循环中启动
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

if __name__ == '__main__':
    start = time.time()
    # https://www.guancha.cn/society/2018_08_29_470073.shtml
    url_list = ["url1", "url2", "..."]
    even_loop(url_list)
    print("cost time:", time.time()-start)
