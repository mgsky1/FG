'''
@desc:各种数值转换工具类
@author: Martin Huang
@time: created on 2019/5/29 17:57
@修改记录:2019/6/3 => 完成基础骨架
          2020/4/12 => 增加日期间秒数计算
'''
import time
class ConversionUtils:
    #将Byte(B)转换为Megabyte(M)
    def bytes2Megabytes(bytesNum):
        return bytesNum / 1024 / 1024

    #将Megabyte(M)转换为Byte(B)
    def megabytes2Bytes(megaNum):
        return megaNum * 1024 * 1024

    #计算两个日期间的秒数(取整)
    # 输入的时间格式为%Y-%m-%d %H:%M:%S eg.2016-03-20 11:45:39 如果是个位数需要补0
    def dates2Interval(beginTime,endTime):
        beginTime = time.mktime(time.strptime(beginTime,'%Y-%m-%d %H:%M:%S'))
        endTime = time.mktime(time.strptime(endTime,'%Y-%m-%d %H:%M:%S'))
        if beginTime > endTime:
            t = beginTime
            beginTime = endTime
            endTime = t
        interval = endTime - beginTime
        return round(interval)