"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 测试钉钉群机器人推送消息
 安全设置是必填项，例如
     自定义关键字：钉钉
     钉钉发送通知时，必须包含关键字 “钉钉”，不然会报 keyword not in content。
 --------------------------------
 @Time    : 2020/2/9 18:34
 @File    : dingding_push.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import requests
import json


def ding_push_message():
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

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
    print(info.text)


if __name__ == "__main__":
    # 请求的URL，WebHook地址
    web_url = "https://oapi.dingtalk.com/robot/send?access_token=1789e4d28b7cd0da2bc4c0fad04633bc830ca9a1c12ed3b8f31a82b53f50999b"
    # 构建请求数据
    msg = "钉钉，测试消息。。。"

    ding_push_message()
