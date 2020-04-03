"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 排序算法集合
 1. 插入排序
 2.
 3.
 4.
 --------------------------------
 @Time    : 2019/7/30 21:51
 @File    : SortedAlgorithms.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class SortedAlgorithms(object):
    def __init__(self):
        pass

    def straight_insertion_sort(self, ints):
        """
        直接插入排序
        介绍：
        一种依次将无序区的元素在有序区内找到合适位置依次插入的算法
        基本思想：
        每次从无序表中取出第一个元素，把它插入到有序表的合适位置，使有序表仍然有序，直到无序表内所有元素插入为止
        评价：
        插入排序的最坏时间复杂度为 O(n^2)，属于稳定排序算法，对于处理小批量数据时高效；
        :return: 排序后列表
        """
        for key, value in enumerate(ints):
            # 获取当前值
            current = value
            # 获取当前项前一项
            j = key - 1
            # 若前一项的 key >= 0 并且 前一项的值大于当前值
            while j >= 0 and ints[j] > current:
                # 将前一项的值赋给当前值，即大的值赋给小的值，小的值此时存储为 current
                ints[j + 1] = ints[j]
                # 继续前移一位
                j = j - 1
            # 将当前值（比较后的最小值）赋给当前项
            ints[j + 1] = current
        return ints

    def straight_insertion_sort_optimization(self):
        """
        直接插入排序算法优化--折半查找
        :return:
        """
        pass


if __name__ == '__main__':
    ints = [1, 5, 3, 8, 1, 9, 4, 7, 2]
    algorithms = SortedAlgorithms()

    # 直接插入排序
    print(algorithms.straight_insertion_sort(ints))
