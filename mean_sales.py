import pandas as pd 
import numpy as np
from datetime import timedelta,datetime

dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'uint8', 'unit_sales':'float32'}
train = pd.read_csv('train.csv', usecols=[1,2,3,4,5], dtype=dtypes, parse_dates=['date'],skiprows=range(1,101688780))
train["unit_sales"] = train["unit_sales"].where(0<train.unit_sales,0)
train['unit_sales'] =  train['unit_sales'].apply(pd.np.log1p)
train['dow'] = train['date'].dt.dayofweek

ma_dw = train[['item_nbr','store_nbr','dow','unit_sales']].groupby(['item_nbr','store_nbr','dow'])['unit_sales'].mean().to_frame('madw')
ma_dw.reset_index(inplace=True)
ma_wk = ma_dw[['item_nbr','store_nbr','madw']].groupby(['store_nbr', 'item_nbr'])['madw'].mean().to_frame('mawk')
ma_wk.reset_index(inplace=True)

#Moving Averages
ma_is = train[['item_nbr','store_nbr','unit_sales']].groupby(['item_nbr','store_nbr'])['unit_sales'].mean().to_frame('mais226')
ma_is['mais']=ma_is.median(axis=1)
ma_is.reset_index(inplace=True)

mean_sales = pd.merge(ma_dw,ma_wk,how="outer",on=["store_nbr","item_nbr"])
mean_sales = pd.merge(mean_sales,ma_is,how="outer",on=["store_nbr","item_nbr"])

mean_sales.to_csv("mean_sales.csv")