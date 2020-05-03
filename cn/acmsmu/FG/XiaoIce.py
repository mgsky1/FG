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
from nonebot import on_command,CommandSession
from nonebot import on_natural_language,NLPSession,IntentCommand
from Utils.JsonUtils import JsonUtils
from aiocqhttp.message import escape

@on_command('xiaoIce')
async def xiaoIce(session:CommandSession):
    print('msg_type-->'+session.event['message_type'])
    # 为了避免未知隐患，只响应群请求
    if session.event['message_type'] == 'group':
        message = session.state.get('message')
        print('received--->'+message)
        report = await getMsgFromXiaoIceFromHTTP(message)
        print('get--->' + report)
        report = '[CQ:at,qq='+str(session.event.user_id)+']'\
               + ' '+escape(report)
        await session.send(report)



@on_natural_language
async def _(session:NLPSession):
    return IntentCommand(60.00,'xiaoIce',args={'message':session.msg_text})

async def getMsgFromXiaoIceFromHTTP(message) -> str:
    url = 'http://127.0.0.1/chat'
    param = {'text':message,'auth':''}
    response = requests.post(url,param)
    jsonStr = response.content.decode('utf-8')
    jsonDict = JsonUtils.jsonStr2Dict(jsonStr)
    msg = jsonDict['text']
    # 过滤html链接部分，只保留文字
    # re.sub('.+<\/?[\s\S]*?(?:".*")*>.+', '', msg)
    msg = re.sub('<.+>', '', msg)
    return msg

print('微软小冰加载成功')