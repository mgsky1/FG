'''
@desc:问答模块，定死关键词的那种
@author: Martin Huang
@time: created on 2020/5/2 21:41
@修改记录:
'''
from nonebot import on_command,CommandSession
from nonebot import on_natural_language,NLPSession,IntentCommand

@on_command('getAudioBookWebside',aliases=('有声书'))
async def getAudioBookWebside(session:CommandSession):
    report = '[CQ:at,qq='+str(session.event.user_id)+']'\
             +' 聆听他人故事，精彩自己人生，欢迎进入哈哈笑的有声世界。https://www.hhx.xyz'
    await session.send(report)

@on_command('whoAmI',aliases=('你是谁','你叫什么名字','你好'))
async def whoAmI(session:CommandSession):
    report = '[CQ:at,qq='+str(session.event.user_id)+']'\
             +' 我是第五代超级计算机FG~很高兴认识你！'
    await  session.send(report)

@on_natural_language(keywords={'你是谁','名字','你好'})
async def whoAmI_NLP_Process(session:NLPSession):
    return IntentCommand(60.00,'whoAmI')

print('Q&A模块加载成功！')