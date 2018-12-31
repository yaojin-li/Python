"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 1. 爬去文章
 2. 下载图片
 3. 替换图片
 4. 输出pdf
 --------------------------------
 @Time    : 2018/12/21 21:22
 @File    : GZH.py
 @Software: PyCharm
 --------------------------------bnnnnnnnnnnnvb          4
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
from lxml import etree
import logging
import random
import re
import os

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


# 选取随机的IP地址
def getRandomIP():
    with open("ipPool.txt", "r") as f:  # 构建IP池
        content = f.read()
        contList = content.split("', '")
        ipList = contList[1:len(contList) - 1]
        random_ip = random.choice(ipList)
        proxy_ip = "http://" + random_ip
        proxies = {"http": proxy_ip}
    return proxies


def downloadImg(imgLinkList, headers, proxies, imgPath):
    if not os.path.exists(imgPath):
        os.makedirs(imgPath)
    os.chdir(imgPath)  # 切换下载图片的目录
    for imgNum, imgLink in enumerate(imgLinkList):
        img = requests.get(imgLink, headers=headers, proxies=proxies)
        suffix = imgLink.split("=")[-1]
        try:
            with open(str(imgNum) + "." + suffix, "wb") as f:
                f.write(img.content)
                logging.info("Download %s th img succeed!" % str(imgNum))
        except Exception as e:
            logging.error(str(e))


def getImgLinkList(url, headers, proxies):
    req = requests.get(url, headers=headers, proxies=proxies)
    struct = etree.HTML(req.text)
    # 获取所有图片地址
    xPath = "//img/@data-src"  # 匹配任意深度含有data-src熟悉的图片，获取链接
    imgLinkList = struct.xpath(xPath)
    return imgLinkList


def downloadHtml(url, htmlPath, headers, proxies):
    try:
        req = requests.get(url, headers=headers, proxies=proxies)
        struct = etree.HTML(req.text)
        xPath = "//h2/text()"
        title = struct.xpath(xPath)
        htmlName = title[0].replace("\\n", "").strip()
        with open(htmlPath + htmlName + ".html", "w+", encoding="utf-8") as f:
            f.write(req.text)
        return htmlName
    except Exception as e:
        logging.error(str(e))


def replaceImg(htmlPath, htmlName, imgPath):
    pathList = os.listdir(imgPath)
    pathList.sort(key=lambda x: int(x.split(".")[0]))  # 顺序读取

    with open(htmlPath + htmlName + ".html", "r+", encoding="utf-8") as f:
        html = f.read()
        pattern = r'<img .*?/>'
        imgre = re.compile(pattern)
        imglist = re.findall(imgre, html)

        for img, path in zip(imglist, pathList):
            a = img.split(" />")
            b = imgPath + "\\" + path
            new = a[0] + "src=" + "\"" + b + "\"" + " />"
            if html.__contains__(img):
                c = html.replace(img, new)
                html = c
    return html


def writeImgToNewHTML(newHtmlPath, html, htmlName):
    with open(newHtmlPath + htmlName + ".html", "w+", encoding="utf-8") as f:
        f.write(html)


if __name__ == '__main__':
    # 定义常量
    imgPath = "F:\\GZH\\img"
    htmlPath = "F:\\GZH\\"
    newHtmlPath = "F:\\GZH\\"
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    url = "https://mp.weixin.qq.com/s?timestamp=1546254005&src=3&ver=1&signature=64KOvajKkM5b-oRNW0N-Foy2OKtwxDVyV58DiofRbumRAlLgMdKssCvwMw*htwxliMjBveSD3ATjXrL1IOV4DoMgoX261NC*lK0*5lztLB0P7k1DZRwsibekTLRXQPDtGwegLs-O0CCVnmCxyxbceEeqTKNwfcGMjlNZD*8pDlc="

    # 随机IP
    proxies = getRandomIP()

    # 下载HTML文件
    htmlName = downloadHtml(url, htmlPath, headers, proxies)

    # 下载图片
    imgList = getImgLinkList(url, headers, proxies)
    downloadImg(imgList, headers, proxies, imgPath)

    # 替换图片写入新的HTML
    afterReplaceImgHtml = replaceImg(htmlPath, htmlName, imgPath)
    writeImgToNewHTML(newHtmlPath, afterReplaceImgHtml, htmlName)
