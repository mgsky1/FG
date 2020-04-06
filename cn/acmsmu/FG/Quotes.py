'''
@Desc: 三体好句与世界科幻好句
@Author: Martin Huang
@Date: 2020-04-03 19:52:09
@Modify Notes: 
'''
from JsonUtils import JsonUtils
from brainyquote import pybrainyquote
import random
import os
class Quotes:
    def sentence_of_a_day():
        tbsd = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','sentences.json'))
        index = round(random.uniform(0,424))
        threebodySentence = tbsd[index].replace('\r~','\n')
        result = pybrainyquote.get_quotes('Fiction',100)
        index1 = round(random.uniform(0,25))
        return threebodySentence,result[index1]
