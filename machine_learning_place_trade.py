import MetaTrader5 as mt5
import pytz
from datetime import datetime
import pandas as pd
import re
import numpy as np

class placeOrder():
    def __init__(self, symbol, direction, is_high_probability, percent_to_risk, stop_loss_point):
        self.symbol = symbol
        self.direction = direction
        self.is_open = True
        self.percent_to_risk = percent_to_risk
        self.stop_loss_point = stop_loss_point
        self.is_high_probability = is_high_probability
        self.acc_info = mt5.account_info()
        self.point = mt5.symbol_info(self.symbol).point
        self.ask_price = mt5.symbol_info_tick(self.symbol).ask
        self.bid_price = mt5.symbol_info_tick(self.symbol).bid
        self.deviation = 20
        self.lot = round(self.lot_to_trade(), 1)
    
    def lot_to_trade(self):
        """
        This method calculate the lot size to trade base on the
        account balance, percentage risk, and the stop loss in point
        """
        lot_size = (int(self.acc_info.balance) * self.percent_to_risk) / (self.stop_loss_point * 0.01) / 100
        return lot_size
    
    def check_if_open_position(self):
        """
        This method check if there are open position
        if there is no open position, it set self.is_open to False,
        it also checks if is_high_propability is True or false, is high
        propability is referring to the probability score of the machine
        learning prediction. 
        
        """
        position = mt5.positions_get(self.symbol)
        if self.is_high_probability == False:
            if position == None :
                self.is_open = False
        elif self.is_high_probability == True :
            if position >= 3 :
                self.is_open = False
        return self.is_open
    
    def place_trade(self):
        result = None
        request = None
        if self.is_open == False :
            if self.direction == 'high':
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": self.lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": self.ask_price,
                "sl": self.ask_price - self.stop_loss_point * self.point,
                "tp": self.ask_price + 100 * self.point,
                "deviation": self.deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
                } 

            elif self.direction == "low" :
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": self.lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": self.bid_price,
                "sl": self.bid_price + self.stop_loss_point * self.point,
                "tp": self.bid_price - 100 * self.point,
                "deviation": self.deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
                }
                
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print("order completed successfully")
            else :
                print(f"order failed with code {result.retcode}")            
            
            
        
        
        