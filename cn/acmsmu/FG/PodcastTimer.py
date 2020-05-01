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
from Utils.JsonUtils import JsonUtils


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
    report = ''
    if jsonDict is not None:
        trackList = jsonDict['data']['trackList']
        index = 1
        for item in trackList:
            if item['createTimeAsString'].find('小时前') != -1:
                report += str(index)+'、《'+item['title']+'》\n'\
                '所属专辑：【'+item['albumTitle']+'】\n'\
                '收听平台：喜马拉雅，传送门-> https://www.ximalaya.com/'+item['trackUrl']+'\n'
                index += 1
    if report != '':
        bot = nonebot.get_bot()
        report = reportPrefix + report
        await bot.send_group_msg(group_id=int('460709626'), message=report)

print('哈哈笑的有声书更新播报插件加载完成')