
from nonebot import on_notice, NoticeSession
from Utils.NetUtils import NetUtils

print('欢迎插件注册成功！')
# addr = 'http://hhx.test.cn/4fb2cb55de07f6e6.gif'
# url1 = NetUtils.jsonApi2Dict('https://api.d5.nz/api/dwz/tcn.php',https=True,url=addr)
# if url1['code'] == '200':
#     url1 = url1['url']
# else:
#     url1 = ''
url1 = 'http://suo.im/6kfsGK'

@on_notice('group_increase')
async def welcome(session:NoticeSession):
    print('群成员增加')
    print(str(session.event.group_id))
    if session.event.group_id == 460709626:
        msg = '[CQ:at,qq='+str(session.event.user_id)+']\n欢迎加入哈哈笑的科幻群\n'\
            '我是第五代超级计算机FG\n'\
            '我为你准备了一份入群礼物[CQ:face,id=178]\n'+url1+'\n'+\
            '放心，不是什么奇怪的东西，是一张动图，请放心点击~\n想要获取哈哈笑老师的全部有声书，可以艾特我，并在后面附上【有声书】(例如@第五代超级计算机FG 有声书)即可\n'\
            "若想查找哈哈笑老师的某一本有声小说，可以艾特我，并在后面附上【找书 你想找的书名】(例如@第五代超级计算机FG 找书 三体)即可，我会告诉你在线收听平台和下载地址(如果有)，返回下载地址时，我需要连接网络，可能速度会有些慢，请您谅解~\n"\
            '祝你在群里玩的愉快~'
        print(msg) 
        await session.send(msg)