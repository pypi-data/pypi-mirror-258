# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 18:10:07 2018

@author: tonyyang1223
"""

import pandas as pd
import numpy as np
import os


data={}
data['品种及频率']=[]
data['均值']=[]
data['最大值']=[]
data['最小值']=[]
data['中值']=[]
data['标准差']=[]
data['偏度']=[]
data['峰度']=[]

file='游程检验数据'
for i in os.listdir(file)[:1]:
    temp=pd.read_csv(file+'/'+i,engine ='python')
    a=temp[' <Close>'].pct_change()*100
    data['品种及频率'].append(os.path.splitext(i)[0])
    data['均值'].append(a.mean())
    data['最大值'].append(a.max())
    data['最小值'].append(a.min())
    data['中值'].append(a.median())
    data['标准差'].append(a.std())
    data['偏度'].append(a.skew())
    data['峰度'].append(a.kurtosis())

info=pd.DataFrame()
info['品种及频率']=data['品种及频率']
info['均值']=data['均值']
info['最大值']=data['最大值']
info['最小值']=data['最小值']
info['中值']=data['中值']
info['标准差']=data['标准差']
info['偏度']=data['偏度']
info['峰度']=data['峰度']
