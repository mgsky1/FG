'''
@desc:IO工具类
@author: Martin Huang
@time: created on 2019/5/29 17:46
@修改记录:2019/6/3 => 完成基础骨架
          2019/6/6 => 增加异常处理，新增了删除单个文件，判断目录的方法
          2019/6/7 =>修复BUG
'''
import os
import hashlib
import zipfile
import pickle
from Utils.ConversionUtils import ConversionUtils

class IOUtils:
    #获取文件大小(MB)
    def getFileSize(path):
        try:
            with open(path) as file:
                fileSize = os.path.getsize(file)
                fileSize = ConversionUtils.bytes2Megabytes(fileSize)
                return fileSize
        except FileNotFoundError as reason:
            print('错误：文件不存在！')
            return -1
        except TypeError as reason:
            print('错误：可能是文件损坏！')
            return -1;

    #获取文件md5值
    def getMD5(path):
        if os.path.isdir(path):
            print('错误：路径是一个目录！')
            return
        md5 = hashlib.md5()
        try:
            with open(path,'rb') as file:
                while True:
                    tempSize = file.read(10240)
                    if not tempSize:
                        break
                    md5.update(tempSize)
            return md5.hexdigest()
        except FileNotFoundError as reason:
            print('错误：文件不存在！')

    #递归列举文件(私有静态)
    def __fileRecursionList(path,pList):
        try:
            ret = os.listdir(path)
        except FileNotFoundError as reason:
            print('错误：目录不存在！')
            return
        for each in ret:
            myPath = path + os.sep + each
            if os.path.isdir(myPath):
                pList.append(myPath)
                IOUtils.__fileRecursionList(myPath,pList)
            else:
                pList.append(myPath)
        return pList

    #将目录打包成.zip文件
    def packageDir(dirPath):
        fullPath = dirPath+os.sep+'dirpack.zip'
        pList = []
        pList = IOUtils.__fileRecursionList(dirPath, pList)
        try:
            gzFile =  zipfile.ZipFile(fullPath,'w',zipfile.ZIP_DEFLATED)
        except FileNotFoundError as reason:
            print('错误：文件不存在！可能是目录路径不正确而导致的')
            return
        for each in pList:
            gzFile.write(each)
        gzFile.close()
        return fullPath

    #分割文件，默认块大小为128MB
    def partitionFile(path,blockSize=128):
        if os.path.isdir(path):
            print('错误：应该是一个文件，不是一个目录')
            return
        blockBytes = ConversionUtils.megabytes2Bytes(blockSize)
        blockNum = IOUtils.getPartionBlockNum(path,blockSize)
        toPath = os.path.dirname(path) + os.sep+'MEtemp'
        try:
            os.mkdir(toPath)
            with open(path, 'rb') as orgFile:
                for i in range(int(blockNum)):
                    print('正在分割第' + str(i + 1) + '块')
                    totalBufferSize = 0
                    with open(toPath + '\\PART' + str(i), 'wb') as toFile:
                        while totalBufferSize < blockBytes:
                            #缓冲区大小为1M
                            data = orgFile.read(1048576)
                            if not data:
                                break
                            toFile.write(data)
                            totalBufferSize += 1048576
            print('分割完成！')
        except FileNotFoundError as reason:
            print('错误！无法创建文件！')
        except FileExistsError as reason:
            print('错误！当前目录下MEtemp目录已存在，请删除之！')

    #得到文件的分块数
    def getPartionBlockNum(path,blockSize=128):
        blockBytes = ConversionUtils.megabytes2Bytes(blockSize)
        try:
            totalSize = os.path.getsize(path)
        except FileNotFoundError as reason:
            print('错误：目录不存在！')
            return
        blockNum = 0
        if totalSize % blockBytes != 0:
            blockNum = (totalSize // blockBytes) + 1
        else:
            blockNum = totalSize // blockBytes
        return blockNum

    #将对象序列化进pkl文件
    def serializeObj2Pkl(obj,path):
        try:
            pickle_file = open(path,'wb')
        except FileNotFoundError as reason:
            print('错误！路径不存在！')
        pickle.dump(obj,pickle_file)
        pickle_file.close()

    #将pkl反序列化至对象
    def deserializeObjFromPkl(path):
        try:
            pickle_file = open(path,'rb')
        except FileNotFoundError as reason:
            print('错误！找不到文件！')
        obj = pickle.load(pickle_file)
        return obj

    #根据路径批量删除文件或目录
    def deleteFiles(fileList):
        for index in range(fileList.__len__()-1,-1,-1):
            try:
                if not IOUtils.isDir(fileList[index]):
                    os.remove(fileList[index])
                else:
                    os.rmdir(fileList[index])
            except FileNotFoundError as reason:
                print('错误！找不到文件！')
    #删除单个文件或目录(递归删除)
    def deleteFile(path):
        try:
            if not IOUtils.isDir(path):
                os.remove(path)
            else:
                fList = []
                IOUtils.__fileRecursionList(path,fList)
                if fList.__len__() == 0:
                    os.rmdir(path)
                else:
                    IOUtils.deleteFiles(fList)
                    os.rmdir(path)
        except FileNotFoundError as reason:
            print('错误！找不到文件')
    #合并文件
    def combineFile(blockPath,targetFilePath,blockNum):
        try:
            with open(targetFilePath, 'wb') as file:
                for i in range(blockNum):
                    print('正在合并第' + str(i) + '块')
                    with open(blockPath +os.sep+'PART' + str(i), 'rb') as tmpFile:
                        while True:
                            # 缓冲区大小为1M
                            data = tmpFile.read(1048576)
                            if not data:
                                break
                            file.write(data)
            print('合并完成')
        except FileNotFoundError as reason:
            print('错误！块路径不正确！或文件块丢失！')

    #判断是否为目录
    def isDir(path):
        return True if os.path.isdir(path) else False
    #创建目录
    def mkdir(path):
        try:
            os.mkdir(path)
        except:
            raise FileExistsError
