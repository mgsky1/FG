'''
@Desc: 三体好句与科幻小说推荐
@Author: Martin Huang
@Date: 2020-04-03 19:52:09
@Modify Notes: 
'''
from Utils.JsonUtils import JsonUtils
import random
import os
class ExtraFunction:
    def quotesAndBooks():
        tbsd = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','sentences.json'))
        index = round(random.uniform(0,424))
        threebodySentence = tbsd[index].replace('\r~','\n')
        index1 = round(random.uniform(1, 117))
        index1 = '{:0>5d}'.format(index1)
        recommend_books = JsonUtils.json2Dict(os.path.join(os.getcwd(),'cn','acmsmu','FG','data','Books','BC'+index1+'.json'))
        if len(recommend_books['authors']) == 0:
            author_info = '无名氏'
        else:
            author_info = recommend_books['authors'][0]['name']
        recommend = '书名：《'+recommend_books['title']+'》\n'\
                    '类型：'+recommend_books['type']+'\n'\
                    '作者：'+author_info+'\n'\
                    '出版社：'+recommend_books['publisher']+'\n'\
                    '出版时间：'+recommend_books['pubDate']
        return threebodySentence,recommend
