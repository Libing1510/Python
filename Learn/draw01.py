#导入模块
import turtle
t=turtle.Pen()

"""
这是一个循环360次，
每次转到59度。
""" 
for x in range(300):
    t.forward(x)
    t.left(59)

for y in range(100):
    t.forward(y)
    t.right(90)
