print("Loading Library")
import pandas as pd 
import numpy as np
from datetime import timedelta,datetime
print("Done")

print("Loading train data")
dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'uint8', 'unit_sales':'float32'}
train = pd.read_csv('train.csv', usecols=[1,2,3,4,5], dtype=dtypes, parse_dates=['date'],skiprows=range(1,101688780))
print("Done")

print("Loading oil Data")
oil = pd.read_csv("oil.csv",parse_dates=["date"],dtype={"dcoilwtico":"float32"},skiprows=range(1,1045))
test_oil = oil[datetime(2017,8,15) < oil.date]
oil = oil[oil.date < datetime(2017,8,16)]
oil.set_index("date",inplace = True)
print("Done")

print("adding oil price")
oil.reset_index(inplace=True)
train = pd.merge(train,oil,how="outer",on="date")
oil = oil.set_index("date")
print("Done")

print("adding month columns")
train["month"] = train["date"].apply(lambda s:s.month)
print("Done")


print("adding weekly_oil columns")
weekly_oil = oil.groupby(pd.TimeGrouper(freq = '1W')).mean()

date = pd.date_range("1/1/2017","15/8/2017")
r = []
for i in range(1,33):
    for j in range(7):
        r.append(i)
r.append(33)
r.append(33)
r.append(33)
df = pd.DataFrame(r,date)
df = df.reset_index()
df.columns = ["date","week"]

a = [i for i in range(1,len(weekly_oil)+1)] 
weekly_oil["week"] = a
weekly_oil.columns = ["weekly_oil","week"]

train = pd.merge(train,df,how="outer",on="date")
train = pd.merge(train,weekly_oil,how="outer",on="week")
print("Done")

print("adding monthly oil columns")
monthly_oil = oil.groupby(pd.TimeGrouper(freq = "1M")).mean()
monthly_oil = monthly_oil.reset_index()
monthly_oil["month"] = monthly_oil["date"].apply(lambda s:s.month)
monthly_oil.columns = ["date","monthly_oil","month"]
del(monthly_oil["date"])

train = pd.merge(train,monthly_oil,how="outer",on="month")
print("Done")

print("writting to csv")
train.to_csv("train2.csv")
print("Done")