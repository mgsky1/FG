'''
@Desc:textRank关键词抽取示例代码
@Author: huangzhiyuan
@Time: 2020/5/18 8:20 下午
@Modify Notes:
共现关系
https://blog.csdn.net/tian_panda/article/details/81127034?utm_source=blogxgwz8
'''
import numpy as np
import networkx as nx
import jieba.posseg
import logging
if __name__ == '__main__':
    # content = '蓝太阳在最大的状态维持了约半分钟，这期间它很稳定，加上此时笼罩一切的诡异的宁静，它居然在这短暂的时间给人一种永恒感，' \
    #            '放佛自世界诞生之日起就在那里似的。蓝太阳使西边已落下去一半的夕阳黯然失色，整个戈壁都淹没在它的蓝光中，使这个世界变得' \
    #            '陌生而怪异。这是一个冷太阳，人们即使在近处也感觉不到它的任何热量。'
    # content = '在水滴尾部的尖端，出现了一个蓝色的光环，那个光环开始很小，但很亮，使周围的一切笼罩在蓝光中，'\
    #             '它急剧扩大，颜色由蓝变黄最后变成红色，仿佛光环不是由水滴产生的，而是前者刚从环中钻出来一样'
    content = '死星平静地燃烧了四亿八千万年，它的生命壮丽辉煌，但冷酷的能量守恒定律使它的内部不可避免地'\
              '发生了一些变化:核火焰消耗着氢，而核聚变的产物氦，沉积到星体的中心并一点点地累积起来。这变化'\
              '对于拥有巨量物质的死星来说是极其缓慢的，人类的整个历史对它来说不过是弹指一挥间。但四亿八千万'\
              '年的消耗终于产生了它能感觉到的结果——惰性较大的氦已沉积到了相当的数量，它那曾是能量源泉的心'\
              '脏渐渐变暗，死星老了。'
    jieba.load_userdict('Resources/myDict.txt')
    content_seged = jieba.posseg.cut(content.strip())
    index = 0
    wordMap = dict()
    wordMap1 = dict()
    totalWordList = []
    stopWords = []
    '''
    单词列表构建
    去除停顿词的列表用于构建无向不带权图（图顶点）
    名词列表用于关键词筛选
    '''
    with open('TextRank4ZH/textrank4zh/stopwords.txt') as f:
        for eachLine in f:
            stopWords.append(eachLine)
    for x in content_seged:
        if x.flag not in ['uj','x'] and x.word not in stopWords:
            totalWordList.append(x.word)
        if str(x.flag).find('n') != -1 and len(x.word) > 1 and x.word not in wordMap.keys():
            wordMap[x.word] = index
            wordMap1[index] = x.word
            index += 1
    windowSize = 2
    d = 0.85
    M = np.zeros((len(wordMap),len(wordMap)))
    R = np.ones((len(wordMap),1))
    # R = np.asarray([1/len(wordMap) for i in range(len(wordMap))]).reshape(len(wordMap),1)
    R1 = np.array(R,copy=True)
    # N = np.asarray([1/len(wordMap) for i in range(len(wordMap))]).reshape(len(wordMap),1)
    N = np.asarray([1-d for i in range(len(wordMap))]).reshape(len(wordMap),1)
    wordList = list(wordMap.keys())

    '''
    利用共现关系构造图
    '''
    index = 0
    for word in totalWordList:
        wt = [word]
        for i in range(1,windowSize):
            try:
                wt.append(totalWordList[index+i])
            except:
                break
        if len(wt) == windowSize:
            for i in range(len(wt)):
                for j in range(i+1,len(wt)):
                    if wt[i] in wordList and wt[j] in wordList:
                        M[wordMap[wt[i]]][wordMap[wt[j]]] = 1
                        M[wordMap[wt[j]]][wordMap[wt[i]]] = 1
        index += 1

    # 调库PageRank
    nx_graph = nx.from_numpy_matrix(M)
    scores = nx.pagerank(nx_graph, alpha=d)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    sorted_words = []
    for index, score in sorted_scores:
        item = (score, wordMap1[index])
        sorted_words.append(item)
    print('使用NetworkX库：')
    print(sorted_words)

    # 自己写的PageRank（由于边没有权重，故退化为PageRank）
    total = M.sum(axis=1)
    for i in range(len(wordMap)):
        for j in range(len(wordMap)):
            if M[j][i] == 1:
                M[j][i] = 1/total[i]

    count = 0
    while 1:
        # R = np.dot(M,R)
        # R = np.dot(np.hstack((R,N)),np.asarray([d,1-d]).reshape(2,1))
        R = d * np.dot(M,R) + N
        if np.all(np.absolute(R-R1) < 1e-4):
            break
        R1 = np.array(R,copy=True)
        count += 1

    logging.critical('Iter num: '+str(count))
    res = []
    for each in wordMap.keys():
        res.append((float(R[wordMap[each]]),each))

    res = sorted(res,reverse=True)
    print('使用论文的公式：')
    for each in res:
        print(each)