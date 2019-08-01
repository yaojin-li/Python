"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : python 测试用例
 主要使用 python 中的 pytest 框架，在 pycharm 配置搜索 pytest 配置
 --------------------------------
 @Time    : 2019/8/1 22:07
 @File    : test_test_demo.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import pytest
from io import StringIO


def count_vowels_v2(fp):
    """
    统计某个文件中，包含元音字母(aeiou)的数量（普通做法）
    :param fp:
    :return:
    """
    VOWELS_LETTERS = {'a', 'e', 'i', 'o', 'u'}
    count = 0
    for line in fp:
        for char in line:
            if char.lower() in VOWELS_LETTERS:
                count += 1
    return count


@pytest.mark.parametrize(
    "content, vowels_count", [
        # 使用 pytest 提供的参数化测试工具，定义测试参数列表（构造测试用例）
        # (文件内容, 期待结果)
        ('', 0),
        ('Hello World!', 2),
        ('HELLO_WORLD!', 3),
        ('啊哈哈哈', 0),
    ]
)
def test_demo(content, vowels_count):
    # 利用 StirngIO 构建类文件对象 file
    file = StringIO(content)
    assert count_vowels_v2(file) == vowels_count
