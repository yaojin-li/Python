"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 
 --------------------------------------
 @File        : randomIp.py
 @Time        : 2019/1/2 23:22
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import requests
from lxml import etree
import configure.userAgent as userAgent
import logging
import random
import traceback

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class RandomIp():
    def __init__(self):
        self.XICI_URL = "https://www.xicidaili.com/nn/"
        self.BAIDU_URL = "https://www.baidu.com/"
        self.MAX_PAGE_OF_XICI = 3614
        self.NUM_OF_PAGES = 3
        # 获取随机的headers
        self.headers = userAgent.UserAgent.getRandomHeaders

    def getIpPool(self):
        """
        获取IP池
        :return:
        """
        resultIpPool = []
        maxPage = self.MAX_PAGE_OF_XICI
        # 获取随机的3页
        targetPage = random.sample(range(1, maxPage), self.NUM_OF_PAGES)
        for onePage in targetPage:
            req = requests.get(self.XICI_URL + str(onePage))
            logging.info(self.XICI_URL + str(onePage))
            req.encoding = "utf-8"
            if (req.status_code == 200):
                struct = etree.HTML(req.text)
                # 遍历当页的每条记录
                for i in range(1, 101):
                    try:
                        ipXpath = '//*[@id="ip_list"]/tbody/tr[' + str(i) + ']/td[2]/text()'
                        speedXpath = '//*[@id="ip_list"]/tbody/tr[' + str(i) + ']/td[7]/div@title'
                        connectTimeXpath = '//*[@id="ip_list"]/tbody/tr[' + str(i) + ']/td[8]/div@title'
                        ip = struct.xpath(ipXpath)
                        speed = struct.xpath(speedXpath)
                        connectTime = struct.xpath(connectTimeXpath)
                        # 爬取每一页经过筛选的IP
                        if (speed < 0.5 and connectTime < 0.5):
                            resultIpPool.append(ip)
                    except Exception as e:
                        logging.error("解析IP参数异常！")
                        traceback.format_exc(e)
            else:
                logging.error("连接异常！异常url: ", self.MAX_PAGE_OF_XICI + onePage)
        return resultIpPool

    def reviewIp(self):
        """
        重新验证IP池
        :return: ipPool
        """
        ipPool = self.getIpPool()
        try:
            for ip in ipPool:
                proxy = {"http": ip}
                req = requests.get(self.BAIDU_URL, proxy=proxy, headers=self.headers)
                if req.status_code != 200:
                    ipPool.remove(ip)
            return ipPool
        except Exception as e:
            logging.error("reviewIp error, ip:" + str(e))
            traceback.format_exc(e)


if __name__ == '__main__':
    randomIp = RandomIp()
    ipPool = randomIp.reviewIp()
    logging.info("ipPool is:" + str(ipPool))
