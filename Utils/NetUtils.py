'''
@desc:网络工具类
@author: Martin Huang
@time: created on 2019/5/29 18:55
@修改记录:2019/6/3 => 完成基础骨架
          2019/6/6 => 增加异常处理
          2019/6/7 => 增加端口连通性检测
          2019/6/8 => BUG修复
          2020/04/01 => 调用JSON API接口并返回字典
'''
import socket
import select
import ssl
import urllib.request
from threading import Lock
from ConversionUtils import ConversionUtils
from IOUtils import IOUtils
from JsonUtils import JsonUtils
#pycharm使用
#from src.main.Utils.ConversionUtils import *
#from src.main.Utils.IOUtils import *

class NetUtils:

    #传输单个文件
    def transferSigFile(path,port=9000,bufferSize=1,verbose=True):
        server = socket.socket()
        #设置socket选项，SO_REUSEADDR让服务程序结束后立即释放端口，否则操作系统将会持有几分钟，Linux会导致异常
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind(('', port))
        server.listen(5)
        conn, add = server.accept()
        if verbose:
            print('Client IP : %s:%d' % add)
        file_lock = Lock()
        try:
            bufferSize =ConversionUtils.megabytes2Bytes(bufferSize)
            with open(path,'rb') as file:
                file_lock.acquire()
                if verbose:
                    print('连接成功，开始传送文件')
                while True:
                    tdata = file.read(bufferSize)
                    if not tdata:
                        break
                    conn.send(tdata)
            if verbose:
                print('传输了1个文件')
            return 1
        except(FileNotFoundError):
            print("文件不存在！")
            return 0
        finally:
            server.close()
            conn.close()
            if not file_lock:
                file_lock.release()

    #接收单个文件
    def receiveSigFile(path,ip,port=9000,bufferSize=1,verbose=True):
        client = socket.socket()
        while True:
            try:
                client.connect((ip, port))
                break
            except:
                continue
        try:
            bufferSize = ConversionUtils.megabytes2Bytes(bufferSize)
            with open(path,'wb') as file:
                if verbose:
                    print("连接成功，开始接收文件")
                while True:
                    tdata = client.recv(bufferSize)
                    if not tdata:
                        break
                    file.write(tdata)
            if verbose:
                print('成功接收了1个文件')
        finally:
            client.close()

    #获取本机IP地址
    @classmethod
    def getLocalIPAddr(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip=s.getsockname()[0]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return ip

    #检测本机特定端口是否被占用
    def isPortOccupied(port):
        ip = '127.0.0.1'
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
            s.close()
            return True
        except:
            return False

    # 端口转发TCP
    def portMappingTCP(fromIp, fromPort, toPort):
        # 创建socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', toPort))
        server.listen(1)
        readableList = [server]
        writeableList = []
        errorList = [server]
        # 连接客户端(侦听本机某端口)
        client.connect((fromIp, fromPort))
        readableList.append(client)
        errorList.append(client)
        # 端口循环监听
        while True:
            rs, ws, es = select.select(readableList, writeableList, errorList)
            for each in rs:
                # 若当前socket是server
                if each == server:
                    conn, add = server.accept()
                    print('Client IP : %s:%d' % add)
                    readableList.append(conn)
                    continue
                elif each == conn:
                    tdata = each.recv(ConversionUtils.megabytes2Bytes(1))
                    client.send(tdata)
                elif each == client:
                    tdata = each.recv(ConversionUtils.megabytes2Bytes(1))
                    conn.send(tdata)
    # 调用JSON API接口并返回字典
    def jsonApi2Dict(ourl,https=True,**params):
        if https:
            ssl._create_default_https_context = ssl._create_default_https_context
        realURL = ourl+'?'
        itemsList = params.items()
        for each in itemsList:
            realURL += str(each[0]) + '=' +str(each[1])
        try:
            response = urllib.request.urlopen(realURL)
            jsonStr = response.read().decode('utf-8')
            return JsonUtils.jsonStr2Dict(jsonStr)
        except:
            print('出错了！')
            return None

