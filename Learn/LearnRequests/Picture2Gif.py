import os
import imageio


def compose_gif(path):
    # 遍历目录下所有的图片文件
    label_names = os.listdir(path)
    label_dir = []
    for filename in label_names:
        if filename.endswith(".png"):
            label_dir.append(os.path.join(path, filename))
    gif_images = []
    for i, filename in enumerate(label_dir):
        print(filename)
        gif_images.append(imageio.imread(filename))

    imageio.mimsave(path + r"/test.gif", gif_images, fps=5)


compose_gif(r"C:\Users\YVR\Pictures\Test")
