"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 测试 python 推送钉钉消息
 --------------------------------
 @Time    : 2020/2/9 19:13
 @File    : demo.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
import json
import logging
import pymysql

# 日志文件设置
logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='/app/mom/demo/run_log.log',  # 指定生成日志文件的位置，否则默认在 /root 路径下生成日志文件
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


# 链接数据库，读取数据
def conn_read_data():
    conn_info = pymysql.connect(
        host='XXXX',
        port=3306,
        user='XXXX',
        passwd='XXXX',
        db='XXXX',
        charset='utf8'  # utf8 not utf-8
    )
    try:
        cursor = conn_info.cursor()
        findall_sql = "select count(id) from XXXX"
        count = cursor.execute(findall_sql)
        cursor.close()
        conn_info.close()
        return count
    except Exception:
        conn_info.rollback()  # 发生错误则全部回滚


# 钉钉推送消息
def ding_push_message(msg):
    # 构建请求数据
    message = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "isAtAll": True
        }
    }

    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=web_url, data=message_json, headers=header)
    # 打印返回的结果
    logging.info(info.text)


if __name__ == "__main__":
    # 钉钉请求的URL，WebHook地址
    web_url = "https://oapi.dingtalk.com/robot/send?access_token=XXXX"

    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    # 构建请求数据
    msg = "【钉钉消息】目前人数共" + str(conn_read_data()) + "人。"

    ding_push_message(msg)
