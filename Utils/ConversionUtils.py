'''
@desc:各种数值转换工具类
@author: Martin Huang
@time: created on 2019/5/29 17:57
@修改记录:2019/6/3 => 完成基础骨架
'''
class ConversionUtils:
    #将Byte(B)转换为Megabyte(M)
    def bytes2Megabytes(bytesNum):
        return bytesNum / 1024 / 1024

    #将Megabyte(M)转换为Byte(B)
    def megabytes2Bytes(megaNum):
        return megaNum * 1024 * 1024