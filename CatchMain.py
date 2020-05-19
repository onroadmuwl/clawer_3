# encoding:utf-8--
import requests
from lxml import etree
from collections import OrderedDict
import pandas as pd
import os
import time
import random


class WEIBO():
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36'
        ,
        'cookie': 'SCF=Ap-E4_z0nkNkTlPtjW4QS3RvaPGi6OfN2IUVhnB16Ht6LHAri5lvH2SZeuxTXy1vWulTg1NGcxIFEaEsWwzb7HA.; SUHB=0N21KPnyF0wHNB; SUB=_2A25wt2nEDeRhGeFN6VoQ9C7Kwz-IHXVQWHeMrDV6PUJbkdANLUXwkW1NQFhynxDZN2psXQGsR8jm7U1R_-tQAMqK'

    }

    cookie = {
        'Cookie': 'UOR=www.sogou.com,open.weibo.com,www.baidu.com; wvr=6; SINAGLOBAL=7321380035840.548.1569900191275; ULV=1575902967567:6:4:4:5210561418544.486.1575902967547:1575879211547; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW.9IalbLWd3LhvmeoZ6Gsd5JpX5oz75NHD95QNe0zReKB7Son0Ws4DqcjSqc8XqcyLMLY41hM4entt; SUB=_2A25wt2nEDeRhGeFN6VoQ9C7Kwz-IHXVQWHeMrDV8PUJbkNANLWX3kW1NQFhynyHUx2wvxRbeC5XMxoduFw3ws2Wu; YF-V5-G0=27518b2dd3c605fe277ffc0b4f0575b3; _s_tentry=-; Apache=5210561418544.486.1575902967547; YF-Page-G0=02467fca7cf40a590c28b8459d93fb95|1575903019|1575903011; wb_view_log_7328140683=1297*7301.4800050258636474'
    }

    def __init__(self):  # 初始化
        self.weibo_num = 0
        self.weibo = []

    def deal_html(self, keyword, num):  # 处理html
        url = str(
            "https://s.weibo.com/hot?q=%23" + keyword + "%23&xsort=hot&suball=1&tw=hotweibo&Refer=weibo_hot&page=" + str(
                num))
        html = requests.get(url, cookies=self.cookie).content
        selector = etree.HTML(html)
        return selector

    def pagenum(self,keyword,num):#防止越界
        select=self.deal_html(keyword,num)
        word=select.xpath('//*[@id="pl_feedlist_index"]/div[2]/div/p/text()')
        if word==[]:
            return True
        else:
            return False

    def get_info(self, keyword, num):  # 数据项获取，处理并加入元组
        selector = self.deal_html(keyword, num)
        name = selector.xpath('//div[@class="content"]/p[@class="txt"][1]/@nick-name')  # 名称
        content = selector.xpath('//div[@action-type="feed_list_item"]/div/div[1]/div[2]/p[1]')
        contents = []  # 内容
        for i in content:
            i = i.xpath('normalize-space(string(.))')  # 去除换行和空格
            contents.append(i)
        times = selector.xpath('//p[@class="from"]/a[1]')
        timess = []  # 时间
        for i in times:
            i = i.xpath('normalize-space(text())')
            i = i[0:i.find(u'日') + 1]
            timess.append(i)
        transpound = []  # 转发
        tran = selector.xpath('//div[@class="card-act"]/ul/li[2]/a/text()')
        for i in tran:
            i = i[3:]
            transpound.append(i)
        review = []  # 评论
        rev = selector.xpath('//div[@class="card-act"]/ul/li[3]/a/text()')
        for i in rev:
            i = i[3:]
            review.append(i)
        like = selector.xpath('//div[@class="card-act"]/ul/li[4]/a/em/text()')  # 点赞
        WeiboTuple = []

        for i in range(0, len(like)):
            weibo = OrderedDict()
            weibo['name'] = name[i]
            weibo['content'] = contents[i]
            weibo['date'] = timess[i]
            weibo['transpound'] = transpound[i]
            weibo['review'] = review[i]
            weibo['like'] = like[i]
            WeiboTuple.append(weibo)
        return WeiboTuple

    def write_print_csv(self, filename, keyword, num):  # 写入csv文件
        weiboContent = self.get_info(keyword, num)
        print(weiboContent)
        if os.path.exists(filename) == False:
            DataFrame = pd.DataFrame(weiboContent,
                                     columns=['name', 'content', 'date', 'transpound', 'review', 'like'])
            DataFrame.to_csv(filename, index=False, sep=',')
        if os.path.exists(filename) == True:
            DataFrame = pd.DataFrame(weiboContent,
                                     columns=['name', 'content', 'date', 'transpound', 'review', 'like'])
            DataFrame.to_csv(filename, mode='a', header=False, index=False, sep=',')

    def get_keyword(self):
        frame = pd.read_csv('keywordDrop_duplicate.csv')
        return frame

    def getPages(self, keyword, filename, begin, count):
        for i in range(begin, 51):  # 每个关键词下面爬取三十页微博
            if self.pagenum(keyword,i)==True:
                print("第" + str(count) + "条关键词（" + keyword + "),第" + str(i) + "页。")
                self.write_print_csv(filename, keyword, i)
            else:
                continue

    def start(self, filename, begin):
        frame = self.get_keyword()
        print(frame)
        keywords = frame['topic']
        number = len(keywords)
        for k in range(begin, number):
            self.getPages(keyword=keywords[k], filename=filename, begin=1, count=k + 1)


if __name__ == '__main__':
    d = WEIBO()
    d.start("domo.csv", 0)
'''except:
                print("休息一下！(getPage)")
                time.sleep(random.randint(10,15))
                error = i
                while(begin<30):
                    self.getPages(keyword,filename,begin=error,count=count)
                continue'''

''' except:
                print("休息一下！(start)")
                error = k
                self.start(filename,error)
                continue'''