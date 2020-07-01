'''
@desc: 定时清理垃圾
@author: Martin Huang
@time: created on 2020/5/9 16:21
@修改记录:
'''

import nonebot
import os
from Utils.JsonUtils import JsonUtils
from Utils.IOUtils import IOUtils

configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','config.json'))

@nonebot.scheduler.scheduled_job('cron',hour=17,minute=50)
async def cleaningXiaoIce():
    IOUtils.deleteFile(os.path.join(configuration['serverPath'],'chatImg'))
    print('小冰聊天信息图片清理完成')
    groupInfo = configuration['groupInfo']
    for each in groupInfo:
        dataDict = IOUtils.deserializeObjFromPkl(os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', each['groupId'], 'var.pkl'))
        dataDict['chatCount'] = 0
        IOUtils.serializeObj2Pkl(dataDict, os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', each['groupId'], 'var.pkl'))
    print('小冰聊天计数清零已完成')

@nonebot.scheduler.scheduled_job('cron',hour=17,minute=0)
async def cleaningWordCould():
    IOUtils.deleteFile(os.path.join(configuration['serverPath'],'wc'))
    print('词云图片清理完成')

print('自动清理插件加载完成！')
