import pyecharts.options as opts
from pyecharts.charts import Line
import pandas as pd
class LINE():
    def GetAllDateAndLine(self):
        frame=pd.read_csv('data_improveutf8.csv')
        data=frame['content'].groupby(frame['date']).count()
        pd.set_option('display.max_columns',None)
        pd.set_option('display.max_rows',None)
        #如何把时间进行正确排序,由于pandas对带日期的时间排序不正确，重新构造dataframe
        datas=data.reset_index()#重置为dataframe
        value=[]
        index=[]
        for i in datas['date']:
            if i[0:3]=='10月' or i[0:3]=='11月' or i[0:3]=='12月':
                i='s'+str(i)
            index.append(i)
        for i in datas['content']:
            value.append(i)
        text={'index':index,'value':value}
        df=pd.DataFrame(text)
        df=df.sort_values(by='index',ascending=True)
        print(df)
        values= []
        indexs = []
        for i in df['index']:
            i=i.replace('s','')
            indexs.append(i)
        for i in df['value']:
            values.append(i)
        line=(
            Line()
            .add_xaxis(indexs)
            .add_yaxis('关注度',values,is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title='香港事件关注度',subtitle='2019年1月1日-12月9日'))
        )
        line.render('myhtml.html')

    def getMonthDate(self,Month):
        frame = pd.read_csv('data_improveutf8.csv')
        data = frame['content'].groupby(frame['date']).count()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        datas = data.reset_index()  # 重置为dataframe
        value = []
        index = []
        index_1=[]
        for row in datas.itertuples():  # 按行查找
            date=getattr(row,'date')
            contentNum=getattr(row,'content')
            dateNum=date[0:date.find(u'月')]
            if dateNum==Month:
                value.append(contentNum)
                index.append(date)
        for i in index:
            i=i[i.find('月')+1:-1]
            i=int(i)
            index_1.append(i)
        text = {'index': index_1, 'value': value}
        df = pd.DataFrame(text)
        df = df.sort_values(by='index', ascending=True)
        values = []
        indexs = []
        for i in df['index']:
            i =Month+'月'+str(i)+'日'
            indexs.append(i)
        for i in df['value']:
            values.append(i)
        list=[indexs,values]
        return list





    def GetUserDate(self,Username):
        frame = pd.read_csv('data_improveutf8.csv')
        frame=frame[frame['name']==Username]
        data = frame['content'].groupby(frame['date']).count()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        # 如何把时间进行正确排序,由于pandas对带日期的时间排序不正确，重新构造dataframe
        datas = data.reset_index()  # 重置为dataframe
        value = []
        index = []
        for i in datas['date']:
            i = i[0:i.find(u'月')]
            i=int(i)
            index.append(i)
        for i in datas['content']:
            value.append(i)
        text = {'index': index, 'value': value}
        df = pd.DataFrame(text)
        df = df.sort_values(by='index', ascending=True)
        df=df['value'].groupby(df['index']).sum()
        df=df.reset_index()
        print(df)
        values=[]
        for i in df['value']:
            values.append(i)
        return values




    def DrawThreeUserLine(self):
        value_1=self.GetUserDate('人民日报')[0:6]
        value_2= self.GetUserDate('央视新闻')[0:6]
        value_3 = self.GetUserDate('头条新闻')[4:10]

        index=['7月','8月','9月','10月','11月','12月']
        line = (
            Line()
                .add_xaxis(index)
                .add_yaxis('人民日报', value_1)
                .add_yaxis('央视新闻', value_2)
                .add_yaxis('头条新闻', value_3)
                .set_global_opts(title_opts=opts.TitleOpts(title='三家热门对香港事件关注度', subtitle="人民日报 央视新闻 今日头条"))
        )
        line.render("Users.html")
    def DrawMonthLine(self,index,value,MonthNum):
        FileName=MonthNum+'月香港事件频率.html'
        line = (
            Line()
                .add_xaxis(index)
                .add_yaxis('关注度', value, is_smooth=True)
                .set_global_opts(title_opts=opts.TitleOpts(title='香港事件关注度', subtitle=MonthNum))
        )
        line.render(FileName)
    def start_get_month(self):
        for i in range(1,13):
            i=str(i)
            list=self.getMonthDate(i)
            index=list[0]
            value=list[1]
            self.DrawMonthLine(index,value,i)
            print(i+'月已经完成！')


if __name__=='__main__':
    d=LINE()
    #d.start_get_month()
    #d.GetAllDateAndLine()
    d.DrawThreeUserLine()