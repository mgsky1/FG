'''
@desc:查找哈哈笑的有声书地址和下载地址
@author: Martin Huang
@time: created on 2020/4/27 9:26
@修改记录:
这里会采用新的语法形式，主要是能让开发者看清函数的参数是什么，以及函数的返回值是什么
'''
from nonebot import on_command,CommandSession
from Utils.JsonUtils import JsonUtils
from Utils.NetUtils import NetUtils
import os
import re

async def searchByKeyWords(key:str) -> str:
    booksDictList = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','hhx_books.json'))
    res = []
    for eachItem in booksDictList:
        for works in eachItem['works']:
            if works['bookName'].find(key) != -1:
                res.append(works)
    if len(res) == 0:
        return '您要查找的有声书在FG的数据库中没有记录，可能由于以下原因:\n'\
                +'1、真的找不到\n'\
                +'2、召唤我的姿势不对，请确认暗号【@第五代超级计算机FG 书名】'\
                +' 例如【@第五代超级计算机FG 三体】'

    if len(res) > 5:
        report = 'FG找到的内容有点多，请确认要查找的有声书后再次艾特我进行搜书\n'
        for each in res:
            report += each['bookName']+'\n'
        return report
    else:
        report = 'FG已为您检索到以下内容：\n'
        for each in res:
            report += '书名：《'+each['bookName']+'》\n'
            if len(each['platform']) != 0:
                report += '收听平台:\n'
                for eachPlatform in each['platform']:
                    report += eachPlatform + '\n'
            if len(each['dPath']) != 0:
                report += '下载链接:\n'
                for eachLink in each['dPath']:
                    if re.match('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',eachLink) is not None:
                        url = NetUtils.jsonApi2Dict('https://api.d5.nz/api/dwz/tcn.php',https=True,url=eachLink)
                        if url['code'] == '200':
                            report += url['url']+'\n'
                        else:
                            report += 'FG与数据中心的通信出现了网络错误，请稍后再试\n'
                    else:
                        report += eachLink +'\n'
    return report

@on_command('search',aliases=('找书'))
async def search(session:CommandSession):
    key = session.get('key',prompt='您是想查找哈哈笑的哪本有声书呢？')
    report = await searchByKeyWords(key)
    await session.send(report)

@search.args_parser
async def _(session:CommandSession):
    args = session.current_arg_text.strip()
    if session.is_first_run:
        if args:
            session.state['key'] = args
        return

    if not args:
        session.pause("FG没有接收到您想查询的书名呢...")

    session.state[session.current_key] = args
print('搜书插件加载完成！')
