"""
奥运五环
"""
import turtle
turtle.width(5)

turtle.color("blue")
turtle.circle(50)
turtle.penup()

turtle.goto(110,0)
turtle.pendown()
turtle.color("black")
turtle.circle(50)
turtle.penup()

turtle.goto(220,0)
turtle.pendown()
turtle.color("red")
turtle.circle(50)
turtle.penup()

turtle.goto(55,-60)
turtle.pendown()
turtle.color("yellow")
turtle.circle(50)
turtle.penup()

turtle.goto(165,-60)
turtle.pendown()
turtle.color("green")
turtle.circle(50)
turtle.penup()
