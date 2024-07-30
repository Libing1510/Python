# file: GoUpdateAvatar.py
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

def get_files(path):
    filenames=os.listdir(path)
    for dir in filenames:
        print(dir)

def get_AllFiles(goPath):
    files=[{"a":"2"}]
    for root,dirs,files in os.walk(goPath):
        for name in files:
            fullPath = os.path.join(root,name)
            print(name)
            files[name]=fullPath
    return files

def delete_SameFiles(originFiles={},sameFiles={}):
    print(originFiles)
    # for key in originFiles.keys()
    #     if sameFiles.get(key)
    #         # os.remove(sameFiles[key])
    #         print("delete: %s",key)


if True:
    goPath = input('place input go path...')
    # if goPath == "1"
    goPath=r"E:\UnityProject\Go\Assets\Project\YVRAvatar"
    print('go:',goPath)
    avatarPath = input('place input avatar path...')
    # if avatarPath == "2"
    avatarPath=r"E:\UnityProject\Avatar\com.yvr.avatar"
    print('avatar:',avatarPath)
    goFiles = get_AllFiles(goPath)
    avatarFiles = get_AllFiles(avatarPath)
    delete_SameFiles(**avatarFiles,**goFiles)