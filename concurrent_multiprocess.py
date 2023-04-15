import multiprocessing
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import time

class runSomething:
    def __init__(self) :
        start = time.time()
        with PoolExecutor() as executor :
            executor.submit(self.calculate_number, 90000000)
            executor.submit(self.calculate_number1, 8000000)
            executor.submit(self.calculate_number2, 30000000)   
        print(time.time() - start)
    
    def calculate_number(self, number):
        c = 1
        for x in range(0, number):
            c+=x
        print(c)
    
    def calculate_number1(self, number):
        c = 1
        for x in range(0, number):
            c+=x
        print(c)
    
    def calculate_number2(self, number):
        c = 1
        for x in range(0, number):
            c+=x
        print(c)

runSomething()
