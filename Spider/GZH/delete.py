"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2018/12/22 21:03
 @File    : delete.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""
import requests
import re
import os


def request(url):
    req = requests.get(url)
    HTML = req.text
    with open("F:\\a.html", "w+", encoding="utf-8") as f:
        f.write(HTML)


def replaceImg():
    path = "F:\\img"
    pathList = os.listdir(path)
    pathList.sort(key=lambda x: int(x.split(".")[0]))  # 顺序读取

    with open("F:\\a.html", "r+", encoding="utf-8") as f:
        html = f.read()
        pattern = r'<img .*?/>'
        imgre = re.compile(pattern)
        imglist = re.findall(imgre, html)

        for img,path in zip(imglist,pathList):
            a=img.split(" />")
            b="F:\\img\\"+path
            new=a[0]+"src="+"\""+b+"\"" + " />"
            if html.__contains__(img):
                c=html.replace(img,new)
                html=c
    return html

def write2HTML(html):
    with open("F:\\b.html", "w+", encoding="utf-8") as f:
        f.write(html)


if __name__ == '__main__':
    # 下载HTML文件
    url = "https://mp.weixin.qq.com/s?timestamp=1546254005&src=3&ver=1&signature=64KOvajKkM5b-oRNW0N-Foy2OKtwxDVyV58DiofRbumRAlLgMdKssCvwMw*htwxliMjBveSD3ATjXrL1IOV4DoMgoX261NC*lK0*5lztLB0P7k1DZRwsibekTLRXQPDtGwegLs-O0CCVnmCxyxbceEeqTKNwfcGMjlNZD*8pDlc="
    result=request(url)

    # # 替换图片
    # html = replaceImg()
    # write2HTML(html)