"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 1. 爬取文章
 2. 下载图片
 3. 替换图片
 4. 输出html
 --------------------------------
 @Time    : 2019/5/29 11:54
 @File    : GZH.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
from lxml import etree
import logging
import random
import re
import os
import userAgent
import time
import uuid

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] '
                           '- %(levelname)s: %(message)s')


def getRandomIP():
    """
    获取随机的IP地址
    :return:
    """
    with open("ipPool.txt", "r") as f:  # 构建IP池
        content = f.read()
        contList = content.split("', '")
        ipList = contList[1:len(contList) - 1]
        random_ip = random.choice(ipList)
        proxy_ip = "http://" + random_ip
        proxies = {"http": proxy_ip}
        logging.info("random ip is {}".format(proxies))
    return proxies


def downloadImg(imgLinkList, imgPath):
    """
    下载所有图片
    :param imgLinkList:
    :param imgPath:
    :return:
    """
    if not os.path.exists(imgPath):
        os.makedirs(imgPath)
    os.chdir(imgPath)  # 切换下载图片的目录
    for imgNum, imgLink in enumerate(imgLinkList):
        img = requests.get(imgLink, headers=headers, proxies=proxies)
        suffix = imgLink.split("=")[-1]
        try:
            with open(str(imgNum) + "." + suffix, "wb") as f:
                f.write(img.content)
                logging.info("Download {imgNum} th img succeed!".format(imgNum=str(imgNum)))
        except Exception as e:
            logging.error(str(e))


def getImgLinkList(url):
    """
    获取所有图片链接
    :param url:
    :return:
    """
    try:
        req = requests.get(url, headers=headers, proxies=proxies)
        struct = etree.HTML(req.text)
        # 获取所有图片地址
        xPath = "//img/@data-src"  # 匹配任意深度含有data-src熟悉的图片，获取链接
        imgLinkList = struct.xpath(xPath)
        logging.info("get img link list succeed!")
        return imgLinkList
    except Exception as e:
        logging.error(str(e))


def downloadHtml(url, htmlPath):
    """
    下载html页面，命名为文章名.html
    :param url:
    :param htmlPath:
    :return:
    """
    if not os.path.exists(htmlPath):
        os.makedirs(htmlPath)
    os.chdir(htmlPath)  # 切换根目录
    try:
        req = requests.get(url, headers=headers, proxies=proxies)
        struct = etree.HTML(req.text)
        xPath = "//h2/text()"
        title = struct.xpath(xPath)
        htmlName = title[0].replace("\\n", "").strip()
        with open(htmlName + ".html", "w+", encoding="utf-8") as f:
            f.write(req.text)
        logging.info("download old html succeed!")
        return htmlName
    except Exception as e:
        logging.error(str(e))


def replaceImg(htmlPath, htmlName, imgPath):
    """
    替换图片
    :param htmlPath:
    :param htmlName:
    :param imgPath:
    :return:
    """
    pathList = os.listdir(imgPath)
    pathList.sort(key=lambda x: int(x.split(".")[0]))  # 顺序读取
    os.chdir(htmlPath)
    with open(htmlName + ".html", "r+", encoding="utf-8") as f:
        html = f.read()
        pattern = r'<img .*?/>'
        imgre = re.compile(pattern)
        imglist = re.findall(imgre, html)

        for img, path in zip(imglist, pathList):
            imgTagList = img.split(" />")
            fullImgPath = imgPath + "\\" + path
            newImgTag = imgTagList[0] + "src=" + "\"" + fullImgPath + "\"" + " />"
            if html.__contains__(img):
                newHtml = html.replace(img, newImgTag)
                html = newHtml
    logging.info("replace img succeed!")
    return html


def delFile(path, htmlName):
    """
    删除指定文件
    :param path:
    :param htmlName:
    :return:
    """
    try:
        os.remove(path + os.path.altsep + htmlName + ".html")
        logging.info("remove file {htmlName}.html done!".format(htmlName=htmlName))
    except Exception as e:
        logging.error(str(e))


def writeImgToNewHTML(newHtmlPath, html, htmlName):
    """
    重写文件中的图片，生成新的html
    :param newHtmlPath:
    :param html:
    :param htmlName:
    :return:
    """
    os.chdir(newHtmlPath)
    try:
        # 直接覆盖原来没有图片的文件
        with open(htmlName + ".html", "w+", encoding="utf-8") as f:
            f.write(html)
        logging.info("rewrite img to new html succeed!")
    except Exception as e:
        logging.error(str(e))


def getRandomPathName():
    """
    获取随机数命名文件夹
    :return:
    """
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + "_" + str(uuid.uuid4())


def run(url):
    # 定义常量
    rootPath = os.path.dirname(__file__) + os.path.altsep + "GZH" + os.path.altsep + getRandomPathName()
    imgPath = rootPath + os.path.altsep + "img"

    # 下载HTML文件
    htmlName = downloadHtml(url, rootPath)

    # 下载图片
    imgList = getImgLinkList(url)
    downloadImg(imgList, imgPath)

    # 替换图片写入新的HTML
    afterReplaceImgHtml = replaceImg(rootPath, htmlName, imgPath)
    writeImgToNewHTML(rootPath, afterReplaceImgHtml, htmlName)


if __name__ == '__main__':
    global proxies, headers
    headers = userAgent.UserAgent().getRandomHeaders()
    # 随机IP
    proxies = getRandomIP()

    url = "https://mp.weixin.qq.com/s?__biz=MjM5NjQ1MTkyMA==&mid=2653814260&idx=1&sn=c82f1695df73ef0dfe76db6a2b2ce1f5&chksm=bd305ecb8a47d7dd64135991ac765723693161c4248b9efde8c15e4651094d7ac9146636c051&scene=0&xtrack=1#rd"

    run(url)
