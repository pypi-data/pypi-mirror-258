# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 00:06:01 2022
Constructing Comprehensive Tick-by-Tick Stock Data
@author: tonyyang1223
"""

import os
import pandas as pd
import numpy as np
import datetime
import time
import statsmodels.api as sm

def convert(x):
    vv=[]
    vv.extend(x)
    return vv

def first(x):
    return x[:1]

def last(x):
    return x[-1:]

file='大单波动率影响'
a=pd.read_csv(file+'/'+'SH600460_20180531.csv',encoding='gbk',header=0,engine='python')
b=pd.read_csv(file+'/'+'SH600460.csv',engine='python',encoding='gbk',header=0,names=['time','price','bs','vol'])
a.index=a['时间']
a['trade_cum']=a['成交笔数'].cumsum()
b['count']=1
b['trade_cum']=b['count'].cumsum()
b['vol']=b['vol']/100


#将逐笔数据与tick数据进行拼接，同一时间单元的交易归入同一个tick中
b['tt']=pd.Series()
for i,j in a['trade_cum'].to_dict().items():
    index_b=np.where(b.trade_cum.values==j)[0]
    b.loc[index_b,'tt']=i
b.fillna(method='bfill',inplace=True)

temp_a=a[['时间','最新价','成交量','买一价','买一量','卖一价','卖一量']]
temp_b=b[['tt','bs','price','vol']]
temp_b.columns=['时间','方向','价格','成交量']
c=pd.merge(temp_a,temp_b,on='时间')

#订单流明细拆解
b['q95']=b['vol'].rolling(500).quantile(0.95)
b['q80']=b['vol'].rolling(500).quantile(0.8)
b['type']=pd.Series()
b['type']='小'
b.loc[b['vol']>=b['q95'],'type']='大'
b.loc[(b['vol']<b['q95'])&(b['vol']>=b['q80']),'type']='中'
detail=b.pivot_table(index='tt',columns='type',values='vol',aggfunc=np.count_nonzero)
info=pd.concat([a[['时间','最新价','买一价','买一量','卖一价','卖一量','成交笔数']],detail],axis=1).dropna()


#生成高开低收的四个价格，构造波动性
h=b.pivot_table(index='tt',values='price',aggfunc=[first,np.max,np.min,last])
h.columns=['open','high','low','close']
h['volity']=h['high']-h['low']
h['big_ratio']=detail['大']/(detail['大']+detail['中']+detail['小'])*100
h.fillna(0,inplace=True)
#构建波动性与明细之间关系
aa=[]
for i in range(0,10):
    aa.append(np.corrcoef(h['volity'].iloc[i:],h['big_ratio'].shift(i).dropna())[0][1])

bb=pd.Series(aa,index=range(0,10))
bb.plot()

x = h['big_ratio'].shift(6).dropna()
y = h['volity'].iloc[6:]*1000
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())

