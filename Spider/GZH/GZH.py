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
import user_agent
import time
import uuid

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def get_random_ip():
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


def download_img(img_link_list, img_path):
    """
    下载所有图片
    :param img_link_list:
    :param img_path:
    :return:
    """
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    os.chdir(img_path)  # 切换下载图片的目录
    for imgNum, imgLink in enumerate(img_link_list):
        img = requests.get(imgLink, headers=headers, proxies=proxies)
        suffix = imgLink.split("=")[-1]
        try:
            with open(str(imgNum) + "." + suffix, "wb") as f:
                f.write(img.content)
                logging.info("Download {imgNum} th img succeed!".format(imgNum=str(imgNum)))
        except Exception as e:
            logging.error(str(e))


def get_img_link(url):
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
        img_link_list = struct.xpath(xPath)
        logging.info("get img link list succeed!")
        return img_link_list
    except Exception as e:
        logging.error(str(e))


def download_html(url, html_path):
    """
    下载html页面，命名为文章名.html
    :param url:
    :param html_path:
    :return:
    """
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    os.chdir(html_path)  # 切换根目录
    try:
        req = requests.get(url, headers=headers, proxies=proxies)
        struct = etree.HTML(req.text)
        xPath = "//h2/text()"
        title = struct.xpath(xPath)
        html_name = title[0].replace("\\n", "").strip()
        with open(html_name + ".html", "w+", encoding="utf-8") as f:
            f.write(req.text)
        logging.info("download old html succeed!")
        return html_name
    except Exception as e:
        logging.error(str(e))


def img_replaced(html_path, html_name, img_path):
    """
    导入图片
    :param html_path:
    :param html_name:
    :param img_path:
    :return:
    """
    path_list = os.listdir(img_path)
    path_list.sort(key=lambda x: int(x.split(".")[0]))  # 顺序读取
    os.chdir(html_path)
    with open(html_name + ".html", "r+", encoding="utf-8") as f:
        html = f.read()
        pattern = r'<img .*?/>'
        img_re = re.compile(pattern)
        img_list = re.findall(img_re, html)

        for img, path in zip(img_list, path_list):
            img_tag_list = img.split(" />")
            full_img_path = img_path + "\\" + path
            new_img_tag = img_tag_list[0] + "src=" + "\"" + full_img_path + "\"" + " />"
            if html.__contains__(img):
                new_html = html.replace(img, new_img_tag)
                html = new_html
    logging.info("replaced img succeed!")
    return html


def deleted_file(path, html_name):
    """
    删除指定文件
    :param path:
    :param html_name:
    :return:
    """
    try:
        os.remove(path + os.path.altsep + html_name + ".html")
        logging.info("remove file {html_name}.html done!".format(html_name=html_name))
    except Exception as e:
        logging.error(str(e))


def combined_img(html_path, html, html_name):
    """
    重写文件中的图片，生成新的html
    :param html_path:
    :param html:
    :param html_name:
    :return:
    """
    os.chdir(html_path)
    try:
        # 直接覆盖原来没有图片的文件
        with open(html_name + ".html", "w+", encoding="utf-8") as f:
            f.write(html)
        logging.info("combined img to new html succeed!")
    except Exception as e:
        logging.error(str(e))


def named_generator():
    """
    获取唯一命名
    :return:
    """
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + "_" + str(uuid.uuid4())


def run(url):
    # 定义常量
    root_path = os.path.dirname(__file__) + os.path.altsep + "GZH" + os.path.altsep + named_generator()
    img_path = root_path + os.path.altsep + "img"

    # 下载HTML文件
    html_name = download_html(url, root_path)

    # 下载图片
    img_list = get_img_link(url)
    download_img(img_list, img_path)

    # 替换图片写入新的HTML
    img_replaced_html = img_replaced(root_path, html_name, img_path)
    combined_img(root_path, img_replaced_html, html_name)


if __name__ == '__main__':
    global proxies, headers
    headers = user_agent.UserAgent().get_headers()
    # 随机IP
    proxies = get_random_ip()

    url = "https://mp.weixin.qq.com/s?__biz=MjM5NjQ1MTkyMA==&mid=2653814260&idx=1&sn=c82f1695df73ef0dfe76db6a2b2ce1f5&chksm=bd305ecb8a47d7dd64135991ac765723693161c4248b9efde8c15e4651094d7ac9146636c051&scene=0&xtrack=1#rd"

    run(url)
