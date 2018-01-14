cate_vars = []
dtrain = lgb.Dataset(
    X_train,label=y_train[:,1],
    categorical_feature=cate_vars,
    weight=pd.concat([items["perishable"]]*6)*0.25+1
)

gbm = lgb.LGBMRegressor(objective='regression',
                        num_leaves = 31,
                        n_estimators=100)

gbm.fit(X_train, y_train[:,1],
        verbose=0)

fti = gbm.feature_importances_

print("Feature Importances:")
for i,feat in enumerate(X_train.columns):
    print('\t{0:10s} : {1:>12.4f}'.format(feat, fti[i]))

    