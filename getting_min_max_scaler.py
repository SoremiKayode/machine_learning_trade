from joblib import load, dump
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from datetime import datetime
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

all_files = [
    "GBPUSD1MINUTE_processed.csv",
    "AUDUSD1MINUTE_processed.csv",
    "NZDUSD1MINUTE_processed.csv",
    "USDCAD1MINUTE_processed.csv",
    "USDCHFIMINUTE_processed.csv",
    "USDJPY1MINUTE_processed.csv",
    "XAUUSD1MINUTE_processed.csv",
    "eur_usd_processed.csv"]


def load_to_dump(data):
    name_of_file = f"{data[:-14]}_scaler.gz"
    data = pd.read_csv(data)
    data_replace = {
    "top" : 1,
    "bottom" : 0.5,
    "Neutral" : 0,
    "low" : 0.5,
    "high" : 1, 
    "neutral" : 0,
    }
    
    data.drop(["Tick", "Date"], inplace=True, axis=1)
    data.replace(data_replace, inplace=True)
    columns = list(data.columns)
    x = data[columns[:-1]]
    scaler = MinMaxScaler()
    scaler.fit(x)
    pickle.dump(scaler, open(name_of_file, 'wb'))

if __name__ == '__main__':
    
    with PoolExecutor() as executor:
        executor.map(load_to_dump, all_files)
        print("completed")

load_to_dump("GBPUSD1MINUTE_processed.csv")