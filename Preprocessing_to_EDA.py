def aggregate(df):
    sale_day_store_level = df.groupby(["Month","Day","store_nbr"],as_index=False)["unit_sales"].agg(["sum","count"])
    sale_day_store_level = sale_day_store_level.reset_index().rename(columns={"sum":"store_sales","count":"item_variety"})

    sale_day_item_level=df.groupby(['Month','Day','item_nbr'],as_index=False)['unit_sales'].agg(['sum','count'])
 
    sale_day_item_level=sale_day_item_level.reset_index().rename(columns={'sum':'item_sales','count':'store_spread'})
 
    sale_store_item_level=df.groupby(['store_nbr','item_nbr'],as_index=False)['unit_sales'].agg(['sum','count'])
    sale_store_item_level=sale_store_item_level.reset_index().rename(columns={'sum':'item_sales','count':'entries'})

    return sale_day_store_level,sale_day_item_level,sale_store_item_level


import pandas as pd 
import numpy as np
from datetime import timedelta,datetime
import time


dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'uint8', 'unit_sales':'float32'}
train = pd.read_csv('./train.csv', usecols=[1,2,3,4,5], dtype=dtypes, parse_dates=['date'],skiprows=range(1,101688780))
#2017-01-01のものから利用

train["Month"] = train["date"].apply(lambda s:s.month)
train["Day"] = train["date"].apply(lambda s:s.day)

sale_day_store_level_2017,sale_day_item_level_2017,sale_store_item_level_2017 = aggregate(train)

sale_day_item_level_2017.to_csv("sale_day_item_2017.csv")
sale_day_store_level_2017.to_csv("sale_day_store_2017.csv")
sale_store_item_level_2017.to_csv("sale_store_item_level.csv")

