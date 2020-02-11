"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
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
import vertica_python
import logging

# 日志文件设置
logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='new.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


# 链接 vertica 数据库，读取数据
def conn_read_data():
    conn_info = {
        'host': '10.1.131.39',
        'port': 5433,
        'user': 'kjresearch',
        'password': 'Tebon@2019',
        'database': 'bigdata',
        'connection_timeout': 5
    }
    connection = vertica_python.connect(**conn_info)
    connection.close()

    # using with for auto connection closing after usage
    with vertica_python.connect(**conn_info) as connection:
        cur = connection.cursor()
        sql = "select count(DISTINCT visitor_id) from wx.page_log where type='view' and page_title='上传身份证页' " \
              "and page_domain in ('ths','https://kaihu.tebon.com.cn') " \
              "and created_time between to_char(TIMESTAMPADD('MINUTE', -3, sysdate),'yyyy-MM-dd HH24:mi:ss') and to_char(sysdate, 'yyyy-MM-dd HH24:mi:ss')"
        data = cur.execute(sql).fetchall()
        return data


# 调用大数据平台接口
def read_data_from_platform():
    # 大数据平台接口URL
    platform_url = "http://172.16.101.43:8080/bdopen/api/getModelScsfz"

    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    data = requests.put(url=platform_url, headers=header)
    print(data.text)


# 调用模型，得出结果
def load_model():
    # 模型系数
    modulus = 0.396
    #
    id_count = read_data_from_platform()
    return id_count, modulus * id_count


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
    web_url = "https://oapi.dingtalk.com/robot/send?access_token=1789e4d28b7cd0da2bc4c0fad04633bc830ca9a1c12ed3b8f31a82b53f50999b"

    # 大数据平台接口URL
    platform_url = "http://172.16.101.43:8080/bdopen/api/getModelScsfz"

    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    read_data_from_platform()

    # #
    # id_count, view_count = load_model()
    #
    # # 构建请求数据
    # msg = "【钉钉消息】前一分钟进入上传身份证页" + str(id_count) + "人，预计进入视频见证" + str(view_count) + "人。"
    #
    # ding_push_message(msg)
