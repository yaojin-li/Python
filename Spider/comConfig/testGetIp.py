"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/4/6 17:49
 @File    : testGetIp.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import randomIp
import user_agent

# 文件中写入IP
randomIp.RandomIp().reviewIp()

# 获取随机一个IP
# randomIp.RandomIp().getOneIp()

# 获取随机一个prop
# randomIp.RandomIp().getOneProxies()

# 获取随机的多个IP
# randomIp.RandomIp().getNumOfIp(5)

# 获取随机userAgent
# userAgent.UserAgent().getRandomUserAgent()

# 获取随机headers
# userAgent.UserAgent().getRandomHeaders()
