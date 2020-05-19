#encoding:utf-8--
from lxml import etree
import requests
import pandas as pd
from collections import OrderedDict
import os
class WEIBO():
    cookie={

        'Cookie':'SINAGLOBAL=17655527886.00688.1572186625833; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW.9IalbLWd3LhvmeoZ6Gsd5JpX5oz75NHD95QNe0zReKB7Son0Ws4DqcjSqc8XqcyLMLY41hM4entt; ALF=1575987614; SUB=_2A25wzGzODeRhGeFN6VoQ9C7Kwz-IHXVQT3SGrDV8PUJbkNANLXPNkW1NQFhyn37EHmCtD6n1tRmBFrqECrXHgn8w; _s_tentry=-; Apache=2524398874551.1836.1575808891403; ULV=1575808891417:5:1:1:2524398874551.1836.1575808891403:1573388661513'

    }
    #cookie免验证登录
    def get_weibo_newage(self,KeyWord,Num):
        url = 'https://s.weibo.com/topic?q=%s&pagetype=topic&topic=1&Refer=weibo_topic&page=%d'%(KeyWord,Num)
        html = requests.get(url).content#解析网页，获取网页内容
        selector = etree.HTML(html)#得到element对象
        WeiboHeader=selector.xpath('//div[@class="card-wrap s-pg16"]//div[@class="info"]/div/a/text()')#爬取相关文本内容
        WeiboReader = selector.xpath('//div[@class="card-wrap s-pg16"]//div[@class="info"]/p[2]/text()')  # 爬取相关文本内容
        Original=[WeiboReader,WeiboHeader]
        return Original
    def deal_format(self,keyword,num):#整理相关内容的格式，规范化
        WeiboReader=self.get_weibo_newage(keyword,num)[0]
        WeiboHead=self.get_weibo_newage(keyword,num)[1]
        WeiboReader_1=[]
        WeiboReader_2=[]
        WeiboHeader=[]
        for i in WeiboHead:
            i=i[1:len(i)-1]
            WeiboHeader.append(i)
        for i in WeiboReader:
            row=i[0:i.find(u'讨')]
            if '万' in row:
                row = row.replace('万', '')
                if '.' in row:
                    row = row.replace('.', '')
                    row = row + '000'
                else:
                    row = row + '0000'
            if '亿' in row:
                row = row.replace('亿', '')
                if '.' in row:
                    row = row.replace('.', '')
                    row = row + '0000000'
                else:
                    row = row + '00000000'
            WeiboReader_1.append(row)
            rows=i[i.find(u' '):i.find(u'阅')]
            if '万' in rows:
                rows = rows.replace('万', '')
                if '.' in rows:
                    rows = rows.replace('.', '')
                    rows = rows + '000'
                else:
                    rows = rows + '0000'
            if '亿' in rows:
                rows = rows.replace('亿', '')
                if '.' in rows:
                    rows = rows.replace('.', '')
                    rows = rows + '0000000'
                else:
                    rows = rows + '00000000'
            WeiboReader_2.append(rows)
        DealData=[WeiboHeader,WeiboReader_1,WeiboReader_2]
        return DealData
    def getTuple(self,keyword,num):#变成数组，方便写入csv
        WeiboHeader=self.deal_format(keyword,num)[0]
        WeiboReader_1=self.deal_format(keyword,num)[1]
        WeiboReader_2=self.deal_format(keyword,num)[2]
        print(WeiboHeader)
        weiboContent = []
        for i in range(0,len(WeiboHeader)):
            weibo = OrderedDict()
            weibo['topic']=WeiboHeader[i]
            weibo['DiscussNum']=WeiboReader_1[i]
            weibo['ReadNum']=WeiboReader_2[i]
            weiboContent.append(weibo)
        print(weiboContent)
        return weiboContent
    def write_csv(self,filename,keyword,num):#写入csv文件
        weiboContent=self.getTuple(keyword,num)
        if os.path.exists(filename)==False:
            DataFrame = pd.DataFrame(weiboContent,
                                     columns=['topic','DiscussNum','ReadNum'])
            DataFrame.to_csv(filename, index=False, sep=',')
        if os.path.exists(filename)==True:
            DataFrame = pd.DataFrame(weiboContent,
                                     columns=['topic', 'DiscussNum', 'ReadNum'])
            DataFrame.to_csv(filename, mode='a', header=False,index=False,sep=',')

    def start(self,filename,keyword,begin):#开启程序
        for i in range(begin,51):
            try:
                print('第',str(i),'页关键词')
                self.write_csv(filename,keyword,i)
            except:#微博对于爬虫极其友好，不用限速
                #但有时会出现意外，突然爬不到数据，可以采用手工操作从断点接着爬取的方式，
                # 我采用的是从断点接着自动重启程序
                error=i
                self.start(filename,keyword,begin=error)

if __name__=='__main__':
    k=WEIBO()
    k.start('domos.csv','香港',1)