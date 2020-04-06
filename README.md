# FG 

## Summary

一个基于Nonebot的QQ群每日总结生成插件，可以根据每日的聊天信息生成每日热词，并以词云方式可视化展示
>  注：**此插件暂时只针对酷Q air设计**

## Technology

这是一个简单的文本挖掘实验，首先会获取群内聊天记录进行数据预处理，包括Q号什么的进行数据脱敏。

FG的核心是一个称为**TextRank**的算法，它源自于Google的PageRank，基本思想采用类似投票机制来找出一篇文章的关键词，由于我不是做NLP的，所以是调库，最后会返回关键词+权重，权重是已经按降序排列过的，所以可以直接用来生成词云。


## Dependency

> * Python >= 3.7
> * nonebot >= 1.5.0 (需安装定时器插件，具体可见官方文档)
> * wordcloud >= 1.6.0
> * textrank4zh >= 0.3
> * [CQHTTP 酷Q插件](https://cqhttp.cc/docs/4.14/#/) >=4.8

## Configuration
需要在两个地方进行配置
> * config.py
> * cn/acmsmu/FG/data/config.json

### config.py

```python
from nonebot.default_config import *
API_ROOT = 'http://127.0.0.1:5700'  # 这里 IP 和端口应与 CQHTTP 配置中的 `host` 和 `port` 对应
```

### config.json

下面是一个样例

```json
{
    "serverPath":"", //存放图片的目录，要保证能够通过域名或ip+端口号的形式访问。由于air不能发图，所以图片都是通过链接发送的。注意，一定要以反斜杠结尾！
    "domain":"",//域名，如果没有的话可以填写ip+端口号
    "reqType":"http",//图片网站请求类型,http或者https
    "windowSize":5,//设置TextRank算法的窗口大小，默认为5
    "keyWordLen":3,//小于此长度的词将不会被显示，默认为3
    "keyWordNum":50,//热词数量，默认50
    "fontPath":"C:/Windows/Fonts/msyh.ttc",//字体，用于生成词云
    "groupInfo":[//群信息数组
        {
            "timer":"timer1",//定时器名称
            "interval":60,//定时时间，以秒为单位
            "groupId":""//群号
        }
    ],
    "wcImg":[//用于生成词云的图片数组
        {
            "desc":"刘慈欣",//图片描述
            "fileNameO":"lcx.jpg",//原始图片，用于展示，存放位置一定要在前面定义的serverPath下
            "fileNameU":"lcx.png"//使用图片，即真正用来生成词云的图片，要求除了主体之外，背景为白色，存放位置一定要在前面定义的serverPath下
        }
    ],
    "template":[{//总结模板数组，一个群要定义两个，一个正常模式，另外一个用于没有热词生成时使用，模板里出现的time，content等非数字标签请不要修改，但是位置可以随意，并没有要求要全部出现，出现其中的某些也是可以的
        "groupId":"",//群号
        "content":[
        {
            "0":"@所有人",
            "1":"大家好，我是FG，第五代电子计算机",
            "2":"这是FG在向群里所有成员广播:",
            "3":"欢迎每晚XX点锁定XXX群，收看由每日聊天信息自动生成的每日热词",
            "time":"收入时间为:{string}到{string}，今日的热点关键词为",//time标签中一定要有两个{string}，出现位置随意
            "content":"{string}",//用于显示热点关键词，建议不做改动，但是出现位置随意
            "wcImg":"今日词云：{img}",//一定要有{img}
            "wcImgDesc":"今日背景图为 {string}",//一定要有{string}
            "oriImg":"原图：{img}",//一定要有{img}
            "9":"热词生成的宗旨是为您节约时间，让您无需时时在线就能了解动态",
            "10":"如果您对此感兴趣，欢迎每晚XX点进入XXX群~再见！"
        },
        {
            "0":"@所有人",
            "1":"大家好，我是FG，第五代电子计算机",
            "2":"这是FG在向群里所有成员广播:",
            "3":"欢迎每晚XX点锁定XXX群，收看由每日聊天信息自动生成的每日热词",
            "4":"今日群里不够热闹，因此今日无热词",
            "5":"热词生成的宗旨是为您节约时间，让您无需时时在线就能了解动态",
            "6":"如果您对此感兴趣，欢迎每晚XX点进入XXX群~再见！"
        }]
    }]
}
```
## Run
配置完成后，在根目录下运行
```python
python3 bot.py
```

## ScreenShots

![](https://blog.acmsmu.cn/wp-content/uploads/2020/04/20200406235704.jpg)

## Note
FG也即Five Generation，第五代超级计算机，灵感来自于刘慈欣长篇科幻，《超新星纪元》