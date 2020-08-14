'''
@desc:接入微软小冰对话机器人
@author: Martin Huang
@time: created on 2020/5/2 22:14
@修改记录:
基于该项目进行开发：
https://github.com/BennyThink/realXiaoice
https://blog.csdn.net/agent_bin/article/details/103082046
'''
import requests
import re
import os
import uuid
from nonebot import on_command,CommandSession
from nonebot import on_natural_language,NLPSession,IntentCommand
from Utils.JsonUtils import JsonUtils
from Utils.IOUtils import IOUtils
from aiocqhttp.message import escape

configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','config.json'))

@on_command('xiaoIce')
async def xiaoIce(session:CommandSession):
    chatCount = int(configuration['chatCount'])
    chatCount_c = -1
    chatRemained = -1
    print('msg_type-->'+session.event['message_type'])
    # 为了避免未知隐患，只响应群请求
    if session.event['message_type'] == 'group':
        # session.state.get参数列表？如何获取群号
        print('msg from ->'+str(session.event['group_id']))
        groupInfo = configuration['groupInfo']
        # 如果从配置文件中找到接收消息的群，就更新该群的pkl，如果找不到，就不更新
        # 特征变量
        flag = False
        for eachGroup in groupInfo:
            if int(eachGroup['groupId']) == int(session.event['group_id']):
                flag = True
                dataDict = IOUtils.deserializeObjFromPkl(os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', eachGroup['groupId'], 'var.pkl'))
                chatCount_c = dataDict['chatCount']
                print('chat count used->' + str(dataDict['chatCount']))
                if chatCount_c  > chatCount:
                    report = '今日的互动次数用完啦，明天再来吧~'
                    await session.send(report)
                else:
                    dataDict['chatCount'] += 1
                    IOUtils.serializeObj2Pkl(dataDict,os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', eachGroup['groupId'], 'var.pkl'))

        if not flag:
            return
        message = session.state.get('message')
        imgUrls = session.state.get('imgUrls') if session.state.get('imgUrls') is not None else ''
        print('received--->'+message)
        imgSendList = []
        for eachImg in imgUrls:
            # 存储图片
            img = requests.get(eachImg)
            imgc = img.content
            img.close()
            fileName = str(uuid.uuid1())+'.jpg'
            with open(os.path.join(configuration['serverPath'],'chatImg',fileName),'wb') as f:
                f.write(imgc)
            imgSendList.append(os.path.join(configuration['serverPath'],'chatImg',fileName))
            print('receivedImg--->'+eachImg)
        # 先发送图片，再发送文字
        report = ''
        suffix = ''
        for each in imgSendList:
            report += await getMsgFromXiaoIceFromHTTP(each,'img')
        if message != '':
            report += await getMsgFromXiaoIceFromHTTP(message,'text')
        print('get--->' + report)
        if chatCount_c != -1:
            chatRemained = chatCount - chatCount_c - 1
            if chatRemained <= 10:
                suffix = '\n今日，我还能和您互动'+str(chatRemained)+'次。'
        if report == '':
            report = '[CQ:at,qq=' + str(session.event.user_id) + '] [CQ:face,id=32]'+suffix
        else:
            report = '[CQ:at,qq='+str(session.event.user_id)+']'\
                + ' '+escape(report)+suffix

        await session.send(report)



@on_natural_language
async def _(session:NLPSession):
    # 这里的args是传给xiaoIce函数的参数，在函数中可调用session.get获取
    return IntentCommand(60.00,'xiaoIce',args={'message':session.msg_text,'imgUrls':session.msg_images})

async def getMsgFromXiaoIceFromHTTP(message:str,type:str) -> str:
    url = 'http://127.0.0.1:6789/chat'
    param = {'text':message,'auth':'','type':type}
    response = requests.post(url,param)
    jsonStr = response.content.decode('utf-8')
    jsonDict = JsonUtils.jsonStr2Dict(jsonStr)
    msg = jsonDict['text']
    # 过滤html链接部分，只保留文字
    # re.sub('.+<\/?[\s\S]*?(?:".*")*>.+', '', msg)
    msg = re.sub('<.+>', '', msg)
    msg = msg.replace('小冰', 'FG')
    msg = msg.replace('本冰', '本超级计算机')
    msg = msg.replace('少女', '帅哥')
    msg = msg.replace('姐姐', '帅哥')
    msg = msg.replace('智慧哥哥', '小哥哥/小姐姐')
    return msg

print('微软小冰加载成功')