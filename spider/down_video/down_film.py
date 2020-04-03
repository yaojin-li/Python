"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 下载VIP视频
 --------------------------------------
 @File        : downFilm.py
 @Time        : 2018/8/26 0:28
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

'''
IPO：
input：.ts文件的url、.ts文件的个数 或者 m3u8文件
process：
        初始化配置参数（IP代理网页数，下载路径，视频名称，请求头部参数）
        获得.ts文件的URI列表（包含文件链接地址及文件个数）
        配置代理IP，选取随机IP地址进行文件下载
        下载.ts文件
        合并转换为MP4格式视频 
output：完成的MP4格式的视频

关键点：
1. 网页解析
2. m3u8解析
3. 设置动态代理
4. 调用DOS命令合并文件

难点：
1. 获得m3u8文件
2. 获取.ts文件的URI与个数

重点：
找到视频的m3u8文件（含有.ts文件的URI和个数）

注：
查看m3u8文件与.ts文件的过程：
1. 打开视频页面，审查元素。
2. 采用移动端的方式查看加载过程，即点击页面左上方的手机图标，然后刷新页面。
3. 查找m3u8文件相关的内容。
   若有，则点击查看headers中的request URL，即可下载m3u8文件。若无，则第四步。
4. 查找.ts文件加载内容。
   根据.ts文件加载headers中的request URL，可获得URI地址。
   查看所有的.ts文件的个数，可以通过解析网站，采用同样的方法，将视频快进到结束时，查看.ts文件的个数。
5. 获得m3u8文件或.ts文件的URI与个数任其一，即可下载全部视频。

视频解析网站：
    VIP视频解析：http://www.vipjiexi.com/
    无名小站：http://www.wmxz.wang/
通用解析方式是：
    VIP视频解析： http://www.vipjiexi.com/tong.php?url=[播放地址或视频id] 
    无名小站：http://www.wmxz.wang/video.php?url=[播放地址或视频id]

视频网站中关于管理m3u8文件各不相同：
腾讯非VIP视频在前端页面中可以直接查看，下载后直接获取VIP试看部分的.ts文件。若获得全部的.ts文件个数，可以通过视频解析网站，按第四步操作查看。
爱奇艺在前端页面中需制定特定.ts文件的URI地址，获取URI址与个数。

'''

import requests
from bs4 import BeautifulSoup as bs
import os
import time
import random
import re
import m3u8
import traceback


