import os
from psd_tools import PSDImage


def psd_png(path):
    # 遍历目录下所有的图片文件
    label_names = os.listdir(path)
    label_dir = []
    for filename in label_names:
        if filename.endswith(".psd"):
            label_dir.append(os.path.join(path, filename))

    id = 0
    for i, filename in enumerate(label_dir):
        print(filename)
        psd = PSDImage.open(filename)
        newFile = str.format("C:/Users/YVR/Pictures/Test/finish_{0}.png", id)
        id += 1
        print(newFile)
        psd.composite().save(newFile)


psd_png(r"C:\Users\YVR\Pictures\Test")
