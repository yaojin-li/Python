"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/10/27 10:57
 @File    : downHistoryBooks.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
from lxml import etree
from comConfig import user_agent
import time


def get_book_urls(url):
    time.sleep(2)
    content = requests.get(url=url, headers=user_agent.UserAgent().get_headers())
    return str(content.text)


if __name__ == '__main__':
    base_url = "http://www.shicimingju.com"
    website_url = "http://www.shicimingju.com/book/"
    book_urls = get_book_urls(website_url)

    struct = etree.HTML(book_urls)
    books_list = struct.xpath('//*[@class="bookmark-list"]/ul/li/h2/a/@href')
    books_name = struct.xpath('//*[@class="bookmark-list"]/ul/li/h2/a/text()')

    # 1. 所有书列表
    print("共 {} 本。".format(len(books_list)))

    book_dict = dict(zip(books_list, books_name))

    for url in book_dict.keys():
        name = book_dict.get(url)
        with open(name + ".txt", "w", encoding="utf-8") as f:
            # 2. 每本书的目录
            book_html = get_book_urls(base_url + url)
            struct = etree.HTML(book_html)

            # 书的章节数
            book_content = struct.xpath('//*[@class="book-mulu"]/ul/li/a/@href')

            for content in book_content[:1]:
                # 3. 每一章节的内容
                one_book = get_book_urls(base_url + content)
                struct = etree.HTML(one_book)

                # 章节名
                book_name = struct.xpath('//*/h1/text()')
                # 每章内容
                book_content = struct.xpath('//*[@class="chapter_content"]/p/text()')

                f.write(str(book_name))

                for content in book_content:
                    f.write(content)
