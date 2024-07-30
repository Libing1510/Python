import json
import re
import numpy as np
import time
from decimal import Decimal

import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, TwoCellAnchor


class vector3:
    # def __init__(self):
    #     self.x = 0
    #     self.y = 0
    #     self.z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def toJson(self):
        return {"x": self.x, "y": self.y, "z": self.z}


class vector4:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def toJson(self):
        return {"x": self.x, "y": self.y, "z": self.z, "w": self.w}


class LogData:
    def __init__(self):
        self.timeStr = "null"
        self.pos = ""
        self.dir = ""

    def __init__(self, timeStr, pos, dir):
        self.timeStr = timeStr
        self.pos = pos
        self.dir = dir

    def toJson(self):
        json_str = (
            '{"timeStr":"aaa","pos":{"x":1,"y":1,"z":1},"dir":{"x":0,"y":0,"z":1}}'
        )
        jsonData = json.loads(json_str)
        jsonData["timeStr"] = self.timeStr
        jsonData["pos"]["x"] = self.pos.x
        jsonData["pos"]["y"] = self.pos.y
        jsonData["pos"]["z"] = self.pos.z
        jsonData["dir"]["x"] = self.dir.x
        jsonData["dir"]["y"] = self.dir.y
        jsonData["dir"]["z"] = self.dir.z
        return json.dumps(jsonData)

    def toString(self):
        return str.format(
            '\{"timeStr":"{0}","pos":\{"x"{1},"y":{2},"z":{3}\},"dir":{"x":{4},"y":{5},"z":{6}\}\}',
            self.timeStr,
            self.pos.x,
            self.pos.y,
            self.pos.z,
            self.dir.x,
            self.dir.y,
            self.dir.z,
        )


