# 爬取电影影评

'''
requests+bs4+jieba

IPO
Input: 电影网站链接
Process: 网站链接 - 电影链接 - 评论处理 
Output: 词云图
'''

import os
import sys
import requests
import re
import jieba
import pandas as pd
import numpy
from pyecharts import WordCloud
from bs4 import BeautifulSoup as bs


# 获取电影
def getNowPlayingMovie(url):
    r = requests.get(url)
    html = r.text
    soup = bs(html, "html.parser")
    nowplaying_movie = soup.find_all("div", id = "nowplaying")
    nowplaying_movie_list = nowplaying_movie[0].find_all("li", class_ = "list-item")    # [0]
    movieList = []
    for oneMovie in nowplaying_movie_list:
        movieDict = {}                  # 列表中的元组存储数据
        movieDict["id"] = oneMovie["data-subject"]  # 通过css属性标签直接获取属性值
        movieDict["name"] = oneMovie["data-title"]
        movieList.append(movieDict)
    return movieList

# 获取评论
def getCommentsById(moviedId, pageNum):
    for i in range(pageNum):
        url = "https://movie.douban.com/subject/" + moviedId + "/comments?start=0&limit=" + str(i)

        # 处理特殊文字、符号的乱码问题
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        r = requests.get(url)
        html = r.text
        html = html.translate(non_bmp_map)
        soup = bs(html, "html.parser")
        comments = soup.find_all("div", id = "comments")
        comments_list = comments[0].find_all("p", class_="")

        commentsResult = []
        for comment in comments_list:
            if comment.string == None or comment.string == "":
                continue
            else:
                commentsResult.append(comment.string.strip())
    return commentsResult

# 数据处理
def dataWranging(dataList):
    ## 1. 筛选所有评论文字
    dataStr = ""
    for data in dataList:
        dataStr = dataStr + data
    patten = re.compile(r"[\u4e00-\u9fa5]+")        # 匹配所有文字
    filterData = re.findall(patten, dataStr)
    wrangedData = "".join(filterData)               # List to String

    ## 2. 分词
    segment = jieba.lcut(wrangedData)               # 结巴分词
    words_df = pd.DataFrame({'segment': segment})   # pandas显示分词结果

    ## 3. 除去停用词(设置chineseStopWords.txt文件为utf-8编码)
    stopwords = pd.read_csv(".\stopWords.txt", index_col = False, quoting = 3, sep = "\t", names = ["stopword"])
    keyWords = words_df[~words_df.segment.isin(stopwords.stopword)]
    keyWordsList = []
    temp = list(keyWords.as_matrix())      # 返回向量组成的列表
    for i in range(len(keyWords)):
        keyWordsList.append(temp[i][0])

    ## 4. 词频统计
    keyWordDict = {}
    for keyWord in keyWordsList:
        if keyWord not in keyWordDict:
            keyWordDict[keyWord] = 1
        else:
            keyWordDict[keyWord] += 1
    keyWordDict = sorted(keyWordDict.items(), key = lambda x:x[1], reverse = True)  # 按照频率排序
    return keyWordDict[:100]

# 绘制词云图
def wordCloud(keyWordDict, label):
    x = []; y = []
    for i in range(len(keyWordDict)):
        x.append(keyWordDict[i][0])
        y.append(keyWordDict[i][1])
    wordCloud = WordCloud(label, width = 1300, height = 620)
    wordCloud.add("", x, y, word_size_range = [20, 100], shape = "circle")
    wordCloud.render()
    os.system(r"render.html")


def main():
    url = "https://movie.douban.com/cinema/nowplaying/shanghai/"
    # movieList = getNowPlayingMovie(url)

    pageNum = 5
    moviedId = "26363254"
    commentsResult = getCommentsById(moviedId, pageNum)

    keyWordDict = dataWranging(commentsResult)

    label = "词云图"
    wordCloud(keyWordDict, label)

if __name__ == "__main__":
    main()


