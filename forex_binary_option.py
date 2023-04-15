"""
Objective :

To create a binary option automated trading startegy
using machine learning algorithms, the strategy must have at least 
95 percent winning rate

INPUTS :

many exponential moving average
two simple moving average or exponential moving average to predict directions
many relative strength index (RSI)
many Average directional strength index (ADX)
Bollinger bands

SOLUTIONS :
get the dataset needed

create a 9 period moving average and a 12 period moving average

loop through the dataset compare if ma9[-1] < ma12[-1] and ma9[0] > ma12[0]
check if that closing price > closing price.shift(10) put up else put neutral

loop through the dataset compare if ma9[-1] > ma12[-1] and ma9[0] < ma12[0]
check if that closing price[0] < closing price.shift(10) put down else put neutral

create an array put the index inside an array.

shift these column by one and create another column with it.

extract these index from the dataframe
"""

