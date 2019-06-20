#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'YongCong Wu'
# @Time    : 2019/6/14 16:18
# @Email   :  : 1922878025@qq.com


import requests, os, sys, xlwt
import pandas as pd

# 读取本地Excel 图片名称截取域名后半部分，跟本地图片名称作对比，上传服务器，返回成功地址更新原有excel图片地址。

reload(sys)
sys.setdefaultencoding('utf8')

ExcelPath = 'E:\ExcelImg\Drive\\'
DirPath = 'E:\80\\' + "files\\"
read_excel_list = []
read_img_path_list = []
presence_img = None


# 读取excel
def excel_list(file_path):
    df = pd.read_excel(ExcelPath + file_path, names=None)
    df_li = df.values.tolist()
    for i in df_li:
        split_str = i[1].split("/")[-1]
        read_excel_list.append(split_str)
    print u"Excel 读取完毕..........."


# 读取图片
def red_img(dir_path):
    for i in os.listdir(dir_path):
        if i.endswith('jpg') or i.endswith("png"):
            read_img_path_list.append(i)
    print u"Image 读取完毕..........."


# 两个list对比
def if_list(excel_list, img_list):
    filter_List = [x for x in excel_list if x in img_list]
    print u"图片对比完毕..........."
    butong = [y for y in (excel_list + img_list) if y not in filter_List]
    print u"存在的个数:   {0}".format(len(filter_List))
    print u"不存在的个数:   {0}".format(len(butong))
    report_excel_data = []
    num = 0
    for i in filter_List:
        ret = update_file(DirPath + i)
        num += 1
        report_excel_data.append([num, "域名/res/files/"+ret[0], ret[1] ])  # 本地图片名称添加域名
        print u"当前上传成功{0}张照片".format(num)
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet("Sheet 1", cell_overwrite_ok=True)
    for i, row in enumerate(report_excel_data):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    workbook.save(u'司机身份证正面.xls')
    print u"导出Excel完成............."


# 上传图片, 返回地址保存Excel
def update_file(name):
    url = '域名/upload'    # 上传图片服务器域名
    file_s = {'file': open(name, 'rb')}
    options = {'output': 'json', 'path': '', 'scene': 'default'}
    try:
        r = requests.post(url, files=file_s, data=options)
        res = r.json()
        split_str = name.split("\\")[-1]
        return split_str, res['url']
    except Exception as er:
        print(er)



excel_list('CardPhotoPath.xlsx')
red_img(DirPath)
if_list(read_excel_list, read_img_path_list)




