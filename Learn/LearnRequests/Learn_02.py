# -*- codeing = utf-8 -*-
## 学习地址：https://blog.csdn.net/ChenBinBini/article/details/109739116

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定 URL,获取网页数据
import xlwt  # 进行 excel 操作

# 创建正则表达式对象，表售规则， 影片详情连接的规则
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)">', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r"<span>(\d*)人评价</span>")
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def Test():
    baseurl = "https://movie.douban.com/top250?start="  # 要爬取的网页链接
    # 1. 爬取网页
    dataList = GetData(baseurl)
    # 存入excel 的文件名
    savePath = "豆瓣电影Top250.xls"
    # 3. 保存数据
    SaveData(dataList, savePath)


def GetData(baseurl):
    dataList = []  # 用来存储爬取的网页信息
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = AskURL(url)  # 保存获取到的网页源码
        # 2. 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):  # 查找符合要求的字符串
            data = []  # 保存一部电影所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]  # 通过正则表达式查找
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                cTitle = titles[0]
                data.append(titles[0])
                oTitle = titles[1].replace("/", "")  # 消除转义字符
                data.append(oTitle)
            else:
                data.append(titles[0])
                data.append(" ")
            rating = re.findall(findRating, item)
            data.append(rating)
            judgeNum = re.findall(findJudge, item)
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findBd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", "", bd)
            bd = re.sub("/", "", bd)
            data.append(bd.strip())
            dataList.append(data)
    return dataList


def AskURL(url):
    # 模拟浏览器头部信息，向豆瓣服务器发送消息
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    print("AskURL: {0}".format(url))
    request = urllib.request.Request(
        url, headers=head
    )  # 这里必现使用headers=head原网址是没有使用的，会报错
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def SaveData(dataList, savePath):
    print("saving ........")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet("豆瓣电影Top250", cell_overwrite_ok=True)  # 创建工作表
    col = (
        "电影详情链接",
        "图片链接",
        "影片中文名",
        "影片外国名",
        "评分",
        "评价数",
        "概况",
        "相关信息",
    )
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = dataList[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 写入数据
    book.save(savePath)  # 保存文件


Test()
