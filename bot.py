'''
@desc: FG主入口
@author: Martin Huang
@time: created on 2020/4/4 14:57
@修改记录:
'''
from os import path
import nonebot
import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'cn', 'acmsmu'),
        'cn.acmsmu'
    )
    nonebot.run(host='127.0.0.1', port=8080)