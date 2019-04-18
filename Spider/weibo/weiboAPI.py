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
import webbrowser

APP_KEY = '4073142975'
APP_SECRET = '6e8a766757e8ae11b06f0e0bfc26b291'
CALLBACK_URL = 'http://apps.weibo.com/heyshheyou'  # 回调授权页面，用户完成授权后返回的页面
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

url = client.get_authorize_url()  # 得到授权页面的url
# webbrowser.open_new(url)
print(url)
code = '7cffcf7f949726b2ab2ed753df994b57'

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
client.set_access_token(r.get('access_token'), r.get('expires_in'))

print(r)

access_token = r.access_token
expires_in = r.expires_in
client.set_access_token(access_token, expires_in)

#print client.statuses__public_timeline()
statuses = client.statuses__public_timeline()['statuses']
length = len(statuses)
#输出了部分信息
for i in range(0,length):
    print(u'昵称：'+statuses[i]['user']['screen_name'])
    print(u'简单介绍：'+statuses[i]['user']['description'])
    print(u'位置：'+statuses[i]['user']['location'])
    print(u'微博：'+statuses[i]['text'])