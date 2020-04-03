"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
    给定一个按非递减顺序排序的整数数组 A，返回每个数字的平方组成的新数组，要求也按非递减顺序排序。

    示例 1：
    输入：[-4,-1,0,3,10]
    输出：[0,1,9,16,100]

    示例 2：
    输入：[-7,-3,2,3,11]
    输出：[4,9,9,49,121]

    提示：
    1 <= A.length <= 10000
    -10000 <= A[i] <= 10000
    A 已按非递减顺序排序。
 --------------------------------
 @Time    : 2019/4/19 23:14
 @File    : 977.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class Solution:
    def sortedSquaresOne(self, A):
        """
        sorted()
        时间复杂度：O(N logN)，其中 N 是数组 A 的长度。
        空间复杂度：O(N)。
        :param A:
        :return:
        """
        return sorted(i ** 2 for i in A)  # sorted()与list.sort()的区别

    def sortedSquaresTwo(self, A):
        """
        左右双指针，从中间分界位置往两边移动
        时间复杂度：O(N)，其中 N 是数组 A 的长度。
        空间复杂度：O(N)。
        :param A:
        :return:
        """
        length = len(A)
        right = 0  # 正向读取非负数部分
        # 找到正负数的分界位置
        while right < length and A[right] < 0:
            right += 1
        left = right - 1  # 反向读取负数部分
        result = []

        # 当左右指针均有指向时
        while left >= 0 and right < length:  # left >= 0    right < length
            # 比较指针对应位置元素平方的大小，result中添加较小的值，并将对应的左右指针往头尾移动
            if A[left] ** 2 > A[right] ** 2:
                result.append(A[right] ** 2)
                right += 1
            else:
                result.append(A[left] ** 2)
                left -= 1
        # 其中一个指针移动到端点时，另一个指针仍指向数据，则在result中添加余下的数据，同时移动指针
        while left >= 0:
            result.append(A[left] ** 2)
            left -= 1
        while right < length:
            result.append(A[right] ** 2)
            right += 1
        return result

    def sortedSquaresThree(self, A):
        """
        左右双指针，从两边位置往中间移动
        :param A:
        :return:
        """
        left = 0
        right = len(A) - 1
        nowIndex = len(A) - 1
        result = [0] * len(A)  # 构建元素为0，个数为len(A)的列表，后续判断中替换元素
        while left <= right:
            if A[left] ** 2 < A[right] ** 2:
                result[nowIndex] = A[right] ** 2  # 替换对应位置的元素
                nowIndex -= 1  # 当前索引自减
                right -= 1  # 右指针往中间移动
            else:
                result[nowIndex] = A[left] ** 2
                nowIndex -= 1
                left += 1  # 左指针往中间移动
        return result


list = [-4, -1, 0, 3, 10]
# print(Solution().sortedSquaresOne(list))
# print(Solution().sortedSquaresTwo(list))
print(Solution().sortedSquaresThree(list))
