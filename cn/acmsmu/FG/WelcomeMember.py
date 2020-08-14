
from nonebot import on_notice, NoticeSession
import os.path

print('欢迎插件注册成功！')

@on_notice('group_increase')
async def welcome(session:NoticeSession):
    print('群成员增加')
    print(str(session.event.group_id))
    if session.event.group_id == 460709626:
        msg = '[CQ:at,qq=' + str(session.event.user_id) + ']\n欢迎加入哈哈笑的科幻群\n' \
              '我是第五代超级计算机FG\n' \
              '这是我的自我介绍：\n http://t.cn/A6wV2qSz \n' \
              '我为你准备了一份入群礼物[CQ:face,id=178]\n[CQ:image,file=' + os.path.join(os.getcwd(),'cn','acmsmu','FG','data','assets','welcome.gif') + ']\n' + \
              '想要了解哈哈笑老师播过哪些有声书？可以艾特我，并在后面附上【哈哈笑作品集】(例如@第五代超级计算机FG 哈哈笑作品集)即可。\n' \
              "若想查找哈哈笑老师的某一本有声小说，可以艾特我，并在后面附上【找书+空格+你想找的书名】(例如@第五代超级计算机FG 找书 三体)即可，我会告诉你在线收听平台和下载地址(如果有)。\n" \
              '若想进入哈哈笑的小宇宙(一个可以在线听哈哈笑老师有声书的网站)，可以艾特我，并在后面附上【小宇宙】（例如@第五代超级计算机FG 小宇宙）即可。\n' \
              '祝你在群里玩的愉快~'
        print(msg) 
        await session.send(msg)