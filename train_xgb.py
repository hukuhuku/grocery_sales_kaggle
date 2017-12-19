#Loading Library
import pandas as pd 
import numpy as np
from datetime import timedelta,datetime
from load_data import load_train,load_test
import xgboost as xgb
from sklearn.model_selection import GridSearchCV

#train読み込み
train = load_train()

x_train = train.drop(["date","unit_sales"],axis=1)
y_train = train.unit_sales

#xgboostのために型変換
fac = x_train.columns

for feat in fac:
    x_train[feat] = pd.factorize(x_train[feat],sort = True)[0]
    
x_train = np.array(x_train)
x_train = xgb.DMatrix(x_train)

#xgboostによりモデルフィッティング

reg = xgb.Regressor()

reg_cv = GridSearchCV(reg,{"max_depth":[2,4,6],"n_estimators":[50,100,200]},verbose = 1)
reg_cv.fit(x_train,y_train)

reg = xgb.Regressor(**reg_cv.best_params_)
reg.fit(x_train, y_train)

#モデルの保存
import pickle
pickle.dump(reg,open("reg_model.pkl","wb"))

#test読み込み
test = load_test()

for feat in fac:
    test[feat] = pd.factorize(test[feat],sort = True)[0]

test = np.array(test)
test = xgb.DMatrix(test)

#モデルに当てはめる
pred_test = reg.predict(test)
submission = pd.DataFrame({"id":test_id,"unit_sales":pd.Series(pred_test)})
submission.to_csv("sub4.csv",index=False)

#feature importance 
import matplotlib.pyplot as plt


