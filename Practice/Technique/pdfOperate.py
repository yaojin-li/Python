"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : pdf相关的操作
 --------------------------------
 @Time    : 2019/5/25 10:39
 @File    : pdfOperate.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import comDocOperate


class pdfOper():
    def __init__(self):
        pass

    def getLimitPagePdf(self, pdfPath, startPage, endPage):
        """
        截取pdf中的几页，输出到同目录
        :param pdfPath:
        :param startPage:
        :param endPage:
        :return:
        """
        output = PdfFileWriter()
        pdfFile = PdfFileReader(open(pdfPath, "rb"))

        # 保存input.pdf中的startPage-endPage页到output.pdf
        for i in range(startPage, endPage):
            output.addPage(pdfFile.getPage(i))

        outputStream = open(str(os.path.dirname(pdfPath)) + os.path.sep + "output.pdf", "wb")
        output.write(outputStream)
        outputStream.close()

    def MergePDF(self, fileDir, outfile):
        """
        合并同一目录下的所有PDF文件
        :param filepath: 存放PDF的原文件夹
        :param outfile: 输出的PDF文件的名称
        :return: 
        """
        output = PdfFileWriter()
        outputPages = 0
        pdfFileName = comDocOperate.getSameEndsFileInDir(fileDir, ".pdf")

        if pdfFileName:
            for pdfFile in pdfFileName:
                # 读取源PDF文件
                input = PdfFileReader(open(pdfFile, "rb"))
                # 获得源PDF文件中页面总数
                pageCount = input.getNumPages()
                outputPages += pageCount
                print("{pdfFile}文件页数：{pageCount}".
                      format(pdfFile=pdfFile, pageCount=pageCount))

                # 分别将page添加到输出output中
                for iPage in range(pageCount):
                    output.addPage(input.getPage(iPage))
            print("合并后的总页数:{pages}".format(pages=outputPages))

            # 写入到目标PDF文件
            outputStream = open(os.path.join(fileDir, outfile), "wb")
            output.write(outputStream)
            outputStream.close()
            print("PDF文件合并完成！")
        else:
            print("没有可以合并的PDF文件！")


if __name__ == '__main__':
    # 开始页
    startPage = 0
    # 截止页
    endPage = 5
    #
    pdfPath = r"D:\ZX\temp\test\1\0.pdf"

    pdfOper = pdfOper()
    # pdfOper.getLimitPagePdf(pdfPath, startPage, endPage)

    fileDir = r'D:\ZX\temp\test\1'  # 存放PDF的原文件夹
    outfile = "out.pdf"  # 输出的PDF文件的名称
    pdfOper.MergePDF(fileDir, outfile)
