import pandas as pd 
import numpy as np
from datetime import timedelta,datetime

def load_train():
    #Loading train data
    dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'uint8', 'unit_sales':'float32'}
    train = pd.read_csv('train.csv', usecols=[1,2,3,4,5], dtype=dtypes, parse_dates=['date'],skiprows=range(1,101688780))
    train["unit_sales"] = train["unit_sales"].where(0<train.unit_sales,0)
    train['unit_sales'] =  train['unit_sales'].apply(pd.np.log1p)

    train["payday"] = train["date"].apply(lambda s:True if s.day==15 or s.day == (datetime(2017,s.month+1,1)-timedelta(days=1)).day else False)
    train['dow'] = train['date'].dt.dayofweek

    train["month"] = train["date"].dt.month
    train["payday"] = train["date"].apply(lambda s:True if s.day==15 or s.day == (datetime(2017,s.month+1,1)-timedelta(days=1)).day else False)
    
    train["month"] = train["month"].astype(np.int8)
    train["dow"] = train["dow"].astype(np.int8)
    
    
    #Loading mean_sales
    mean_sales = pd.read_csv("mean_sales.csv")
    mean_sales.drop(["mawk","mais226","madw","Unnamed: 0"],axis=1,inplace=True)
    train = pd.merge(train,mean_sales,how="outer",on=["item_nbr","store_nbr","dow"])
    train.drop(["item_nbr","store_nbr"],axis=1,inplace=True)
    del(mean_sales)

    #Loading oildata
    oil = pd.read_csv("oil.csv",parse_dates=["date"],dtype={"dcoilwtico":"float32"},skiprows=range(1,1045))
    test_oil = oil[datetime(2017,8,15) < oil.date]
    oil = oil[oil.date < datetime(2017,8,16)]
    
    #オイル情報カラムの追加
    train = pd.merge(train,oil,how="outer",on="date")
    train["dcoilwtico"] = train["dcoilwtico"].fillna(train["dcoilwtico"].mean())
    del(oil)

    #祝日カラムの追加
    holidays = pd.read_csv("holidays_events.csv",parse_dates = ["date"])
    holidays = holidays[holidays.date >datetime(2016,12,31)]
    holidays = holidays[holidays.date <datetime(2017,9,1)]
    test_holiday = holidays[holidays.date > datetime(2017,8,15)]
    holidays = holidays[holidays.date < datetime(2017,8,16)]
    holidays.drop(["type","locale","locale_name","description","transferred"],axis = 1,inplace = True)
    holidays["holidays"] = True

    train = pd.merge(train,holidays,how="outer",on="date")
    train["holidays"] = train["holidays"].fillna(False)
    del(holidays)
    

    return train


def load_test():
    #Loading_test_data
    dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'uint8', 'unit_sales':'float32'}
    test = pd.read_csv("test.csv",dtype = dtypes,parse_dates =["date"])
    test_id = test["id"]

    test["dow"] = test["date"].dt.dayofweek
    test["holiday"] = test["date"].dt.day.apply(lambda s:True if s == 24 else False)
    test["payday"] = test["date"].apply(lambda s:True if s.day == 31else False)

    test["month"] = test["date"].dt.month
    test["month"] = test["month"].astype(np.int8)
    test["dow"] = test["dow"].astype(np.int8)
    
    #Loading mean_sales
    mean_sales = pd.read_csv("mean_sales.csv")
    mean_sales.drop(["mawk","mais226","madw","Unnamed: 0"],axis=1,inplace=True)
    test = pd.merge(test,mean_sales,how="outer",on=["item_nbr","store_nbr","dow"])
    test.drop(["item_nbr","store_nbr"],axis=1,inplace=True)
    test["mais"] = test["mais"].fillna(test["mais"].mean())

    #Loading_test_oil
    oil = pd.read_csv("oil.csv",parse_dates=["date"],dtype={"dcoilwtico":"float32"},skiprows=range(1,1045))
    test_oil = oil[datetime(2017,8,15) < oil.date]
    oil_date = pd.date_range("8/16/2017","31/8/2017")
    oil_date = pd.DataFrame(oil_date)

    oil_date.columns= ["date"]

    test_oil2 = pd.merge(test_oil,oil_date,how="outer",on="date")
    test_oil2["dcoilwtico"].fillna(test_oil["dcoilwtico"].mean(),inplace=True)

    test = pd.merge(test,test_oil2,how="outer",on="date")

    test = test.dropna(subset = ["date"])    
    
    del(test["id"])
    del(test["date"])
    del(oil)
    del(test_oil)
    del(test_oil2)

    return test


if  __name__ == "__main__":
    test = load_test()
    print(test.columns)
    print(test.isnull().any())