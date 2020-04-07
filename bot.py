'''
@desc: FG主入口
@author: Martin Huang
@time: created on 2020/4/4 14:57
@修改记录:
'''
import os
from Utils.JsonUtils import JsonUtils
import nonebot
import config

if __name__ == '__main__':
    configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', 'config.json'))
    nonebot.init(config)
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'cn', 'acmsmu'),
        'cn.acmsmu'
    )
    nonebot.run(host=configuration['nonebotHost'], port=configuration['nonebotPort'])