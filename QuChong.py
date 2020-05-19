import pandas as pd

def quchong(filename,Newfilename):
    frame=pd.read_csv(filename,header=0)
    frame=frame.drop_duplicates()
    frame.to_csv(Newfilename,index=False)

quchong('Originaldata.csv','a.csv')