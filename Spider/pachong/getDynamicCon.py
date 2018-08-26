#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 16:55
# @Author  : lxj1
# @File    : getDynamicCon.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
import time

## 1. 动态抓取页面
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
## 2. 更改user-agent
# chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
# chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')

driver = webdriver.Chrome(chrome_options=chrome_options)
# PhantomJS 目前标记为不赞成，在未来版本中可能不支持，改用chrome的headless chrome
# driver = webdriver.PhantomJS(executable_path="./phantomjs/bin/phantomjs")

url = "https://www.huomao.com/channel/lol"

# 获取页面全部内容
driver.get(url)
data = driver.page_source
print(len(data))

# 获取网页截图
# driver.save_screenshot("./screenshot/1.png")

## 3. 保存爬取内容到本地分析！
with open("./page_source.txt", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()

# ----------------------------------------------------------------------------------------------

## 4. 分析
page_source = ''    # 本地文件内容代替爬取结果str类型
with open("./page_source.txt", "r", encoding="utf-8") as f:
    page_source = f.read()

# 存储最终分析结果
name = []
title = []
watching = []

# 开始解析
soup = bs(page_source, "html.parser")
channelList = soup.find("div", attrs={'id':"channellist"})
rooms = channelList.find_all("div", attrs={'class':"list-smallbox no-logo"})
# 获取每个房间中的主播信息
for room in rooms:
    try:
        this_title = room.find("a")["title"]    # title当作a的属性获取
        this_name = room.find("span", class_="nickname").text   # bs 解析标签中的值
        this_watching = room.find("em", attrs={"class":"flr"}).find("span").text
    except:
        this_watching = room.find("div", class_="no-playing").text
    name.append(this_name)
    title.append(this_title)
    watching.append(this_watching)

result = DataFrame({
    "主播名":name,
    "节目名":title,
    "观看人数":watching
})

result.to_csv("./result.csv", encoding = "utf_8_sig")
