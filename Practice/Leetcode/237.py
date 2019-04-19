"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
    请编写一个函数，使其可以删除某个链表中给定的（非末尾）节点，你将只被给定要求被删除的节点。
    现有一个链表 -- head = [4,5,1,9]，它可以表示为:
    4->5->1->9

    示例 1:
    输入: head = [4,5,1,9], node = 5
    输出: [4,1,9]
    解释: 给定你链表中值为 5 的第二个节点，那么在调用了你的函数之后，该链表应变为 4 -> 1 -> 9.

    示例 2:
    输入: head = [4,5,1,9], node = 1
    输出: [4,5,9]
    解释: 给定你链表中值为 1 的第三个节点，那么在调用了你的函数之后，该链表应变为 4 -> 5 -> 9.

    说明:
    链表至少包含两个节点。
    链表中所有节点的值都是唯一的。
    给定的节点为非末尾节点并且一定是链表中的一个有效节点。
    不要从你的函数中返回任何结果。

    注：直接把当前要删除的节点的下一个节点的值直接赋值给当前要删除的节点；
    其实删除的是下一个节点，只是把下一个节点的值复制给了当前要删除的节点。
 --------------------------------
 @Time    : 2019/4/19 23:00
 @File    : 237.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def deleteNode(self, node):
        if node.next.next != None:
            node.val = node.next.val    # 执行顺序：先处理值，再移动节点
            node.next = node.next.next
        node.val = node.next.val
        node.next = None
        # 同理可以删除前N个节点。for ()中从node节点处开始删除


node = ListNode(5)
print(Solution().deleteNode(node))
