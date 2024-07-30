import os
from PIL import Image


def bmp2png(json_dir):
    label_names = os.listdir(json_dir)
    label_dir = []
    for filename in label_names:
        if filename.endswith(".bmp"):
            label_dir.append(os.path.join(json_dir, filename))
    for i, filename in enumerate(label_dir):
        print(filename)
        im = Image.open(filename)  # open ppm file

        newname = label_names[i].split(".")[0] + ".png"  # new name for png file
        im.save(os.path.join(json_dir, newname))
        # os.remove(filename)


json_dir1 = r"D:\Log\testcap\SGS测试图卡\602色立体色域测试图卡（3648x3144)"
json_dir2 = r"D:\Log\testcap\SGS测试图卡\Testpattern_1"
json_dir3 = r"D:\Log\testcap\SGS测试图卡\灰阶相应时间测试pattern"
json_dir4 = r"D:\Log\testcap\SGS测试图卡\测试图"
bmp2png(json_dir1)
bmp2png(json_dir2)
bmp2png(json_dir3)
bmp2png(json_dir4)
