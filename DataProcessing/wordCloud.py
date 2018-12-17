"""
 !/usr/bin/python3
 -*- coding: utf-8 -*-
 --------------------------------------
 @File    	  : wordCloud.py
 @Time    	  : 2018/8/26 0:37
 @Software	  : PyCharm
 --------------------------------------
 @Description : 
 --------------------------------------
 @Author  	  : lixj
 @Contact  	  : lixj_zj@163.com
 --------------------------------------
"""

# WordCloud + 统计图表
'''
关键点和难点在于：
对于网上用户的评论+文字做分析，提取出关键点作为列表
'''

import os
from pyecharts import WordCloud
from pyecharts import Bar, Pie, Line, Scatter3D
from pyecharts import Page
import random


# 词云图
def wordCloud(x, y, label):
    wordCloud = WordCloud(width=1300, height=620)

    # word_size_ragne限定字体大小范围
    # shape参数用来调整词云形状（'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'）
    wordCloud.add("", x, y, word_size_range=[20, 100], shape="circle")
    wordCloud.render()
    os.system(r"render.html")  # 默认内容输出到根目录


# 统计图表
def get_charts(x, y, label, type):
    if type == 1:
        c = Pie("饼状图")
    elif type == 2:
        c = Bar3D("条形图")
    elif type == 3:
        c = Line("折线图")
    print(c)
    c.add(label, x, y, is_more_utils=True)
    # 打印输出图表的所有配置项
    c.show_config()
    c.render()
    os.system(r"render.html")


# 多个统计图
def get_otherCharts(page):
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 75, 90]
    v2 = [10, 25, 8, 60, 20, 80]
    bar = Bar("柱状图数据堆叠示例")
    bar.add("商家A", attr, v1, is_stack=True)
    bar.add("商家B", attr, v2, is_stack=True)
    page.add(bar)
    page.render()
    os.system(r"render.html")


# Scatter3D
def get_scatter3D(page):
    data = [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)] for _ in range(80)]
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D散点示例", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    page.add(scatter3D)
    page.render()
    os.system(r"render.html")


def main():
    '''
    # 测试词云图
    x = [
        "python", "lxj", "zj", "big data", "python", "lxj", "zj", "big data",
        "python", "lxj", "zj", "big data", "python", "lxj", "zj", "big data"
        ]
    y = [
        10000, 8000, 6000, 3000, 10000, 8000, 6000, 3000,
        10000, 8000, 6000, 3000, 10000, 8000, 6000, 3000
        ]
    label = "词云"
    wordCloud(x, y, label)
    '''

    '''
    # 测试统计图表    
    x = ["衬衫", "袜子", "高跟鞋", "羊毛衫", "裤子"]
    y1 = [5, 10, 38, 75, 90]
    y2 = [15, 4, 70, 25, 190]
    label = "服装"
    type = 2
    get_charts(x, y, label, type)
    '''

    '''
    # 测试多个统计图
    page = Page()
    get_otherCharts(page)
    '''

    # 测试三维散点图
    page = Page()
    get_scatter3D(page)


if __name__ == "__main__":
    main()