def ReadTobiiLog(file, key):
    pattern = r"\[(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?)]"
    direction = []
    with open(file, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for l in lines:
            if l.find(key) >= 0:
                match = re.search(pattern, l)
                if match:
                    content = match.group(0)
                    temp = re.sub(r"\[|\]", "", content)
                    data = re.split(r",", temp)
                    v3 = vector3()
                    v3.x = float(data[0])
                    v3.y = float(data[1])
                    v3.z = float(data[2])
                    direction.append(v3)
    return direction


def ReadYYLog(file, key):
    pattern = r"\((-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?)\)"
    direction = []
    with open(file, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for l in lines:
            if l.find(key) >= 0:
                match = re.search(pattern, l)
                if match:
                    content = match.group(0)
                    temp = re.sub(r"\(|\)", "", content)
                    data = re.split(r",", temp)
                    v4 = vector4()
                    v4.x = float(data[0])
                    v4.y = float(data[1])
                    v4.z = float(data[2])
                    v4.w = float(data[3])
                    direction.append(v4)
    return direction


def ReadLBOrigin_dirLog(file, key):
    pattern = r"\(x:[\d.-]+,y:[\d.-]+,z:[\d.-]+\)"
    direction = []
    with open(file, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for l in lines:
            if l.find(key) >= 0:
                # print(l)
                dir = re.split(r"direction:", l)[1]
                match = re.search(pattern, dir)
                if match:
                    content = match.group(0)
                    # print(content)
                    temp = re.sub(r"\(|\)|x\:|y\:|z\:", "", content)
                    data = re.split(r",", temp)
                    v3 = vector3()
                    v3.x = float(data[0])
                    v3.y = float(data[1])
                    v3.z = float(data[2])
                    direction.append(v3)
    return direction


def quaternion_angle(q1, q2):
    # Compute the dot product of the quaternions
    dot_product = np.dot(q1, q2)

    # Compute the magnitude of the dot product
    dot_product_magnitude = np.linalg.norm(dot_product)

    # Compute the angle between the quaternions
    angle = 2 * np.arccos(np.clip(dot_product_magnitude, -1.0, 1.0))

    return np.degrees(angle)  # Convert radians to degrees


def vector_angle(v1, v2):
    # Normalize the vectors
    v1_normalized = v1 / np.linalg.norm(v1)
    v2_normalized = v2 / np.linalg.norm(v2)

    # Compute the dot product
    dot_product = np.dot(v1_normalized, v2_normalized)

    # Compute the angle (in radians) between the vectors
    angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))

    # Convert radians to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg


def DrawVector3(v3, key):
    # # 绘图
    X = []
    Y = []
    Z = []
    tt = []
    i = 0
    angle = []
    v1 = np.array([v3[0].x, v3[0].y, v3[0].z])
    for v in v3:
        v2 = np.array([v.x, v.y, v.z])
        angle_d = vector_angle(v1, v2)
        angle.append(angle_d)
        X.append(v.x)
        Y.append(v.y)
        Z.append(v.z)
        i += 1
        tt.append(i)
        v1 = v2

    fig, ax = plt.subplots(1, 2)
    ax[0].plot(tt, X, "r", label="X")
    ax[0].plot(tt, Y, "g", label="Y")
    ax[0].plot(tt, Z, "b", label="Z")
    ax[0].set_ylabel("X,Y,Z")
    ax[1].plot(angle)
    ax[1].set_ylabel(f"{key}_angle")
    plt.title = key
    Now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    plt.savefig(f"./{key}_{Now_time}.jpg")
    plt.show()


def DrawVector4(v4, key):
    # # 绘图
    X = []
    Y = []
    Z = []
    W = []
    tt = []
    i = 0
    angle = []
    q1 = np.array([v4[0].x, v4[0].y, v4[0].z, v4[0].w])
    for v in v4:
        q2 = np.array([v.x, v.y, v.z, v.w])
        angle_d = quaternion_angle(q1, q2)
        angle.append(angle_d)
        X.append(v.x)
        Y.append(v.y)
        Z.append(v.z)
        W.append(v.w)
        i += 1
        tt.append(i)
        q1 = q2

    fig, ax = plt.subplots(1, 2)
    ax[0].plot(tt, X, "r", label="X")
    ax[0].plot(tt, Y, "g", label="Y")
    ax[0].plot(tt, Z, "b", label="Z")
    ax[0].plot(tt, W, "k", label="Z")
    ax[0].set_ylabel("X,Y,Z")
    ax[1].plot(angle)
    ax[1].set_ylabel(f"{key}_angle")
    plt.title = key
    Now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    plt.savefig(f"./{key}_{Now_time}.jpg")
    plt.show()


def tobii_gazeDirectionCombined(file):
    tobiikey = "gazeDirectionCombined:"
    dir = ReadTobiiLog(file, tobiikey)
    if len(dir):
        DrawVector3(dir, tobiikey)
    else:
        print("cant find data")


def tobii_foveatedGazeDirection(file):
    tobiikey = "foveatedGazeDirection:"
    dir = ReadTobiiLog(file, tobiikey)
    if len(dir):
        DrawVector3(dir, tobiikey)
    else:
        print("cant find data")


def tobii_gazeOriginCombined(file):
    tobiikey = "gazeOriginCombined:"
    dir = ReadTobiiLog(file, tobiikey)
    if len(dir):
        DrawVector3(dir, tobiikey)
    else:
        print("cant find data")


def yy_orientation(file):
    yykey = "out_relation orientation"
    quartion = ReadYYLog(file, yykey)
    if len(quartion):
        DrawVector4(quartion, yykey)
    else:
        print("cant find data")


def lb_direction(file):
    yykey = "SSS:origin:"
    quartion = ReadLBOrigin_dirLog(file, yykey)
    if len(quartion):
        DrawVector3(quartion, "SSS")
    else:
        print("cant find data")


def lb_saveTobiiOrigin(file):
    yykey = "SSS:origin:"
    pattern = r"\(x:[\d.-]+,y:[\d.-]+,z:[\d.-]+\)"
    time_pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3})"
    direction = []
    pose = []
    times = []
    logData = []
    with open(file, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for l in lines:
            if l.find(yykey) >= 0:
                # print(l)
                dt = re.split(r"direction:", l)
                posStr = dt[0]
                dirStr = dt[1]
                matchDir = re.search(pattern, dirStr)
                if matchDir:
                    dirContent = matchDir.group(0)
                    temp = re.sub(r"\(|\)|x\:|y\:|z\:", "", dirContent)
                    data = re.split(r",", temp)
                    v3Dir = vector3(float(data[0]), float(data[1]), float(data[2]))
                    direction.append(v3Dir)

                matchPos = re.search(pattern, posStr)
                if matchPos:
                    posContent = matchPos.group(0)
                    temp = re.sub(r"\(|\)|x\:|y\:|z\:", "", posContent)
                    data = re.split(r",", temp)
                    v3Pos = vector3(float(data[0]), float(data[1]), float(data[2]))
                    pose.append(v3Pos)

                matchTime = re.search(time_pattern, posStr)
                if matchTime:
                    timer = matchTime.group(0)
                    times.append(timer)
                logData.append(LogData(timer, v3Pos, v3Dir))
    print(
        "time={0}，pos={1},dir={2},logData={3}",
        len(times),
        len(pose),
        len(direction),
        len(logData),
    )
    return logData


def save_json(save_path, data):
    assert save_path.split(".")[-1] == "json"
    with open(save_path, "w") as file:
        js = json.dumps(data)
        json.dump(js, file)


def write_txt(file_path, SaveList):
    # 写入存档到文件
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("[")
        for i in SaveList:
            file.write(i.toJson())
            file.write(",")
        file.write("]")
        file.close()


# def draw_points(file_path,saveList):
#     pos_x[]
#     pos_y[]
#     for data in saveList:
#         posX.append(data.pos.X)


# logFile = f"D:/DingDing/temp(1)(1).log"

# logFile = f"D:/DingDing/2024-06-06_19_01_27/2024-06-06_19_01_27.log"
# tobii_gazeDirectionCombined(logFile)
# tobii_foveatedGazeDirection(logFile)
# tobii_gazeOriginCombined(logFile)
# yy_orientation(logFile)

logFile = f"D:\Log\D3HDXD2D4231000086_20240723_121143\systemlog_1.txt"
da = lb_saveTobiiOrigin(logFile)
write_txt("D:/Log/tobii_data.json", da)
