import pandas as pd
import numpy as np
import os
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

score_dataFrame = {
    "model_name" : [],
    "model_evaluation_loss" : [],
    "model_evaluation_accuracy" : []
}

def train_data_LSTM(data):
    
  name_of_file = data.split("/")[-1]
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
  y = data["sorted_direction"]
  row_count1 = int(data.shape[0] * 0.5)
  row_count2 = int(data.shape[0] * 0.7)
  x_train = x[:row_count1]
  x_test = x[row_count1:row_count2]
  x_validate = x[row_count2:]
  y_train = y[:row_count1]
  y_test = y[row_count1:row_count2]
  y_validate = y[row_count2:]
  y_train = tf.keras.utils.to_categorical(y_train, 3)
  y_test = tf.keras.utils.to_categorical(y_test, 3)
  y_validate = tf.keras.utils.to_categorical(y_validate, 3)
  scaler = MinMaxScaler()
  scaler.fit(x)
  x_train = scaler.transform(x_train)
  x_test = scaler.transform(x_test)
  x_validate = scaler.transform(x_validate)
  size = x_train.shape[1]
  size_y_0, size_y_1 = y_train.shape[0], y_train.shape[1]
  y_train = y_train.reshape(y_train.shape[0], 1, y_train.shape[1])
  y_test = y_test.reshape(y_test.shape[0], 1, y_test.shape[1])
  x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])
  x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])
  x_validate = x_validate.reshape(x_validate.shape[0], 1, x_validate.shape[1])
  model = tf.keras.models.Sequential()
  model.add(tf.keras.layers.LSTM(15, return_sequences=True, activation="relu"))
  model.add(tf.keras.layers.Dropout(0.2))
  model.add(tf.keras.layers.LSTM(10, return_sequences=True, activation="relu"))
  model.add(tf.keras.layers.Dropout(0.2))
  model.add(tf.keras.layers.LSTM(3, return_sequences=True, activation="softmax"))
  model.compile(optimizer="adam", metrics='accuracy', loss='categorical_crossentropy')
  model.fit(x_train, y_train, epochs=10, batch_size=12)
  evaluation_loss, evaluation_accuracy = model.evaluate(x_test, y_test)
  pred = model.predict(x_validate)
  score_dataFrame["model_name"].append(name_of_file[:-4])
  score_dataFrame["model_evaluation_loss"].append(evaluation_loss)
  score_dataFrame["model_evaluation_accuracy"].append(evaluation_accuracy)
  save_name = name_of_file[:-4]
  model.save(save_name)

if __name__ == "__main__":
    with PoolExecutor() as executor:
        first = time.time()
        executor.map(train_data_LSTM, all_files)
        last = time.time()
        print(last - first)
        
    datas = pd.DataFrame(score_dataFrame)
    datas.to_csv("score_data.csv")