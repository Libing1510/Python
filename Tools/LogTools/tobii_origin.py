"""
计算tobii 原始数据
"""

import json
import numpy as np
import os
import csv
import math
import matplotlib.pyplot as plt


class vector2:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y


class vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z


class vector4:
    def __init__(self, _x, _y, _z, _w):
        self.x = _x
        self.y = _y
        self.z = _z
        self.w = _w

def read_log_origin():
