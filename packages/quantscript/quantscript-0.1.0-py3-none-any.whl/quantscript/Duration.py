# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 22:52:51 2018

@author: tonyyang1223
"""

import pandas as pd
import os
import numpy as np
from scipy import stats
import math

file='久期泊松分布'
for i in os.listdir(file)[0:1]:
    a=pd.read_csv(file+'/'+i,engine ='python')
    
a['time']=pd.to_datetime(a['Time'])
a.index=a['time']
a['hour']=a.index.hour
a['minute']=a.index.minute
a['period']=pd.Series()
a.loc[(a['hour']==9)&(a['minute']>=30),'period']='09:30-10:30'
a.loc[(a['hour']==10)&(a['minute']<30),'period']='09:30-10:30'
a.loc[(a['hour']==10)&(a['minute']>=30),'period']='10:31-11:30'
a.loc[(a['hour']==11)&(a['minute']<30),'period']='10:31-11:30'
a.loc[(a['hour']==13),'period']='13:00-14:00'
a.loc[(a['hour']==14),'period']='14:00-15:00'
a['tt']=pd.Series()
for i in ['09:30-10:30','10:31-11:30','13:00-14:00','14:00-15:00']:
    a.loc[a['period']==i,'tt']=a.loc[a['period']==i,'time'].diff().apply(lambda x: x.seconds)
a.dropna(inplace=True)
count=a.pivot_table(index='period',values='TranID',aggfunc=np.count_nonzero)
describe=a.pivot_table(index='period',values='tt',aggfunc=[np.mean,np.median,np.std,stats.skew,stats.kurtosis])
b=pd.concat([count,describe],axis=1)
b.index.name='时间'
b.sort_index(inplace=True)
b.columns=['数量','平均值','中位数','标准差','偏度','峰度']

#泊松分布建模
num=len(a)
time=240-3
average=num/time
hist=[]
for i in range(15):
    poison=(average)**i*np.exp(-average)/math.factorial(i)
    hist.append(poison)
hi=pd.Series(hist,index=range(15))
hi.plot(kind='bar')

