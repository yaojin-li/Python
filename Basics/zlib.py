"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 压缩解压
 --------------------------------------
 @File    	  : zlib.py
 @Time    	  : 2018/8/25 22:10
 @Software	  : PyCharm
 --------------------------------------
 @Author  	  : lixj
 @Contact	  : lixj_zj@163.com
 --------------------------------------
"""

import zlib
import requests


# zlib.compress 用来压缩字符串的bytes类型
def str_zlib():
    req = requests.get("http://python.jobbole.com/81513/")
    message = req.text
    bytes_message = str.encode(message)
    compressed = zlib.compress(bytes_message, zlib.Z_BEST_COMPRESSION)
    decompressed = zlib.decompress(compressed)  # str、repr的区别
    print("original string:", len(message))
    print("original bytes:", len(bytes_message))
    print("compressed:", len(compressed))
    print("decompressed:", len(decompressed))


# zlib.compressobj 用来压缩数据流，用于文件传输
def file_compress(beginFile, zlibFile, level):
    infile = open(beginFile, "rb")
    zfile = open(zlibFile, "wb")
    compressobj = zlib.compressobj(level)  # 压缩对象
    data = infile.read(1024)  # 1024为读取的size参数
    while data:
        zfile.write(compressobj.compress(data))  # 写入压缩数据
        data = infile.read(1024)  # 继续读取文件中的下一个size的内容
    zfile.write(compressobj.flush())  # compressobj.flush()包含剩余压缩输出的字节对象，将剩余的字节内容写入到目标文件中


def file_decompress(zlibFile, endFile):
    zlibFile = open(zlibFile, "rb")
    endFile = open(endFile, "wb")
    decompressobj = zlib.decompressobj()
    data = zlibFile.read(1024)
    while data:
        endFile.write(decompressobj.decompress(data))
        data = zlibFile.read(1024)
    endFile.write(decompressobj.flush())


def main():
    # 测试字符串的压缩与解压
    str_zlib()

    # 测试数据流压缩
    beginFile = "./beginFile.txt"
    zlibFile = "./zlibFile.txt"
    level = 9
    file_compress(beginFile, zlibFile, level)

    # 测试数据流解压
    zlibFile = "./zlibFile.txt"
    endFile = "./endFile.txt"
    file_decompress(zlibFile, endFile)


if __name__ == "__main__":
    main()


