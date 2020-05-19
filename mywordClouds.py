import pandas as pd
import numpy as np
from wordcloud import WordCloud
from PIL import Image
import jieba

class Deal():
    def readframekeyword(self,):
        frame=pd.read_csv('keywordDrop_duplicate.csv',header=0)
        return frame['topic']
    def readframeName(self):
        frame=pd.read_csv('data_improveutf8.csv',header=0)
        frames=frame[(frame['like']>=10000)]
        return frames['name']
    def getMouthKey_1_2(self,num):
        frame = pd.read_csv('data_improveutf8.csv', header=0)
        word=str(num)+'月'
        frames = frame[frame['date'].str.contains(word)]
        frames_1=[]
        for row in frames.itertuples():#按行查找
            if getattr(row, 'date')[1]=='月':
                frames_1.append(getattr(row, 'content'))
        return frames_1
    def getMouthKey(self,num):
        frame = pd.read_csv('data_improveutf8.csv', header=0)
        word=str(num)+'月'
        frames = frame[frame['date'].str.contains(word)]
        return frames['content']
    def getWeiboUserWord(self,Username):
        frame = pd.read_csv('data_improveutf8.csv', header=0)
        frames=frame[frame['name']==Username]
        return frames['content']
    def wordClouds(self,filelist,file):
        row_titles=filelist
        row_title_list=[]
        for row_t in row_titles:
            row_t=str(row_t)
            row_t=row_t.replace('展开',' ')
            row_t = row_t.replace('全文', ' ')
            row_t = row_t.replace('微博', ' ')
            row_t = row_t.replace('视频', ' ')
            row_t = row_t.replace('香港', ' ')
            row_t = row_t.replace('网页', ' ')
            row_t = row_t.replace('链接', ' ')
            row_t = row_t.replace('沙雕', ' ')
            row_t = row_t.replace('日常', ' ')
            row_t = row_t.replace('没有', ' ')
            row_t = row_t.replace('你们', ' ')
            row_t = row_t.replace('我们', ' ')
            row_t = row_t.replace('他们', ' ')
            row_t = row_t.replace('自己', ' ')
            row_t = row_t.replace('今天', ' ')
            row_t = row_t.replace('这个', ' ')
            row_t = row_t.replace('一次', ' ')
            row_t = row_t.replace('一个', ' ')
            row_t = row_t.replace('现在', ' ')

            row_title_list.append(row_t)
        row_title_str="".join(row_title_list)#列表变成字符串
        data=' '.join(jieba.cut(row_title_str))
        img=Image.open(r'logo1.png')
        imgarray=np.array(img)#转化为数组
        my_word_cloud=WordCloud(
            font_path='C:\Windows\Fonts\simkai.ttf',
            mask=imgarray,
            min_font_size=8,
            background_color='white',
            scale=10#构造精细度
        )
        myWordCloud=my_word_cloud.generate(data)
        myWordCloud.to_file(file)

    def wordClouds_withoutjieba(self,filelist,file):#不用jieba断词
        row_titles=filelist
        row_title_list=[]
        for row_t in row_titles:
            row_title_list.append(row_t)
        data=' '.join(row_title_list)
        img=Image.open(r'logo.png')
        imgarray=np.array(img)#转化为数组
        my_word_cloud=WordCloud(
            font_path='C:\Windows\Fonts\simkai.ttf',
            mask=imgarray,
            min_font_size=8,
            background_color='white',
            scale=10#构造精细度
        )
        myWordCloud=my_word_cloud.generate(data)
        myWordCloud.to_file(file)



    def start(self):
        list_1=self.readframekeyword()
        self.wordClouds(list_1,'a.jpg')
        list_2=self.readframeName()
        self.wordClouds_withoutjieba(list_2,'nickName.jpg')
    def start_mouth(self):
        for i in range(1,3):
            filename = str(i) + '月WordCloud.jpg'
            list=self.getMouthKey_1_2(i)
            self.wordClouds(list, filename)
            print("第" + str(i) + "月词云已经完成！")
        for i in range(3,13):
            filename=str(i)+'月WordCloud.jpg'
            list=self.getMouthKey(i)
            self.wordClouds(list,filename)
            print("第"+str(i)+"月词云已经完成！")

    def start_users(self):
        userList=["人民日报","央视新闻","头条新闻"]
        for i in userList:
            lists=self.getWeiboUserWord(i)
            filename=i+'wordCloud.jpg'
            self.wordClouds(lists,filename)
            print(i+"已经完成！")




if __name__=='__main__':
    d=Deal()
    d.start_users()
    d.start()
    d.start_mouth()