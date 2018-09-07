"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 多线程爬取网站图片
 --------------------------------------
 @File        : getMeiziImage.py
 @Time        : 2018/8/26 0:23
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool
import sys
from datetime import datetime
import re
import traceback

headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 'Referer': 'http://www.mzitu.com'}
Picreferer = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 'Referer': 'http://i.meizitu.net'}


def request(url):
    try:
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, "lxml")  # beautiful库解析
        return soup
    except:
        print("request请求链接异常！")
        traceback.print_exc()


def get_MaxPage(href):
    try:
        html_soup = request(href)
        max_span = html_soup.find("div", class_="pagenavi").find_all("span")[-2].get_text()  # 获取页数
        return max_span
    except:
        print("获取最大页数异常！")
        traceback.print_exc()

def re2title(string):
    result = re.sub(r'\*|\?|\？|\:|\：|\||\&|\$|\@|\>|\<|\""|\'\'|\“”|\\|\/', "", string)
    return result


def download(all_url, root_path, num):
    try:
        count = 0
        a_soup = request(all_url)
        all_a = a_soup.find("div", class_="all").find_all("a")  # 20180308 11:50 共2693个
        print(len(all_a))
        for a in all_a[1:int(num)]:
            title = a.get_text()
            href = a["href"]  # 获取a标签的链接

            # makdirs
            newTitle = re2title(title)
            path = newTitle.strip()
            os.makedirs(os.path.join(root_path, path))
            os.chdir(root_path + "\\" + path)

            max_span = get_MaxPage(href)

            for page in range(1, int(max_span) + 1):
                page_url = href + "/" + str(page)

                img_soup = request(page_url)

                img_url = img_soup.find("div", class_="main-image").find("img")["src"]
                name = img_url[-9: -4]  # 截取
                img = requests.get(img_url, headers=Picreferer)
                f = open(name + ".jpg", "wb")
                f.write(img.content)
                f.close
            count += 1
            # print("完成：" + title)  多线程时无法执行
            print("完成：" + str(count / (num - 1) * 100) + "%")
    except:
        print("下载异常！")
        traceback.print_exc()


def main():
    all_url = 'http://www.mzitu.com/all'  # 爬取链接入口
    root_path = "E:\\mzitu"  # 本地存储根目录
    num = 4  # 爬取个数-1

    if not os.path.isdir(root_path):
        os.makedirs(root_path)

    start_time = datetime.now()
    print(start_time)

    # 方法1
    download(all_url, root_path, num)

    # 方法2
    '''
    # 线程池个数，电脑CPU个数
    pool = Pool(4)
    for i in range(4):
        pool.apply_async(download, args = (all_url, root_path, num) )  # apply_async非阻塞且支持结果返回进行回调
    pool.close()
    pool.join()
    '''

    end_time = datetime.now()
    print(end_time)
    print("程序耗时：")
    print(end_time - start_time)


if __name__ == "__main__":
    main()

