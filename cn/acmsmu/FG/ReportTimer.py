'''
@desc: FG定时发布每日总结
@author: Martin Huang
@time: created on 2020/4/4 16:22
@修改记录:
        2020/4/12 => 修改定时器模式
'''
import nonebot
import os
from cn.acmsmu.FG import DailyConclusion
from Utils.JsonUtils import JsonUtils
from Utils.IOUtils import IOUtils

async def handleTimer(timerName,groupId):
    dataDict = IOUtils.deserializeObjFromPkl(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',groupId, 'var.pkl'))
    flag = dataDict['flag']
    clu = DailyConclusion.DailyConlusion(groupId)
    report = clu.generateReport()
    #print(timerName+'的每日总结为\n'+report)
    await bot.send_group_msg(group_id=int(groupId), message=report)
    if flag:
        dataDict['flag'] = False
        dataDict['file'] = 'chatB.txt'
        IOUtils.serializeObj2Pkl(dataDict,os.path.join(os.getcwd(),'cn','acmsmu','FG','data',groupId, 'var.pkl'))
        IOUtils.deleteFile(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',groupId, 'chatA.txt'))
    else:
        dataDict['flag'] = True
        dataDict['file'] = 'chatA.txt'
        IOUtils.serializeObj2Pkl(dataDict,os.path.join(os.getcwd(),'cn','acmsmu','FG','data',groupId, 'var.pkl'))
        IOUtils.deleteFile(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',groupId, 'chatB.txt'))

bot = nonebot.get_bot()
configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','config.json'))
print(configuration)
groupInfo = configuration['groupInfo']
for each in groupInfo:
    hour = each['beginHour']
    minutes = each['beginMinutes']
    nonebot.scheduler.add_job(handleTimer, 'cron',hour=hour,minute=minutes,args=[each['timer'],each['groupId']])
    print('定时器' + each['timer'] + '定时任务添加成功!')