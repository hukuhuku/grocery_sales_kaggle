import pandas as pd 
import numpy as np
from datetime import timedelta,datetime
from sklearn.ensemble import RandomForestRegressor

#データ読み込み,前処理
dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'uint8', 'unit_sales':'float32'}
train = pd.read_csv('train.csv', usecols=[1,2,3,4,5], dtype=dtypes, parse_dates=['date'],skiprows=range(1,101688780))
train["unit_sales"] = train["unit_sales"].where(0<train.unit_sales,0)

oil = pd.read_csv("oil.csv",parse_dates=["date"],dtype={"dcoilwtico":"float32"},skiprows=range(1,1045))
test_oil = oil[datetime(2017,8,15) < oil.date]
oil = oil[oil.date < datetime(2017,8,16)]
oil.set_index("date",inplace = True)

oil.reset_index(inplace=True)
train = pd.merge(train,oil,how="outer",on="date")
oil = oil.set_index("date")

train["dcoilwtico"] = train["dcoilwtico"].fillna(train["dcoilwtico"].mean())

#モデルの生成
x_train = train.drop(["date","unit_sales"],axis=1)
y_train = train.unit_sales

rf = RandomForestRegressor(n_jobs = -1, n_estimators = 15)
y = rf.fit(x_train, y_train)

#importanceの確認
fti = y.feature_importances_

for i ,feat in enumerate(list(x_train.columns)):
    print('\t{0:20s} : {1:>.6f}'.format(feat, fti[i]))

#testデータ予測
test = pd.read_csv("test.csv",dtype = dtypes,parse_dates =["date"])
test_id = test["id"]

oil_date = pd.date_range("8/16/2017","31/8/2017")
oil_date = pd.DataFrame(oil_date)

oil_date.columns= ["date"]

test_oil2 = pd.merge(test_oil,oil_date,how="outer",on="date")
test_oil2["dcoilwtico"].fillna(test_oil["dcoilwtico"].mean(),inplace=True)

test = pd.merge(test,test_oil2,how="outer",on="date")

del(test["id"])
del(test["date"])

pred_test = y.predict(test)
submission = pd.DataFrame({"id":test_id,"unit_sales":pd.Series(pred_test)})
submission.to_csv("sub1.csv",index=False)
