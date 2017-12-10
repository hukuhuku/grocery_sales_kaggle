import numpy as np 
import pandas as pd 

print("Loading_Data")
train = pd.read_csv("./input/train.csv")
test = pd.read_csv("./input/test.csv")
print("done")

print("")
print("optimize test_data")
print("")
print("test_max")
print(test.max())
print("")
print("test_min")
print(test.min())
print("")
print("test_dtype")
print(test.dtypes)

mem_test = test.memory_usage(index=True).sum()
print("test dataset uses",mem_test/1024**2,"MB")

#store_nbrは54種類しかないのでunit8型
#idはかなり大きいが非負なのでunit32
#item_nbrも同じ理由でunit32
