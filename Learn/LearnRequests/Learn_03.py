# -*- coding:utf-8 -*-
# 模拟键盘和鼠标操作
import keyboard
import pyautogui


def Test_Keyboard():
    # write() 函数将输入作为参数传递给此函数的任何字符串。此函数将人工键盘事件发送到操作系统，然后在插入符号处进一步键入。
    keyboard.write("Python is an amazing programming language.")
    # 如果键盘上没有任何字符可用，则键入明确的 Unicode 字符。press_and_release() 函数发送操作系统事件以执行热键并键入作为参数传递的字符。
    keyboard.press_and_release("enter")
    keyboard.press_and_release("enter")
    keyboard.press_and_release("shift+p")
    keyboard.press_and_release("y")
    keyboard.press_and_release("t")
    keyboard.press_and_release("h")
    keyboard.press_and_release("o")
    keyboard.press_and_release("n")


def Test_Mouse():
    pyautogui.write("Python is an amazing programming language.")
    pyautogui.keyDown("shift")
    pyautogui.press("a")
    pyautogui.press("b")
    pyautogui.press("c")
    pyautogui.keyUp("shift")
    pyautogui.press("x")
    pyautogui.press("y")
    pyautogui.press("z")
    pyautogui.keyDown("shift")
    pyautogui.press("a")
    pyautogui.keyUp("shift")
    pyautogui.keyDown("shift")
    pyautogui.press("b")
    pyautogui.keyUp("shift")
    pyautogui.keyDown("shift")
    pyautogui.press("c")
    pyautogui.keyUp("shift")


Test_Mouse()
