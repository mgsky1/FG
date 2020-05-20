'''
@desc: FG群文件处理
@author: Martin Huang
@time: created on 2020/4/4 15:04
@修改记录:
'''
import nonebot
import time
import os
from cn.acmsmu.FG import WelcomeMember
from cn.acmsmu.FG import SearchBooks
from cn.acmsmu.FG import ReportTimer
from cn.acmsmu.FG import PodcastTimer
from cn.acmsmu.FG import QAndA
from cn.acmsmu.FG import XiaoIce
from cn.acmsmu.FG import CleaningTimer
from Utils.JsonUtils import JsonUtils
from Utils.IOUtils import IOUtils

configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','config.json'))
groupInfo = configuration['groupInfo']
for each in groupInfo:
    fpath = os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'])
    try:
        dataDict = dict()
        dataDict['flag'] = True
        dataDict['file'] = 'chatA.txt'
        IOUtils.mkdir(fpath)
        IOUtils.serializeObj2Pkl(dataDict, fpath + '/var.pkl')
    except FileExistsError:
        continue
bot = nonebot.get_bot()
print('初始化完成')

@bot.on_message('group')
async def handleGroupMsg(session):
    groupInfo = configuration['groupInfo']
    for each in groupInfo:
        if each['groupId'] == str(session['group_id']):
            # 读取每个群文件夹的pkl
            dataDict = IOUtils.deserializeObjFromPkl(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'],'var.pkl'))
            # 确定flag的值
            flag = dataDict['flag']
            # 确定要往哪一个文件中写入聊天记录
            msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + str(session['user_id']) + '\n' + session['raw_message'] + '\n'
            if flag:
                with open(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'],'chatA.txt'), 'a', encoding='utf-8') as fileA:
                    fileA.write(msg)
            else:
                with open(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'],'chatB.txt'), 'a', encoding='utf-8') as fileB:
                    fileB.write(msg)
            break
