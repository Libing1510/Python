# -*- codeing = utf-8 -*-
import matplotlib.pyplot as plt  # 图表绘制
import numpy as np  # 数组库


# 基础绘图
def Test_01():
    # 定义x和y坐标轴上的点   x坐标轴上点的数值
    X = [1, 2, 3, 4]
    # y坐标轴上点的数值
    Y = [1, 4, 9, 16]
    # 使用plot绘制线条第1个参数是x的坐标值，第2个参数是y的坐标值
    plt.plot(X, Y)
    plt.show()


# 定义绘图属性
def Test_02():
    # 定义x和y坐标轴上的点   x坐标轴上点的数值
    X = [1, 2, 3, 4]
    # y坐标轴上点的数值
    Y = [1, 4, 9, 16]
    # 使用plot绘制线条第1个参数是x的坐标值，第2个参数是y的坐标值
    # color：线条颜色，值r表示红色（red)
    # marker：点的形状，值o表示点为圆圈标记（circle marker
    # linestyle：线条的形状，值dashed表示用虚线连接各点
    plt.plot(X, Y, color="g", marker="v", linestyle="dashed")
    # 坐标轴范围，axis[xmin, xmax, ymin, ymax]
    plt.axis([0, 6, 0, 20])
    plt.show()


# 添加说明，title 和注释
def Test_03():
    # 定义x和y坐标轴上的点   x坐标轴上点的数值
    X = [1, 2, 3, 4]
    # y坐标轴上点的数值
    Y = [1, 4, 9, 16]
    # 使用plot绘制线条第1个参数是x的坐标值，第2个参数是y的坐标值
    plt.plot(X, Y)
    # 添加文本 #x轴文本
    plt.xlabel("x axis")
    # y轴文本
    plt.ylabel("y axis")
    # 标题
    plt.title("Test_03")
    # 添加注释 参数名xy：箭头注释中箭头所在位置，参数名xytext：注释文本所在位置，
    # arrowprops在xy和xytext之间绘制箭头, shrink表示注释点与注释文本之间的图标距离
    plt.annotate(
        "我是注释 ##",
        xy=(2, 5),
        xytext=(2, 10),
        arrowprops=dict(facecolor="blue", shrink=0.01),
    )
    plt.show()


# 绘制多个图
def Test_04():
    # 创建画板1
    fig = plt.figure(1)  # 如果不传入参数默认画板1
    # 第2步创建画纸，并选择画纸1
    # subplot()方法里面传入的三个数字 前两个数字代表要生成几行几列的子图矩阵,第三个数字代表选中的子图位置 2行1列的图 （2，1，选择1或者2画纸）
    # subplot(2,1,1)生成一个2行1列的子图矩阵，当前是第一个子图
    ax1 = plt.subplot(2, 1, 1)
    # 在画纸1上绘图
    plt.plot([1, 2, 3])
    # 选择画纸2
    ax2 = plt.subplot(2, 1, 2)
    # 在画纸2上绘图
    plt.plot([4, 5, 6])
    # 显示图像
    plt.show()


# 数组绘图
def Test_05():
    # 定义一维数组
    t = np.arange(0, 5, 0.2)
    # 使用数组同时绘制多个线性
    # 线条1
    x1 = y1 = t
    # 线条2
    x2 = x1
    y2 = t**2
    # 线条3
    x3 = x1
    y3 = t**3
    # 使用plot绘制线条
    linesList = plt.plot(x1, y1, x2, y2, x3, y3)
    # 用 step 方法可以同时设置多个线条的属性
    plt.setp(linesList, color="r")
    plt.show()
    print("返回的数据类型", type(linesList))
    print("数据大小：", len(linesList))


Test_01()
Test_02()
Test_03()
Test_04()
Test_05()