class VideoDownload():
    def __init__(self):
        self.pageNum = 3  # IP代理网站页数，一页100个IP

        #################### begin 以下路径地址可更改，具体视频的url地址又具体的视频而定 ###################

        # .ts文件的url，针对爱奇艺视频
        self.url = "http://video2.fxsdp.com:8091/81820180315/JAVHD00054/650kb/hls/Vf6Uur2229"

        # m3u8文件的url，针对腾讯视频
        self.TC_m3u8_url = "http://apd-983a0da8026d665ba14276af64267b05.v.smtcdns.com/vipts.tc.qq.com/A8_h69zsltM9kkOROl8Vx-l7g4JU8HQSrV-cE6aZ1uSc/SSXffv8zY6OTtSN-TvdRq_1UPxz2DDoymrbx04tr9kXcEXoqsDS-bUQNxi9ECFzDb0FC6fHlwXnBk3aN__auyD4rLuK7i9-Q7eCTkP8XE0qplasm_4UKUsyok_3nkKpoDIBP4GCk6THrBrsOST0EZxSi55wQO5Fh/0310_a0026o0eqrg.321002.ts.m3u8?ver=4"
        # .ts文件的url，针对腾讯视频
        # 根据此url与m3u8文件中的.ts路径相结合，获取.ts文件下载
        # 此url在网页审查元素 -> network -> 加载.ts文件的headers中获得
        self.TC_ts_url = "https://apd-983a0da8026d665ba14276af64267b05.v.smtcdns.com/vipts.tc.qq.com/A8_h69zsltM9kkOROl8Vx-l7g4JU8HQSrV-cE6aZ1uSc/SSXffv8zY6OTtSN-TvdRq_1UPxz2DDoymrbx04tr9kXcEXoqsDS-bUQNxi9ECFzDb0FC6fHlwXnBk3aN__auyD4rLuK7i9-Q7eCTkP8XE0qplasm_4UKUsyok_3nkKpoDIBP4GCk6THrBrsOST0EZxSi55wQO5Fh/"

        # 路径名称 “ \\ ”，绝对路径
        self.m3u8Path = "E:\\delete\\temp.m3u8"  # m3u8文件的暂存路径
        self.download_path = "E:\\delete\\DOWN"  # .ts文件下载路径
        self.final_path = "E:\\delete\\FINAL"  # 最终合并视频的路径
        self.name = "resultFilmName"  # 最终合并视频的名称

        #################### end 以上路径地址可更改，具体视频的url地址又具体的视频而定 ###################

        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }

    # 获得.ts文件的URI信息（针对爱奇艺中的视频，需要手动处理）
    def getURIList(self):
        uri_list = []
        for i in range(1, 1742):  ####################################     .ts文件的具体个数可在视频解析网站查看后确定
            if i < 10:
                uri_list.append(self.url + "00" + str(i) + ".ts")
            elif i > 100:
                uri_list.append(self.url + str(i) + ".ts")
            else:
                uri_list.append(self.url + "0" + str(i) + ".ts")
        return uri_list

    # 获得m3u8文件并解析（针对腾讯视频，可以直接获取m3u8文件）
    def get_m3u8_uri(self):
        # 开始获取m3u8文件
        m3u8Content = requests.get(self.TC_m3u8_url)
        try:
            with open(self.m3u8Path, "w") as f:
                f.write(m3u8Content.text)
            # 开始解析m3u8文件
            uri_list = []
            m3u8Cont = open(self.m3u8Path, "r")
            for line in m3u8Cont.readlines():
                if ".ts" in line:  # 提取出含有.ts的一行，作为HTTP请求尾部
                    uri_list.append(self.TC_ts_url + line.strip())
                else:
                    continue
            return uri_list
        except:
            traceback.print_exception

    # 获取代理IP网址
    def getIPList(self):
        print("获取代理IP...")
        url = 'http://www.xicidaili.com/nn/'
        ipList = []
        for i in range(self.pageNum):
            newurl = url + str(i + 1)  # 从第一个页面开始
            r = requests.get(newurl, headers=self.headers)
            soup = bs(r.text, "html.parser")
            ips = soup.find_all("tr")
            for i in range(1, len(ips)):  # 第0个为头信息获取时出现索引异常，从1开始
                ipInfo = ips[i]
                tds = ipInfo.find_all("td")
                ipList.append(tds[1].string + ":" + tds[2].string)
        return ipList

    # 选取随机的IP地址
    def getRandomIP(self, ipList):
        random_ip = random.choice(ipList)
        proxy_ip = "http://" + random_ip
        proxies = {"http": proxy_ip}
        return proxies

    # 下载
    def downloadFilm(self):
        print("开始下载...")
        start_time = time.time()
        os.chdir(self.download_path)  # 更改下载文件的执行路径，即在该路径下下载文件
        ip_list = self.getIPList()
        proxies = self.getRandomIP(ip_list)

        uri_list = self.getURIList()  # 爱奇艺视频
        # uri_list = self.get_m3u8_uri()  # 腾讯视频
        print(uri_list[:3])

        num = 1  # 操作文件的个数
        for uri in uri_list[:10]:
            if num % 5 == 0:
                print("更换代理IP")
                proxies = self.getRandomIP(ip_list)
            if num % 60 == 0:
                print("休眠10s")
                time.sleep(10)
            try:
                resp = requests.get(uri, headers=self.headers,
                                    proxies=proxies)  # 存在有些网站不支持代理IP， 去掉proxies设置(proxies = proxies)
            except:
                traceback.print_exception()
            if num < 10:
                name = ('clip00%d.ts' % num)
            elif num > 100:
                name = ('clip%d.ts' % num)
            else:
                name = ('clip0%d.ts' % num)
            with open(name, "wb") as f:
                f.write(resp.content)
                print("正在下载clip%d" % num)
            num = num + 1
        print("下载完成！总共耗时 %0.3f min " % float((time.time() - start_time) / 60.0))

    # 合并
    def mergeFilm(self):
        mess = input("是否进行电影合并？（y/n）")
        if mess == "y":
            try:
                os.chdir(self.download_path)  # 更改合并文件的执行路径，即在该路径下进行DOS命令操作
                allFile = ''
                for file in os.listdir(self.download_path):
                    allFile = allFile + "+" + file
                allFileName = allFile[1:]
                # 合并所有.ts文件名，通过DOS命令进行文件合并
                command = "copy /b " + allFileName + " /y %s\%s.mp4" % (self.final_path, self.name)  # DOS语法，路径为“\”
                os.system(command)
                print("合并完成...")
            except:
                traceback.print_exception()
        else:
            print("不合并电影，程序退出。")


if __name__ == "__main__":
    videoDownload = VideoDownload()
    videoDownload.downloadFilm()
    # videoDownload.mergeFilm()

