"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 经典量化交易策略之羊驼策略
 基本概念：
    每天卖掉持有的股票中收益率最差的一只，然后让羊驼随机选入一只股票来买

 基本原理：
    对股票池中的所有股票，每天按照收益率从小到大进行排序，
    起始时买入num_of_stocks只股票，然后每天在整个股票池中选出收益率前num_of_stocks，
    如果这些股票未持有则买入，已持有，则继续持有，并把收益率不是排在前num_of_stocks的股票卖掉。

 策略实现：
　　初始资金：20万元
　　投资域：沪深300股票池
　　回测频率 ：按日回测
　　回测时间段 ：2012年1月2日至2015年10月8日(和股票上市实际时间段的交集 )

 每天持有收益率前n选股流程：
　　1.设置策略参数，初始买入的股票数num_of_stocks，收益率计算所用天数period，其中收益率=昨天的收盘价/period天之前的收盘价。
　　2.将股票池内的股票按照收益率排序，买入收益率最高的num_of_stocks只股票。
　　3.之后的每天都将所有股票按收益率排序，如果股票池中有处于收益率前num_of_stocks而未持有的则买入，并卖掉收益率不处于前num_of_stocks的

 注：在本策略中，如果遇到选中的股票停牌导致无法卖出/买入，当天不卖出/不买入此股票，在第二天多卖一只/多买一只
 --------------------------------
 @Time    : 2018/11/22 21:11
 @File    : quantitativeTradingForAlpaca.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import random
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import scipy.stats as stats
import math
from jqdatasdk import *
auth(15021952809, 952809)

## 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # True为开启动态复权模式，使用真实价格交易
    set_option('use_real_price', True)
    # 设定成交量比例
    set_option('order_volume_ratio', 1)
    # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001,
                             open_commission=0.0003, close_commission=0.0003,
                             close_today_commission=0, min_commission=5), type='stock')
    # 持仓数量
    g.stocknum = 3
    # 交易日计时器
    g.days = 0
    # 调仓频率
    g.refresh_rate = 5
    # 运行函数
    run_daily(trade, 'every_bar')


## 选出小市值股票
def check_stocks(context):
    # 设定查询条件
    q = query(
        valuation.code,
        valuation.market_cap
    ).filter(
        valuation.market_cap.between(20, 30)
    ).order_by(
        valuation.market_cap.asc()
    )

    # 选出低市值的股票，构成buylist
    df = get_fundamentals(q)
    buylist = list(df['code'])

    # 过滤停牌股票
    buylist = filter_paused_stock(buylist)

    return buylist[:g.stocknum]


## 交易函数
def trade(context):
    if g.days % g.refresh_rate == 0:

        ## 获取持仓列表
        sell_list = list(context.portfolio.positions.keys())
        # 如果有持仓，则卖出
        if len(sell_list) > 0:
            for stock in sell_list:
                order_target_value(stock, 0)

        ## 分配资金
        if len(context.portfolio.positions) < g.stocknum:
            Num = g.stocknum - len(context.portfolio.positions)
            Cash = context.portfolio.cash / Num
        else:
            Cash = 0

        ## 选股
        stock_list = check_stocks(context)

        ## 买入股票
        for stock in stock_list:
            if len(context.portfolio.positions.keys()) < g.stocknum:
                order_value(stock, Cash)

        # 天计数加一
        g.days = 1
    else:
        g.days += 1


# 过滤停牌股票
def filter_paused_stock(stock_list):
    current_data = get_current_data()
    return [stock for stock in stock_list if not current_data[stock].paused]


