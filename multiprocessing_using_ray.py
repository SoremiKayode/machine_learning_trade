# import pandas as pd
# import numpy as np
# import os
# from talib.abstract import *
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# import tensorflow as tf
import ray
# from datetime import datetime
import time
ray.init()





# end = datetime.strptime(datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"), "%Y-%m-%d-%H:%M:%S.%f")
# start = datetime.strptime(datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"), "%Y-%m-%d-%H:%M:%S.%f")
@ray.remote
class countMe() :
    def  __init__(self):
        pass
    
    def count_one(self, x, y):
        a = 0
        for b in x :
            a += b * y
        return a
    
    def count_two(self, x, y):
        a = 0
        for b in x :
            a += b * y
        return a
    
    def count_three(self, x, y):
        a = 0
        for b in x :
            a += b * y
        return a
    
    def result(self):
        return self.resulter
    

        

start = time.time()
dutch = countMe.remote()
print(ray.get(dutch.count_one.remote(list(range(0, 100000000)), 14)))
print(ray.get(dutch.count_two.remote(list(range(0, 100000000)), 15)))
print(ray.get(dutch.count_three.remote(list(range(0, 100000000)), 20)))
end = time.time()
print(end - start)

