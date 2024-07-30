## 学习地址： https://zhuanlan.zhihu.com/p/270391233
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定 URL,获取网页数据
import xlwt  # 进行 excel 操作
import requests
from bs4 import (
    BeautifulSoup,
)  ##如果库没有：pip install beautifulsoup4 , pip show beautifulsoup4


def Test01_get():
    ## 请求网页数据
    res = requests.get("http://www.douban.com")
    print(res)
    print(type(res))
    ## 输出网页数据 text 或者 content
    print(type(res.text))
    print(res.text)


def Test02_get():
    url = "https://movie.douban.com/celebrity/1011562/photos/"
    res = requests.get(url).text
    print(type(res))
    print(res)
    content = BeautifulSoup(res, "html.parser")
    data = content.find_all("div", attrs={"class": "cover"})
    print("data count:".format(data.count))
    picture_list = []
    for d in data:
        plist = d.find("img")["src"]
        picture_list.append(plist)
    print(picture_list)


Test02_get()
