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
from aiocqhttp.message import escape

configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','config.json'))

@on_command('xiaoIce')
async def xiaoIce(session:CommandSession):
    print('msg_type-->'+session.event['message_type'])
    # 为了避免未知隐患，只响应群请求
    if session.event['message_type'] == 'group':
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
        for each in imgSendList:
            report += await getMsgFromXiaoIceFromHTTP(each,'img')
        if message != '':
            report += await getMsgFromXiaoIceFromHTTP(message,'text')
        print('get--->' + report)
        if report == '':
            report = '[CQ:at,qq=' + str(session.event.user_id) + '] [CQ:face,id=32]'
        else:
            report = '[CQ:at,qq='+str(session.event.user_id)+']'\
                + ' '+escape(report)
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
    msg = msg.replace('小冰','FG')
    msg = msg.replace('本冰','本超级计算机')
    return msg

print('微软小冰加载成功')