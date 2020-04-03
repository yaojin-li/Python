"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 布隆过滤器
 --------------------------------
 @Time    : 2019/9/6 17:16
 @File    : test_bloomfilter.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import mmh3
from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, bit_size):
        # 位向量大小
        self.bit_size = bit_size
        # 构建位向量
        self.bit_array = bitarray(bit_size)
        # 位向量初始化，全部设置为0
        self.bit_array.setall(0)

    def add_data(self, url):
        """
        往布隆过滤器中添加数据，同时将其hash成bitarray，将位向量中与结果集对应的位置至1
        :param url: 添加的 URL
        """
        position_list = self.get_positions(url)
        for position in position_list:
            self.bit_array[position] = 1

    def is_contained(self, url):
        """
        校验布隆过滤器中是否包含某个url
        :param url: 目标URL
        """
        # 获取目标URL对应的多个hash值在位向量中的位置集
        position_list = self.get_positions(url)
        result = True
        # 判断每个位置是否已经被至1
        for position in position_list:
            result = result and self.bit_array[position]
        return result

    def get_positions(self, url):
        """
        返回url经过hash之后的位向量。此处采用三个hash函数构建。
        取余数，保证向量组的比特位索引小于bit_size
        :param url: 需要经过hash的数据
        :return: url所在位向量的位置
        """
        # hash(key, seed=0, signed=True)
        # 参数解释：
        # key: 需要hash的元素
        # seed: 种子参数，随机化函数的一种方法。采用不同的种子参数，生成不同的hash值，防止不同数据的hash冲突
        # signed: 默认True
        # seed 参数解释参考：https://stackoverflow.com/questions/9241230/what-is-murmurhash3-seed-parameter
        position_one = mmh3.hash(url, 60) % self.bit_size
        position_two = mmh3.hash(url, 61) % self.bit_size
        position_three = mmh3.hash(url, 62) % self.bit_size
        return [position_one, position_two, position_three]

if __name__ == '__main__':
    bloom = BloomFilter(100000)
    bloom.add_data('https://www.baidu.com')
    print(bloom.is_contained('https://www.baidu.com'))
    print(bloom.is_contained('test'))
