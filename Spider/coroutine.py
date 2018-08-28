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

import asyncio
import time
import aiohttp
from lxml import etree

start = time.time()

async def get(url):
    try:
        session = aiohttp.ClientSession()
        response = await session.get(url)
        result = await response.text()
        struct = etree.HTML(result)
        content = struct.xpath("/html/body/div[1]/div[3]/ul/li[1]/div[4]/p/text()")
    except:
        print("出错...")
    finally:
        session.close()
    return content

async def request():
    url = "https://www.guancha.cn/society/2018_08_28_469969.shtml"
    print("waitting for", url)
    result = await get(url)
    print("get response from ", url, "result: ", result)

tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print("cost time:", time.time()-start)
