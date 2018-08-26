# 获取豆瓣影评

"""
requests + Xpath + pandas + MongoDB
IPO:
input: url
process: 获取HTML页面内容，Xpath解析，pandas数据处理，数据写入csv文件，数据存入数据库
output: csv文件、存入到mongodb

评论内容解析：
id
name
recommend
time
title
content	  https://movie.douban.com/review/5199026 + id
useful
useless
comment
	res_name
	res_time
	res_content
	
问题：
1. 评论解析为空，适配不同的标签 √
2. 评论文字过多，csv文件中单个单元格错乱 （设置阈值，大于则压缩或截取部分内容）
3. IP被封，调试问题 （将爬取下来的内容存入临时文件中，从文件中读取数据）
4. 数据清理，存储为文件
"""

import requests
import re
from lxml import etree
import pandas as pd
import csv
import codecs
import traceback
import random

# 选取随机的IP地址
def getRandomIP():
    with open("./ipPool.txt", "r") as f:
        content = f.read()
        contList = content.split("', '")
        ipList = contList[1:len(contList)-1]
        random_ip = random.choice(ipList)
        proxy_ip = "http://" + random_ip
        proxies = {"http" : proxy_ip }
    return proxies

def getHTMLContent(url, headers, proxies):
    res = requests.get(url, headers = headers, proxies = proxies)
    struct = etree.HTML(res.text)

    dic = {}
    filmName = struct.xpath('//div[@id="content"]/h1/text()')
    dic["0"] = filmName
    IDList = struct.xpath('//div[@class="main review-item"]/@id')
    dic["1"] = IDList
    nameList = struct.xpath('//a[@class="name"]/text()')
    dic["2"] = nameList
    recommendList = struct.xpath('//header[@class="main-hd"]/span/@title')
    dic["3"] = recommendList
    timeList = struct.xpath('//span[@class="main-meta"]/text()')
    dic["4"] = timeList
    titleList = struct.xpath('//div[@class="main-bd"]/h2/a/text()')
    dic["5"] = titleList

    contentList = []
    for userid in IDList:
        contentURL = "https://movie.douban.com/review/" + userid
        r = requests.get(contentURL, headers = headers, proxies = proxies)
        contStruct = etree.HTML(r.text)
        fullContentOne = stripForList(contStruct.xpath('//div[@class="review-content clearfix"]/text()'))
        fullContentTwo = stripForList(contStruct.xpath('//div[@class="review-content clearfix"]/p/text()'))
        resultContent = fullContentOne + fullContentTwo     # list合并
        contentList.append(resultContent)
    dic["6"] = contentList

    usefulList = stripForList(struct.xpath('//a[@title="有用"]/span/text()'))
    dic["7"] = usefulList
    uselessList = stripForList(struct.xpath('//a[@title="没用"]/span/text()'))
    dic["8"] = uselessList
    commentList = struct.xpath('//a[@class="reply"]/text()')
    dic["9"] = commentList

    with open("./temp2.txt", "w", encoding = "utf-8") as f:
        f.write(str(dic))

    return dic

def writeData2CSV(HTMLDic):
    csv_col_name = ["主题", "用户ID", "用户名", "推荐力度", "评论时间", "评论标题", "评论内容", "有用个数", "没用个数", "回应内容"]
    resultDic = {}

    HTMLDic = cleanData(HTMLDic)
    
    try:
        for i in range(1, len(csv_col_name)):
            resultDic[csv_col_name[i]] = HTMLDic[str(i)]
        dataframe = pd.DataFrame(resultDic)
        dataframe.to_csv("./test2.csv", sep=',', encoding = "utf_8_sig", columns = csv_col_name)    # 解决中文在csv文件中乱码
    except:
        traceback.print_exception
    

def cleanData(HTMLDic):
    print("begin clean...")
    dic = {'！,':'！', '……,':'……', '？,':'？', ',,':''}
    for j in range(len(HTMLDic)):
        if j == 6:  # 清理内容
            for i in range(len(HTMLDic[str(j)])):
                HTMLDic[str(j)][i] = re.sub(r'\*|\'|\[|\]|\ |\\|\/', "", str(HTMLDic[str(j)][i]))
                for key,value in dic.items():
                    HTMLDic[str(j)][i] = HTMLDic[str(j)][i].replace(key, value)
        else:
            continue
        
    return HTMLDic


def getHTMLDic():
    tempFile = "./temp2.txt"
    tempStr = ""
    with open(tempFile, "r", encoding = "utf-8") as f:
        tempStr = f.read()
    tempDic = eval(tempStr)     # str to dic
    return tempDic

    
def stripForList(targetList):
    result = []
    for target in targetList:
        result.append(target.strip())
    return result


def main():
    url = "https://movie.douban.com/subject/1292212/reviews"
    headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
    #proxies = getRandomIP()
    #HTMLDic = getHTMLContent(url, headers, proxies)
    HTMLDic = getHTMLDic()
    writeData2CSV(HTMLDic)

if __name__ == "__main__":
    main()


