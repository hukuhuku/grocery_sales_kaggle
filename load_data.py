import pandas as pd    
import numpy as np
from datetime import timedelta
from logging import getLogger


TRAIN_DATA = "input/train.csv"
TEST_DATA = "input/test.csv"
HOLIDAY_DATA = "input/holidays_events.csv"

dtypes = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}
logger = getLogger(__name__)

def read_csv(path):
    logger.debug("enter")
    df = pd.read_csv(path,usecols=[1,2,3,4],dtype=dtypes,parse_dates=["date"],skiprows=range(1, 86672217))
    logger.debug("exit")
    return df

def load_holiday():
    logger.debug("enter")
    df = read_csv(HOLIDAY_DATA)
    logger.debug("exit")
    return df

def load_train():
    print("Loading_train_data")
    df = read_csv(TRAIN_DATA)
    print("Done")
    return df

def load_test():
    print("Loading_test_data")
    df = read_csv(TEST_DATA)
    print("Done")
    return df


if __name__ == "__main__":
    print(load_train)


    