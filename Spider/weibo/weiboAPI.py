"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/4/14 18:40
 @File    : weiboAPI.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

from weibo import APIClient

# 1.配置
APP_KEY = '4073142975'
APP_SECRET = '6e8a766757e8ae11b06f0e0bfc26b291'
CALLBACK_URL = 'http://apps.weibo.com/heyshheyou'  # 回调授权页面，用户完成授权后返回的页面

# 2.调用APIClient生成client实例
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

# 3.得到授权页面的url
url = client.get_authorize_url()
print(url)

# 4.点击访问url，在浏览器端获得code
code = '6ecdbf350f0680a6f00cc8c34ae721a6'
req = client.request_access_token(code)
client.set_access_token(req.get('access_token'), req.get('expires_in'))

# 5.调用微博普通读取接口，返回最新的公共微博。
# 接口详情见 https://open.weibo.com/wiki/2/statuses/public_timeline
statuses = client.statuses__public_timeline()['statuses']
print(len(statuses))
# 6.输出部分信息
for i in range(0, len(statuses)):
    print(u'昵称：' + statuses[i]['user']['screen_name'])
    print(u'简单介绍：' + statuses[i]['user']['description'])
    print(u'位置：' + statuses[i]['user']['location'])
    print(u'微博：' + statuses[i]['text'])
    print(statuses[i])
