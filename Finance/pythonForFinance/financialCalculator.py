"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 金融计算器
 --------------------------------------
 @File        : financialCalculator.py
 @Time        : 2018/10/29 20:42
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""


def fv(fv, r, n):
    '''
    计算未来现金的现值
    :param fv: 未来获取的现金量
    :param r: 每期折现率
    :param n: 周期数（时间）
    :return: 现值
    '''
    return fv / (1+r)**n


def pv_perpetuity(c, r):
    '''
    计算永久年金（假设第一次现金流发生在第一期的结尾）
    :param c: 每一期期末未支付的等额现金
    :param r: 每一期的折现率
    :return: 永久年金
    '''
    return c/r


def pv_growing(c, g, r):
    '''
    计算增长型永久年金
    :param c: 每一期期末未支付的等额现金
    :param g: 增长率
    :param r: 每一期的折现率
    :return: 增长型永久年金
    '''
    return c / (r - g)


def pv_regularAnnuity(pmt, r, n):
    '''
    计算定期年金的现值
    :param pmt: 每期的付款项
    :param r: 每期折现率
    :param n: 周期数（时间）
    :return: 定期年金的现值
    '''
    return pmt * (1 - 1 / (1 + r)**n) / r


def pv_growingAnnuity(pmt, r, g, n):
    '''
    计算增长型年金的现值
    :param pmt: 每期的付款项
    :param r: 每期折现率
    :param g: 增长率
    :param n: 周期数（时间）
    :return: 增长型年金的现值
    '''
    return pmt * (1 - ((1 + g)/(1 + r))**n ) / (r - g)


def fv_regularAnnuity(pmt, r, n):
    '''
    计算定期年金的未来值
    :param pmt: 每期的付款项
    :param r: 每期折现率
    :param n: 周期数（时间）
    :return: 定期年金的未来值
    '''
    return pmt * ((1 + r)**n - 1)


def fv_growingAnnuity(pmt, r, g, n):
    '''
    计算增长型年金的未来值
    :param pmt: 每期的付款项
    :param r: 每期折现率
    :param g: 增长率
    :param n: 周期数（时间）
    :return: 增长型年金的未来值
    '''
    return pmt * ((1 + r)**n - (1 + g)**n) / (r - g)


if __name__ == '__main__':
    print(fv(100, 0.1, 1))
