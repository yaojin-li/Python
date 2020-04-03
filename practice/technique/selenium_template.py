"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/7/20 15:03
 @File    : selenium_template.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

from selenium import webdriver
from comConfig.user_agent import UserAgent
from comConfig.random_ip import RandomIp


class SeleniumTemp:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        # 指定 chromedriver.exe 文件路径
        self.executable_path = "D:\ZX_workspace\Python\otherfiles\chromedriver\chromedriver.exe"

    def selenium_operate(self):
        """
        加载 chrome driver，每次加载时更新 IP 与 useragent
        :return: driver
        """
        # 有代理 IP 时加载
        # self.chrome_options.add_argument('--proxy-server=http://{}'.format(RandomIp().get_one_ip()))
        self.chrome_options.add_argument('--user-agent=' + UserAgent().get_user_agent())
        return webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)

    def get_page_source(self, driver, url):
        """
        获取页面全部内容
        :param driver:
        :param url:
        :return:
        """
        driver.get(url)
        return driver.page_source

if __name__ == '__main__':
    url = "http://exam.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk=8E0DEB6C9FC3F295E053D651A8C05FCD"
    selenium_temp = SeleniumTemp()
    driver = selenium_temp.selenium_operate()
    data = selenium_temp.get_page_source(driver, url)
    print(data)
