import MetaTrader5 as mt5
import pytz
from datetime import datetime
import pandas as pd
import re
from preprocessing_real_prediction import prepareData
if not mt5.initialize() :
    print("Failed to initialize metatrader 5")
    mt5.shutdown()
    
class FetchData():
    """
    This class fetch data for all major forex symbols
    like EURUSD, EURJPY, USDJPY, EURCAD, USDCAD, USDCHF
    This class take four parameters :
    symbol : symbol is a 6 letter string representing the forex quote you want to fetch.
    start_date : the starting date of the quote should be int this format  "YYYY-M-D"
    end_date : the ending date of the quote should be int this format  "YYYY-M-D"
    time_frame : the time_frame should be a string; it should be in this format
    "TIMEFRAME_M1" : 1 minute,
    "TIMEFRAME_M2" : 2 Minute,
    "TIMEFRAME_M5" : 5 Minute,
    "TIMEFRAME_M15" : 15 Minute,
    "TIMEFRAME_M30" : 30 Minute,,
    "TIMEFRAME_H1" : 1 Hour,
    "TIMEFRAME_H4" : 4 Hour,
    "TIMEFRAME_D1" : mt5.TIMEFRAME_D1, 
    
    """
    def __init__(self, symbol, start_date:str, end_date:str, time_frame):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.time_frame = time_frame
        self.dictionary_of_time = {
            "TIMEFRAME_M1" : mt5.TIMEFRAME_M1,
            "TIMEFRAME_M2" : mt5.TIMEFRAME_M2,
            "TIMEFRAME_M5" : mt5.TIMEFRAME_M5,
            "TIMEFRAME_M15" : mt5.TIMEFRAME_M15,
            "TIMEFRAME_M30" : mt5.TIMEFRAME_M30,
            "TIMEFRAME_H1" : mt5.TIMEFRAME_H1,
            "TIMEFRAME_H4" : mt5.TIMEFRAME_H4,
            "TIMEFRAME_D1" : mt5.TIMEFRAME_D1,
        }
    
    def process_date(self, date:str):
        splitted_date = re.split(r"(:|-)", date)
        splitted_date = [int(x) for x in splitted_date if x != '-' and x != ':']
        return splitted_date
    
    def save_dataframe(self, dataframe):
        dataframe.to_csv(f"{self.symbol}_{self.time_frame}.csv")
        
    def conv_to_date(self, dataframe):
        dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
        return dataframe
        
    def get_data(self):
        if type(self.symbol) == list :
                
            start_date = self.process_date(self.start_date)
            end_date = self.process_date(self.end_date)
            timezone = pytz.timezone("Etc/UTC")
            # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
            utc_from = datetime(start_date[0], start_date[1], start_date[2], tzinfo=timezone)
            utc_to = datetime(end_date[0], end_date[1], end_date[2], tzinfo=timezone)
            # get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
            for items in self.symbol :
                rates = mt5.copy_rates_range(items, self.time_frame,
                utc_from, utc_to)
                pandas_dataframe = pd.DataFrame(rates)
                # dataframe = self.conv_to_date(pandas_dataframe)
                pandas_dataframe.to_csv(f"{items}_{self.time_frame}.csv")
                # return pandas_dataframe
            
        else : 
            start_date = self.process_date(self.start_date)
            end_date = self.process_date(self.end_date)
            timezone = pytz.timezone("Etc/UTC")
            # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
            utc_from = datetime(start_date[0], start_date[1], start_date[2], tzinfo=timezone)
            utc_to = datetime(end_date[0], end_date[1], end_date[2], tzinfo=timezone)
            # get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
            rates = mt5.copy_rates_range(self.symbol, self.time_frame,
            utc_from, utc_to)
            pandas_dataframe = pd.DataFrame(rates)
            # dataframe = self.conv_to_date(pandas_dataframe)
            return pandas_dataframe
        
data_run = FetchData(symbol="EURUSD", start_date="2023:4:10", end_date="2023-4-12", time_frame=mt5.TIMEFRAME_M1)
data = data_run.get_data()
print(data)
prepare_data = prepareData(data)
print(prepare_data.data)