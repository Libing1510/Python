from win32com.shell import shell, shellcon
import os
import pythoncom


def GetFolder(path, folder=None):
    folderName = path.split("\\", 1)
    baseFolder = folder or shell.SHGetDesktopFolder()
    for pidl in baseFolder:
        if baseFolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == folderName[0]:
            folder = baseFolder.BindToObject(pidl, None, shell.IID_IShellFolder)
            break
        if len(folderName) > 1:
            return GetFolder(folderName[1], folder)
        else:
            return folder


def CopyFilesToComputer(
    folder, phoneFolderPath, computerDir, currentComputerDir=None, dateName=True
):
    if folder:
        isPfo = True
        # 遍历文件
        for filePidl in folder:
            # 获取文件名
            fileName = folder.GetDisplayNameOf(filePidl, shellcon.SHGDN_FORADDRESSBAR)
            # 判断是否为文件夹
            isFolder = folder.GetAttributesOf([filePidl], shellcon.SFGAO_FOLDER)
            if isFolder == 536870912:
                # 生成电脑文件夹路径，将手机路径替换为电脑路径
                newComputerDir = fileName.replace(phoneFolderPath, computerDir)
                # 如果电脑不存在文件夹则新建文件夹
                if not os.path.exists(newComputerDir):
                    os.makedirs(newComputerDir)
                newFolder = folder.BindToObject(filePidl, None, shell.IID_IShellFolder)
                CopyFilesToComputer(
                    newFolder, phoneFolderPath, computerDir, newComputerDir
                )
            # 如果是文件，则进行拷贝
            elif isFolder == 0:
                if currentComputerDir is not None:
                    computerDirPidl = shell.SHILCreateFromPath(currentComputerDir, 0)
                else:
                    computerDirPidl = shell.SHILCreateFromPath(computerDir, 0)
                computerDirItem = shell.SHCreateItemFromIDList(computerDirPidl)
                phoneFolderPidl = shell.SHGetIDListFromObject(folder)
                # 生成当前复制的文件的PIDL,手机文件夹的 PIDL + 文件的 PIDL
                filePidl = phoneFolderPidl + filePidl
                pidlItem = shell.SHCreateItemFromIDList(filePidl, shell.IID_IShellItem2)
                # 创建 com 对象
                pfo = pythoncom.CoCreateInstance(
                    shell.CLSID_FileOperation,
                    None,
                    pythoncom.CLSCTX_ALL,
                    shell.IID_IFileOperation,
                )
                pfo.SetOperationFlags(
                    shellcon.FOF_NOCONFIRMATION
                    | shellcon.FOF_SILENT
                    | shellcon.FOF_NOERRORUI
                )
                # 是否给文件名增加日期前缀
                newFileName = None
                if dateName:
                    newFileName = f'{pidlItem.GetFileTime(("{EF6B490D-5CD8-437A-AFFC-DA8B60EE4A3C}",18)).Format("%Y-%m-%d %H-%M-%S")}@{pidlItem.GetDisplayName(shellcon.SHGDN_NORMAL)}'
                # 拷贝文件
                pfo.CopyItem(pidlItem, computerDirItem, newFileName)
                pfo.PerformOperations()


def Test():
    phonePath = r"此电脑/YVR 2/Internal shared storage/Screenshots"
    computerDir = r"D:/Test"
    date_name = True

    folder = GetFolder(phonePath)
    CopyFilesToComputer(folder, phonePath, computerDir, date_name=date_name)


Test()
