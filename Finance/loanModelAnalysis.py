"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : Analysis of several loan models
 1. 等额本息贷款
 2. 固定点数贷款
 3. 双利率贷款
 --------------------------------------
 @File        : loanModelAnalysis.py
 @Time        : 2018/9/24 16:47
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import matplotlib

matplotlib.rcParams["font.sans-serif"] = ["SimHei"]

# 计算贷款额loan r(月利率) m(还款时间/月)
def findPayment(loan, r, m):
    return loan * ((r * (1 + r) ** m) / ((1 + r) ** m - 1))




