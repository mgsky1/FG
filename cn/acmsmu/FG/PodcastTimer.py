'''
@desc:每日检测哈大有声小说24小时内是否有更新
@author: Martin Huang
@time: created on 2020/5/1 8:54
@修改记录:
暂时没有考虑使用datetime.timedelta等日期运算
xm-sign生成算法来自：https://github.com/hkslover/ximalaya
'''
import hashlib
import requests
import time
import random
import nonebot
import os
from Utils.JsonUtils import JsonUtils
from cn.acmsmu.FG.SearchBooks import searchByKeyWords


def xm_md5():
    url = 'https://www.ximalaya.com/revision/time'
    headrer = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
        'Host': 'www.ximalaya.com',
        'Accept-Encoding': 'gzip, deflate, br'}
    try:
        html = requests.get(url, headers = headrer)
        nowTime = str(round(time.time()*1000))
        sign = str(hashlib.md5("himalaya-{}".format(html.text).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + html.text + "({})".format(str(round(random.random()*100))) + nowTime
    except:
        print('错误','请检查网络是否畅通')
        return 0
    return sign

def getPodcastList():
    url = 'https://www.ximalaya.com/revision/user/track?page=1&pageSize=10&keyWord=&uid=7712455&orderType=2'
    header = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        "xm-sign": xm_md5()
    }
    try:
        response = requests.get(url,headers = header)
        jsonStr = response.content.decode('utf-8')
        jsonDict = JsonUtils.jsonStr2Dict(jsonStr)
        return jsonDict
    except:
        print('出错了')
    return None

@nonebot.scheduler.scheduled_job('cron',hour=12)
async def podcastHandler():
    jsonDict = getPodcastList()
    reportPrefix = '@所有人\n'\
                    '大家好，我是FG，第五代电子计算机，这是FG在向群里所有成员广播：\n'\
                    '我探测到群主大屁股老鼠哈哈笑老师在过去24小时内更新了以下作品：\n'
    specialPrefix = '哈哈笑科幻群的首席资源官，XXXXX，你好，我是FG，第五代电子计算机\n' \
                    '我探测到大屁股老鼠哈哈笑老师在过去24小时内更新了以下作品：\n'
    report = ''
    if jsonDict is not None:
        trackList = jsonDict['data']['trackList']
        index = 1
        for item in trackList:
            if item['createTimeAsString'].find('小时前') != -1 or item['createTimeAsString'].find('分钟前') != -1:
                report += str(index)+'、《'+item['title']+'》\n'\
                '所属专辑：【'+item['albumTitle']+'】\n'\
                '收听平台：喜马拉雅，传送门-> https://www.ximalaya.com'+item['trackUrl']+'\n'
                index += 1
                msg = await searchByKeyWords(item['albumTitle'])
                print(msg)
                booksDictList = JsonUtils.json2Dict(
                    os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', 'hhx_books.json'))
                # 自动更新hhx_books.json
                if msg.find('您要查找的有声书在FG的数据库中没有记录') != -1:
                    for eachItem in booksDictList:
                        if eachItem['author'] == '哈哈笑':
                            bookInfo = {'bookName':item['albumTitle'],'platform':['喜马拉雅'],'dPath':[]}
                            eachItem['works'].append(bookInfo)
                            # 写回
                            JsonUtils.json2File(
                                os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', 'hhx_books.json'),
                                booksDictList)
                            break
    if report != '':
        bot = nonebot.get_bot()
        specialReport = specialPrefix + report
        report = reportPrefix + report
        await bot.send_group_msg(group_id=int('123456'), message=report)
        await bot.send_private_msg(user_id=int('123456'),message=specialReport)

print('哈哈笑的有声书更新播报插件加载完成')