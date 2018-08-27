"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 获取代理IP
 --------------------------------------
 @File        : get_ip.py
 @Time        : 2018/5/5 13:39
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

"""
1. bs解析页面，将提取到的代理交给队列
2. 通过共享队列分配给线程。
3. 开启线程通过设置代理ip访问一个网站，因为访问网站的时间比较长，因此要开起多个线程

网站：
1. 西刺：http://www.xicidaili.com/nn/
2. 快代理：https://www.kuaidaili.com/free/inha/
"""

import requests
from bs4 import BeautifulSoup as bs
import threading
import queue
import lxml

class get_ip():

    def __init__(self, page):
        self.root_url = "http://www.xicidaili.com/nn/"
        self.ips = []    # ip列表
        self.urls = []   # url列表
        # 获取所有页面存入url列表
        for i in range(1, page):
            self.urls.append(self.root_url + str(i))
        # 请求头
        self.header = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        self.queue = queue.Queue()    # 队列 !!!
        self.lock = threading.Lock()  # 线程锁 !!!

    # 获取ip加入到队列
    def get_ips(self):

        for url in self.urls:
            res = requests.get(url, headers=self.header)
            soup = bs(res.text, "lxml")
            ips = soup.find_all("tr")
            for i in range(1, len(ips)-50):
                ip = ips[i]
                tds = ip.find_all("td")
                ip_temp = str(tds[5].contents[0]).lower() + "://" + tds[1].contents[0] + ":" + tds[2].contents[0]
                self.queue.put(str(ip_temp))

    # 重新审查可用IP
    def review_ips(self):
        while not self.queue.empty():
            ip = self.queue.get()
            try:
                begin_ip = ip.split(":")[0]
                proxy = {begin_ip : ip}
                res = requests.get("http://www.baidu.com", proxies=proxy)

                # 互斥锁，保证共享数据操作的完整性，防止资源被抢占
                self.lock.acquire()     # 线程锁定资源--控制多个线程对同一资源的访问
                if res.status_code == 200:
                    self.ips.append(ip)
                    self.lock.release()

                # 当获取到可用的IP地址为10个的时候，停止验证余下的IP地址
                if len(self.ips) == 10:
                    break
            except:
                continue

    def run(self):
        self.get_ips()
        self.review_ips()
        return self.ips

if __name__ == '__main__':
    get_ip = get_ip(2)
    ip = get_ip.run()
    print(ip)   # 输出十个可用的IP地址
