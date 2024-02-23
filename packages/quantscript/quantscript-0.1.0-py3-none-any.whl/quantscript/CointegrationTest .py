# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:28:37 2018

@author: tonyyang1223
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
file='协整检验数据'
for i in os.listdir(file):
    a=pd.read_csv(file+'/'+i,index_col=0,engine='python')
    
data=pd.Series()
data=a['000333.XSHE']-a['000651.XSHE']

#进行平稳性检验
dftest=adfuller(data,autolag='BIC')
dfoutput = pd.Series(dftest[0:4], index=['统计量','p-value','延迟阶数','观测窗口'])
for key,value in dftest[4].items():
    dfoutput['临界值 (%s)'%key] = value
print(dfoutput)
#进行线性回归
x = a['000333.XSHE']
y = a['000651.XSHE']
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())
#画出拟合曲线
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(x, y, 'o', label="data")
ax.plot(x, result.fittedvalues, 'r', label="OLS")
ax.legend(loc='best')
plt.show()
#得到两序列围绕常数的波动，这个常数是截距也是其平稳序列的均值
z=1.0059*x-y
z_score=(z-z.mean())/z.std()
plt.plot(np.arange(len(z_score)),z_score)
plt.axhline(z_score.mean(), color="black")
plt.axhline(1.0, color="red", linestyle="--")
plt.axhline(-1.0, color="green", linestyle="--")
plt.legend(["z-score", "mean", "+1", "-1"])
