# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   get_html_new
   Description:
   Author:      tebon
   Date:        2018/8/13
-------------------------------------------------
   Change Activity: 2018/8/13
-------------------------------------------------
"""
__author__ = 'tebon'


import requests
from lxml import etree
import random
import time
from selenium import webdriver
from multiprocessing import Pool
import pymysql

def getHTMLText(url):
    driver = webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs')  # phantomjs的绝对路径
    driver.set_page_load_timeout(1)
    time.sleep(1)
    driver.get(url)  # 获取网页
    time.sleep(1)
    return driver.page_source

def getContent(headers, html):
    struct = etree.HTML(html)
    # title = struct.xpath('/html/body/section/div[1]/h1/text()')
    content = struct.xpath('/html/body/section/div[2]/p/text()')
    # time = struct.xpath('/html/body/section/div[1]/p/span[2]/text()')
    # source = struct.xpath('/html/body/section/div[1]/p/span[1]/text()')
    # return title, content, time, source
    return content

# def write2file(title, content, time, source):
#     conn = pymysql.connect(host="localhost", user='root', password='123456789', database = 'news', charset='utf8')
#     print(conn)
#     cursor = conn.cursor();
#     cursor.execute("SELECT * FROM info")
#     data = cursor.fetchone()
#     print(data)
    # with open("./content.txt", "a+", encoding = "utf-8") as f:
    #     f.write(''.join(title))
    #     f.write('\n')
    #     f.write(''.join(content))
    #     f.write('\n\n')



def write2mysql(num, content):
    conn = pymysql.connect(host="localhost", user='root', password='123456789', database = 'news', charset='utf8')
    cursor = conn.cursor();
    sql = "UPDATE docList SET content = '%s' WHERE news_id = %s" % (content[0], num)
    print(sql)
    pass
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        print("error: write to mysql! ")
        conn.rollback()

def run(num):
    url = "http://localhost:92/zx/cont.html?id=" + str(num) + "&type=jrtt&flags=null"
    html = getHTMLText(url)
    content = getContent(headers, html)
    write2mysql(str(num), content)


def get_news_id():
    conn = pymysql.connect(host="localhost", user='root', password='123456789', database = 'news', charset='utf8')
    cursor = conn.cursor();
    sql = "SELECT news_id FROM docList"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        list = []
        for one in result:
            list.append(one[0])

        for newsid in list[38:39]:
            run(newsid)

    except:
        print("错误！")
        conn.rollback()




if __name__ == '__main__':
    headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }

    get_news_id()





    # beginNum = 281189000
    # endNum = 281189001
    # beginTime = time.time()
    #
    # pool = Pool(4)
    # for num in range(beginNum, endNum):
    #     try:
    #         pool.map(run, run(num))
    #         pool.close()  # 关闭进程池，不再接受新的进程
    #         pool.join()  # 主进程阻塞等待子进程的退出
    #     except:
    #         pass
    #     continue
    # endTime = time.time()
    # usedTime = endTime - beginTime
    # print(usedTime)



