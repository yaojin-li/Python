"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : pdf相关的操作
 --------------------------------
 @Time    : 2019/5/25 10:39
 @File    : pdf_operate.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import comDocOperate


class PdfOperate():
    def __init__(self):
        pass

    def get_limit_page_pdf(self, pdf_path, start_page, end_page):
        """
        截取pdf中的几页，输出到同目录
        :param pdf_path:
        :param start_page:
        :param end_page:
        :return:
        """
        output = PdfFileWriter()
        pdf_file = PdfFileReader(open(pdf_path, "rb"))

        # 保存input.pdf中的start_page-end_page页到output.pdf
        for i in range(start_page, end_page):
            output.addPage(pdf_file.getPage(i))

        output_stream = open(str(os.path.dirname(pdf_path)) + os.path.sep + "output.pdf", "wb")
        output.write(output_stream)
        output_stream.close()

    def merge_pdf(self, file_dir, outfile):
        """
        合并同一目录下的所有PDF文件
        :param filepath: 存放PDF的原文件夹
        :param outfile: 输出的PDF文件的名称
        :return: 
        """
        output = PdfFileWriter()
        output_pages = 0
        pdf_file_name = comDocOperate.getSameEndsFileInDir(file_dir, ".pdf")

        if pdf_file_name:
            for pdf_file in pdf_file_name:
                # 读取源PDF文件
                input = PdfFileReader(open(pdf_file, "rb"))
                # 获得源PDF文件中页面总数
                page_count = input.getNumPages()
                output_pages += page_count
                print("{pdfFile}文件页数：{page_count}".
                      format(pdfFile=pdf_file, page_count=page_count))

                # 分别将page添加到输出output中
                for one_page in range(page_count):
                    output.addPage(input.getPage(one_page))
            print("合并后的总页数:{pages}".format(pages=output_pages))

            # 写入到目标PDF文件
            output_stream = open(os.path.join(file_dir, outfile), "wb")
            output.write(output_stream)
            output_stream.close()
            print("PDF文件合并完成！")
        else:
            print("没有可以合并的PDF文件！")


if __name__ == '__main__':
    # 开始页
    start_page = 0
    # 截止页
    end_page = 5
    #
    pdf_path = r"D:\ZX\temp\test\1\0.pdf"

    pdf_operate = PdfOperate()
    # pdfOper.get_limit_page_pdf(pdf_path, start_page, end_page)

    file_dir = r'D:\ZX\temp\test\1'  # 存放PDF的原文件夹
    outfile = "out.pdf"  # 输出的PDF文件的名称
    pdf_operate.merge_pdf(file_dir, outfile)
