"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/4/6 17:49
 @File    : test_comfig.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import random_ip
import user_agent

# 文件中写入IP
random_ip.RandomIp().write_ip_to_file()

# 重新验证IP
random_ip.RandomIp().review_ip_pool()

# 获取随机一个IP
random_ip.RandomIp().get_one_ip()

# 获取随机一个prop
random_ip.RandomIp().get_one_proxies()

# 获取随机的多个IP
random_ip.RandomIp().get_num_of_ip(5)

# 获取随机userAgent
user_agent.UserAgent().get_user_agent()

# 获取随机headers
user_agent.UserAgent().get_headers()
