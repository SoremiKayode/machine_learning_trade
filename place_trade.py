import MetaTrader5 as mt5
import pytz
from datetime import datetime
import pandas as pd
import re

if not mt5.initialize() :
    print("Failed to initialize metatrader 5")
    mt5.shutdown()
# This function get account information, like equity, balance, trade etc.
# acc_info = mt5.account_info()

def lot_to_trade(equity, risk_percent, stop_loss_point):
    lot_size = (equity * risk_percent) / (stop_loss_point * 0.01) / 100
    return lot_size

# print(round(lot_to_trade(int(acc_info.equity), 0.02, 300), 1))
"""This method get the total number of symbol"""
# print(mt5.symbols_total())

"""To get information about all symbol
Just call the symbols_get(), you can pass the symbol prefixed
with an asterisk, you can pass a group of symbols
"""
# symbols_all = mt5.symbols_get()
"""to get all US symbols"""
# symbols_all = mt5.symbols_get("*")
# for symbols in symbols_all:
#     print(symbols)

"""To check if a symbol is selected in market watch
Here we are checking if XAUUSD symbol is in market watch
"""
# selected = mt5.symbol_select("XAUUSD", True)
# print(selected)

"""To get information about a particular symbol
here we are converting the information into a dictionary
and printing the key value pair out
"""
# symbol_info = mt5.symbol_info("EURUSD")._asdict()

# for prop in symbol_info:
#     print(f"{prop} : {symbol_info[prop]}")

"""
To place a trade use order_send() this method takes on parameter the trade 
request

the trade request should contain the following parameters
"action" = action could be any of this :
TRADE_ACTION_DEAL =  Place an order for an instant deal with the specified parameters (set a market order)
TRADE_ACTION_PENDING : pending order
TRADE_ACTION_SLTP : Change open position Stop Loss and Take Profit
TRADE_ACTION_MODIFY : change parameter of the previously placed position
TRADE_ACTION_REMOVE : Remove previously placed pending order
TRADE_ACTION_CLOSE_BY : Close a position by an opposite one

"magic" : either set the magic number by yourself or allow the ea set the magic number itself
"order" : Order ticket. Required for modifying pending orders
"symbol" : The name of the trading instrument, for which the order is placed. Not required when modifying orders and closing positions
"volume" : lot size
"price" :  The price you want to execute the order
"stoplimit" :  price to execute a stop limit order
"sl" : The stop loss price
"tp" : the take profit price
"deviation" : maximum acceptable deviation form the requested price, shouldbe in point

"type" order type, it can be anof this parameters :
ORDER_TYPE_BUY = Market buy order
ORDER_TYPE_SELL = Market sell order
ORDER_TYPE_BUY_LIMIT = Buy Limit pending order
ORDER_TYPE_SELL_LIMIT = Sell Limit pending order
ORDER_TYPE_BUY_STOP = Buy Stop pending order
ORDER_TYPE_SELL_STOP = Sell Stop pending order
ORDER_TYPE_BUY_STOP_LIMIT = Upon reaching the order price, Buy Limit pending order is placed at StopLimit price
ORDER_TYPE_SELL_STOP_LIMIT = Upon reaching the order price, Sell Limit pending order is placed at StopLimit price
ORDER_TYPE_CLOSE_BY = Order for closing a position by an opposite one

"type_filling" : This can be any of the following
ORDER_FILLING_FOK = execute at a specified volume, if the volume is larger than the maximum accepted volume, the order will not be placed
ORDER_FILLING_IOC = if the volume is larger than the maximum accepted volume, the maximum acceptable volume will be use.

"type_time" : the expiration time of the order, it can be any of the parameter 
ORDER_TIME_GTC = The order stays in the queue until it is manually canceled
ORDER_TIME_DAY = The order is active only during the current trading day
ORDER_TIME_SPECIFIED = The order is active until the specified date
ORDER_TIME_SPECIFIED_DAY = The order is active until 23:59:59 of the specified day. If this time appears to be out of a trading session, the expiration is processed at the nearest trading time.

"expiration" : pending order expiration time
"comment" : comment on the order
"position" : closing position ticket number
"position_by" : Ticket number when a postion is closed by another position

The function below place an order
"""
symbol = "EURUSD"

"""Check if the symbol is in the market watch, if not switch it on"""
symbol_info = mt5.symbol_info(symbol)
if not symbol_info :
    print("switching on symbol")
    mt5.symbol_select(symbol, True)
"""calculating lot size using the lot_to_trade function define above"""
# getting the account information
acc_info = mt5.account_info()
print(acc_info)
lot = round(lot_to_trade(int(acc_info.balance), 0.01, 300), 1)
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
print(f"lot : {lot} \n point : {point} \n price : {price} \n deviation : {deviation}")

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
} 

result = mt5.order_send(request)
result_dict = result._asdict()
print(f"sending order..... with the following parameter:\n symbol : {symbol}\n lot : {lot}\n price : {price}")
if result.retcode == mt5.TRADE_RETCODE_DONE:
    print("order completed successfully")
else :
    print(f"order failed with code {result.retcode}")
    print(result_dict)
    
