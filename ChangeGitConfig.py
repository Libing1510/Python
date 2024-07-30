# file: ChangeGitConfig.py
#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import os

def get_files(path):
    filenames=os.listdir(path)
    for dir in filenames:
        print(dir)
        
def get_Allfiles(path):
    for root,dirs,files in os.walk(path):
        for name in files:
            fullPath = os.path.join(root,name)
            if('.git\config' in fullPath):
                change_ip(fullPath)
            elif('Packages\manifest.json' in fullPath):
                change_ip(fullPath)
    
def change_ip(filePath):
    file = open(filePath,mode='r')
    lines = file.readlines()
    file.close()
    newLines = []
    needWrite = False
    for line in lines:
        if('com.yvr.androiddevice' in line):
            print('filePath:',filePath)
            line = line.replace('com.yvr.androiddevice','com.yvr.android-device')
            needWrite=True
        newLines.append(line)
    pass
    print(filePath,needWrite)    
    if needWrite:    
        newfile = open(filePath,mode='w+')
        newfile.writelines(newLines)
        newfile.close()

    
if True:
    path = input('place input path...')
    print('input:',path)
    get_Allfiles(path)
