'''
@desc:
@author: Martin Huang
@time: created on 2020/4/4 14:57
@修改记录:
'''
from nonebot.default_config import *
from Utils.JsonUtils import JsonUtils
import os
configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','config.json'))
API_ROOT_URL = 'http://'+configuration['cqhttpHost']+':'+str(configuration['cqhttpPort'])
API_ROOT = API_ROOT_URL