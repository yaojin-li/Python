"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
    给定一个二进制矩阵 A，我们想先水平翻转图像，然后反转图像并返回结果。

    水平翻转图片就是将图片的每一行都进行翻转，即逆序。
    例如，水平翻转 [1, 1, 0] 的结果是 [0, 1, 1]。

    反转图片的意思是图片中的 0 全部被 1 替换， 1 全部被 0 替换。例如，反转 [0, 1, 1] 的结果是 [1, 0, 0]。

    示例 1:
    输入: [[1,1,0],[1,0,1],[0,0,0]]
    输出: [[1,0,0],[0,1,0],[1,1,1]]
    解释:
    首先翻转每一行: [[0,1,1],[1,0,1],[0,0,0]]；
    然后反转图片: [[1,0,0],[0,1,0],[1,1,1]]

    示例 2:
    输入: [[1,1,0,0],[1,0,0,1],[0,1,1,1],[1,0,1,0]]
    输出: [[1,1,0,0],[0,1,1,0],[0,0,0,1],[1,0,1,0]]
    解释:
    首先翻转每一行: [[0,0,1,1],[1,0,0,1],[1,1,1,0],[0,1,0,1]]；
    然后反转图片: [[1,1,0,0],[0,1,1,0],[0,0,0,1],[1,0,1,0]]

    说明:
    1 <= A.length = A[0].length <= 20
    0 <= A[i][j] <= 1
 --------------------------------
 @Time    : 2019/4/20 14:33
 @File    : 832.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class Solution:
    def flipAndInvertImageOne(self, A):
        """
        enumerate()遍历
        :param A:
        :return:
        """
        result = []
        for list in A:
            list = list[::-1]
            for key, value in enumerate(list):
                #
                if value == 0:
                    list[key] = 1
                else:
                    list[key] = 0
                # 或者 list[key] = 1 - list[key] 代替if-else判断
            result.append(list)
        return result

    def flipAndInvertImageTwo(self, A):
        """
        ^ 异或运算：相同为1，相异为0
        :param A:
        :return:
        """
        return [[j ^ 1 for j in i[::-1]] for i in A]
        # 或者 j ^ 1 替换成 1 - j

    def flipAndInvertImageThree(self, A):
        """
        头尾数据取反并调换位置
        i[end], i[start] = 1 - i[start], 1 - i[end]
        :param A:
        :return:
        """
        for i in A:
            start = 0
            end = len(i) - 1
            while start <= end:
                i[end], i[start] = 1 - i[start], 1 - i[end]  # ！头尾数据取反并调换位置
                # 或者 i[end], i[start] = 1 ^ i[start], 1 ^ i[end]
                start = start + 1
                end = end - 1
        return A


A = [[1, 1, 0], [1, 0, 1], [0, 0, 0]]
# print(Solution().flipAndInvertImageOne(A))
# print(Solution().flipAndInvertImageTwo(A))
print(Solution().flipAndInvertImageThree(A))
