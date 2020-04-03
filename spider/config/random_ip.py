"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 获取随机可以用IP
 --------------------------------
 @Time    : 19-2-28 上午11:28
 @File    : random_ip.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
from bs4 import BeautifulSoup as bs
import user_agent
import logging
import os
import random
import traceback
import time

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class RandomIp():
    def __init__(self):
        self.XICI_URL = "https://www.xicidaili.com/nn/"
        self.TEST_URL = "https://www.jd.com/"
        self.IP_POOL_FILE = "ip_pool.txt"
        self.MAX_PAGE_OF_XICI = 3614  # 西刺网站总页数
        self.NUM_OF_PAGES = 2  # 爬取的目标页数
        # 获取随机的headers
        self.headers = user_agent.UserAgent().get_headers() # userAgent.UserAgent() 类实例化()括号就相当于self参数

    def get_target_pages(self, page):
        """
        获取随机的NUM_OF_PAGES页
        :param page:
        :return:
        """
        return random.sample(range(1, page), self.NUM_OF_PAGES)

    def request_get(self, url):
        """
        requests请求
        :param url:
        :return:
        """
        return requests.get(url, headers=self.headers, timeout=10)

    def analysis_page(self, req):
        result_ip_pool = []
        soup = bs(req.text, "lxml")
        ips = soup.find_all("tr")
        # 遍历当页的每条记录
        for i in range(1, len(ips)):
            try:
                ip = ips[i]
                tds = ip.find_all("td")
                temp_ip = str(tds[5].contents[0]).lower() + '://' + tds[1].contents[0] + ':' + tds[2].contents[0]
                speed = float(tds[6].div.get("title")[:-1])
                connect_time = float(tds[7].div.get("title")[:-1])
                #
                if speed < 0.5 and connect_time < 0.5:
                    result_ip_pool.append(temp_ip)
            except Exception as e:
                logging.error("解析IP参数异常！")
                traceback.format_exc(e)
        return result_ip_pool

    def get_ip_pool(self):
        """
        获取IP池
        :return:
        """
        result_ip_pool = []
        max_page = self.MAX_PAGE_OF_XICI
        # 获取随机的NUM_OF_PAGES页
        target_pages = RandomIp().get_target_pages(max_page)
        for one_page in target_pages:
            one_page_url = self.XICI_URL + str(one_page)
            req = RandomIp().request_get(one_page_url)
            if (req.status_code == 200):
                result_ip_pool.extend(RandomIp().analysis_page(req))
            else:
                logging.error("连接异常！异常url:", one_page_url)
        return result_ip_pool

    def review_ip_pool(self):
        """
        重新验证IP池
        :return: ip_pool
        """
        ip_pool_path = self.IP_POOL_FILE
        try:
            with open(ip_pool_path, "r", encoding="utf-8") as f:
                content = f.read()
            ip_pool = content[2:len(content) - 2].split("', '")
            reduce_num = 0
            logging.info("IP池中待验证个数：{}".format(len(ip_pool)))
            for ip in ip_pool[:]:
                proxy = {ip.split("://")[0]: ip.split("://")[1]}
                try:
                    req = requests.get(self.TEST_URL, proxies=proxy, headers=self.headers, timeout=3)
                    if req.status_code != 200:
                        ip_pool.remove(ip)
                        reduce_num += 1
                    time.sleep(1)
                except Exception as e:
                    logging.error("ip异常：{}，异常信息：{}".format(ip, str(e)))
                    ip_pool.remove(ip)
                    reduce_num += 1
                    continue
            logging.info("IP池中已验证个数：{}，减少个数：{}个".format(len(ip_pool), reduce_num))
            with open(ip_pool_path, "w", encoding="utf-8") as f:
                f.write(str(ip_pool))
            logging.info("IP池已更新！")
        except Exception as e:
            logging.error("重新验证IP池异常！异常信息：{}".format(e))

    def write_ip_to_file(self):
        """
        IP写入文件，追加形式
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            file_name = module_path + '\\' + self.IP_POOL_FILE
            with open(file_name, "a+", encoding="utf-8") as f:
                f.write(str(self.get_ip_pool()))
            logging.info("写入IP {} 个结束！".format(len(self.get_ip_pool())))
        except Exception as e:
            logging.error("IP写入文件异常！异常信息：", e)
            traceback.format_exc(e)

    def get_one_ip(self):
        """
        获取随机的一个IP地址
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            file_name = module_path + '\\' + self.IP_POOL_FILE
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
                ip_list = content[1:len(content) - 1].split(", ")
                random_ip = random.choice(ip_list)  # choice()获取一个
                logging.info("random_ip: %s", random_ip)
            return random_ip
        except Exception as e:
            logging.error("IP读入文件异常！异常信息：", e)
            traceback.format_exc(e)

    def get_one_proxies(self):
        """
        获取随机的一个Proxies
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            file_name = module_path + '\\' + self.IP_POOL_FILE
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
                ip_list = content[2:len(content) - 2].split("', '")
                random_ip = random.choice(ip_list)  # choice()获取一个
                proxies = {"http": random_ip}
                logging.info("proxies: %s", str(proxies))
            return proxies
        except Exception as e:
            logging.error("IP读入文件异常！异常信息：", e)
            traceback.format_exc(e)

    def get_num_of_ip(self, num_of_ip):
        """
        获取指定数量的IP
        :return:
        """
        try:
            module_path = os.path.dirname(__file__)
            file_name = module_path + '\\' + self.IP_POOL_FILE
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
                cont_list = content.split("', '")
                ip_list = cont_list[1:len(cont_list) - 1]
                random_ip_list = random.sample(ip_list, num_of_ip)  # sample()获取多个
                logging.info("random_ip_list: %s", random_ip_list)
            return random_ip_list
        except Exception as e:
            logging.error("IP读入文件异常！异常信息：", e)
            traceback.format_exc(e)


if __name__ == '__main__':
    RandomIp().write_ip_to_file()
    RandomIp().review_ip_pool()


