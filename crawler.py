# -*- coding: utf-8 -*-
__author__ = 'YongCong Wu'
# @Time    : 2019/6/20 10:27
# @Email   :  : 1922878025@qq.com

from requests_html import HTMLSession
import csv

# 爬取豆瓣电影名称，导出csv

session = HTMLSession()

file = open('movies.csv', 'w', newline='')
csvwriter = csv.writer(file)
csvwriter.writerow(['名称', '年份'])

links = ['https://movie.douban.com/subject/1292052/', 'https://movie.douban.com/subject/26752088/', 'https://movie.douban.com/subject/1962665/']

for link in links:
    r = session.get(link)
    title = r.html.find('#content > h1 > span:nth-child(1)', first=True)
    year = r.html.find('#content > h1 > span.year', first=True)
    csvwriter.writerow(title.text)
    csvwriter.writerow(year.text)

file.close()