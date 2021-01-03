# -*- coding: utf-8 -*-
"""
Date    : 2020/2/12 上午12:53
Author  : zhanglu70
Description: 在这里描述本脚本的主要用途
"""
"""
爬取豆瓣电影Top250
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


def download(url, page):
    # url_basic = 'https://accounts.douban.com/j/mobile/login/basic'
    # #url = 'https://www.douban.com/'
    # ua_headers = {"User-Agent": 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'}
    # data = {
    #     'ck': '',
    #     'name': 'loozhang@163.com',
    #     'password': '980706321zllz',
    #     'remember': 'false',
    #     'ticket': ''
    # }

    s = requests.session()
    print(f"正在爬取：{url}")
    html = s.get(url,headers=headers,verify=False).text   # 这里不加text返回<Response [200]>
    soup = BeautifulSoup(html.encode("utf-8"), 'html.parser')
    lis = soup.select("ol li")
    for li in lis:
        index = li.find('em').text
        title = li.find('span', class_='title').text
        rating = li.find('span', class_='rating_num').text
        strInfo = re.search("(?<=<br/>).*?(?=<)", str(li.select_one(".bd p")), re.S | re.M).group().strip()
        infos = strInfo.split('/')
        year = infos[0].strip()
        area = infos[1].strip()
        type = infos[2].strip()
        write_fo_file(index, title, rating, year, area, type)
    page += 25
    if page < 250:
        time.sleep(2)
        download(f"https://movie.douban.com/top250?start={page}&filter=", page)


def write_fo_file(index, title, rating, year, area, type):
    f = open('movie_top250.csv', 'a',encoding="UTF-8")
    f.write(f'{index},{title},{rating},{year},{area},{type}\n')
    f.closed



def main():
    if os.path.exists('movie_top250.csv'):
        os.remove('movie_top250.csv')

    url = 'https://movie.douban.com/top250'
    download(url, 0)
    print("爬取完毕。")


if __name__ == '__main__':
    main()