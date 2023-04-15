import pandas as pd
import numpy as np
import os
from talib.abstract import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from datetime import datetime
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


class prepareData():
  def __init__(self, data):
    pool = mp.Pool()
    
    self.data = data
    # self.data.rename(columns={"time" : "Time", "high" : "High", "open" : "Open", "low":"Low", "close":"Close"}, inplace=True)
    # self.data.drop(columns=["Unnamed: 0", "tick_volume", "spread", "real_volume"], inplace=True, axis=1)
    # self.data["Time"] = pd.to_datetime(data["Time"])
    self.needed_data = []
    #moving average 15 -50
    self.create_mutiple_indicator(array_of_parameter=[9, 12, 15, 21, 30, 40, 45, 50], function_to_run=self.moving_avaerage)
    # ma = pool.apply_async(self.create_mutiple_indicator, args=((9, 12, 15, 21, 30, 40, 45, 50), self.moving_avaerage))
    #bollinger bands 15 - 50
    self.create_mutiple_indicator(array_of_parameter=[9, 12, 15, 21, 30, 40, 45, 50], function_to_run=self.bbands)

    # adx indicator indicator 14 - 30
    self.create_mutiple_indicator(array_of_parameter=[14, 16, 20, 22, 25, 30, 35], function_to_run=self.adx_indicator)

    # rsi indicator indicator 14 - 30
    self.create_mutiple_indicator(array_of_parameter=[14, 16, 18, 20, 22, 24, 30], function_to_run=self.rsi_indicator)

    # zigzag indicator
    self.zig_zag(0.02)

    # output array using direction
    # dropping null data
    self.data.dropna(inplace=True)
    self.shift_all_column()
    self.create_up_down_array()
    self.filter_real_trade(0.0010)

  def moving_avaerage(self, window):
    self.data[f"ma{window}"] = self.data["Close"].rolling(window).mean()
    self.data.dropna(inplace=True)
    return self.data

  def create_up_down_array(self):
    self.data["ma9shift"] = self.data["ma9"].shift(1)
    self.data["ma21shift"] = self.data["ma21"].shift(1)
    data_array = []
    ma9 = np.array(self.data['ma9'])
    ma21 = np.array(self.data["ma21"])
    ma9_shift = np.array(self.data['ma9shift'])
    ma_21_shift = np.array(self.data['ma21shift'])
    for x in range(0, len(self.data["Close"])):
      if ma9_shift[x] < ma_21_shift[x] and ma9[x] > ma21[x] :
        data_array.append("high")
      elif  ma9_shift[x] > ma_21_shift[x] and ma9[x] < ma21[x] :
        data_array.append("low")
      else :
        data_array.append("neutral")
    self.data["Direction"] = data_array
    self.data = self.data[(self.data["Direction"] == "low") | (self.data["Direction"] == "high")]
    return self.data

  def filter_real_trade(self, price_limit):
    direction = np.array(self.data["Direction"])
    close = np.array(self.data["Close"])
    sorted_direction = []
    for x in range(0, len(self.data["Close"]) - 1):
      if direction[x] == "high" :
        if (close[x+1] - close[x] >= price_limit) :
          sorted_direction.append("high")
        else :
          sorted_direction.append("neutral")
      elif direction[x] == "low" :
        if (close[x] - close[x+1] >= price_limit) :
          sorted_direction.append("low")
        else :
          sorted_direction.append("neutral")
    sorted_direction.append("neutral")
    self.data["sorted_direction"] = np.array(sorted_direction)

    return self.data

  def shift_all_column(self):
    column_list = np.array(self.data.columns)
    for x in column_list[5:] :
      self.data[f"{x}shift"] = self.data[x].shift(1)
    return self.data

  def create_mutiple_indicator(self, array_of_parameter, function_to_run):
    for x in array_of_parameter :
      function_to_run(x)
      
  def adx_indicator(self, timeperiod):
    self.data[f"adx{timeperiod}"] = ADX(self.data["High"], self.data["Low"], self.data["Close"], timeperiod)
    return self.data
  
  def bbands(self, time, updeviation=2.0, down_deviation=2.0):
    upper_bollinger, middle_bollinger, lower_bollinger = BBANDS(self.data["Close"], timeperiod=time, nbdevup=updeviation, nbdevdn=down_deviation)
    self.data[f"upperbollinger{time}"] = upper_bollinger
    self.data[f"middlebollinger{time}"] = middle_bollinger
    self.data[f"lowerbollinger{time}"] = lower_bollinger
    return self.data

  def rsi_indicator(self, timeperiod):
    self.data[f"rsi{timeperiod}"] = RSI(self.data["Close"], timeperiod=timeperiod)
    return self.data

  def zig_zag(self, percentage):
    price = self.data.iloc[0]["Close"]
    direction = None
    direction_array = []

    for x in range(1, len(self.data["Close"])) :
      if ((direction == None) or (direction == "bottom" and self.data.iloc[x]["Close"] >= price * (1 + percentage))):
        direction_array.append("top")
        direction = "top"
        price = self.data.iloc[x]["Close"]
      elif ((direction == None) or (direction == "top" and self.data.iloc[x]["Close"] <= price * (1 + percentage))):
        direction_array.append("bottom")
        direction = "bottom"
        price = self.data.iloc[x]["Close"]
        price_real = price * (1 + percentage)
      else :
        direction_array.append("Neutral")

    direction_array.append("Neutral")
    self.data["zigzag"] = direction_array
    return self.data

def compute_result(files):
      data = pd.read_csv(f"{files}.csv")
      dataprepared =  prepareData(data)
      dataprepared.data.to_csv(f"{files}_processed.csv")
      print("===========================================")
      print(f"{files} finished preparing")
      print("===========================================")
      
if __name__ == '__main__':
    all_files = ["USDJPY1MINUTE","AUDUSD1MINUTE"]
    with PoolExecutor() as executor :
      first = time.time() 
      executor.map(compute_result, all_files)
   
      last = time.time()

      print(last - first)
  

