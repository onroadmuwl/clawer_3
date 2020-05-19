import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
class pictorial():
    def draw(self,indexs,values,filename):
        c = (
            PictorialBar()
                .add_xaxis(indexs)
                .add_yaxis(
                "",
                values,
                label_opts=opts.LabelOpts(is_show=False),
                symbol_size=18,
                symbol_repeat="fixed",
                symbol_offset=[0, 0],
                is_symbol_clip=True,
                symbol=SymbolType.ROUND_RECT,
            )
                .reversal_axis()
                .set_global_opts(
                title_opts=opts.TitleOpts(title="报道香港新闻热门博主前十名"),
                xaxis_opts=opts.AxisOpts(is_show=False),
                yaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(opacity=0)
                    ),
                ),
            )
        )
        c.render(filename)

    def getName(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        frame = pd.read_csv('data_improveutf8.csv', header=0)
        frames = frame[(frame['like'] >= 100000)|(frame['transpound']>=10000)|(frame['review']>=10000)]
        select=frames['content'].groupby(frames['name']).count()
        selector=select.reset_index()
        selector=selector.sort_values(by='content',ascending=False)
        selector=selector.head(10)
        selector = selector.sort_values(by='content', ascending=True)
        name=[]
        content=[]
        for i in selector['name']:
            name.append(i)
        for i in selector['content']:
            content.append(i)
        list=[name,content]
        return list
    def start(self):
        list=self.getName()
        index=list[0]
        value=list[1]
        self.draw(index,value,'name.html')

if __name__=='__main__':
    d=pictorial()
    d.start()