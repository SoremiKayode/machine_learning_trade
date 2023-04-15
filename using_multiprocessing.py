import time
import multiprocessing as mp
import concurrent.futures


class counters() :
    def  __init__(self):
        self.y = 0
        pool = mp.Pool()
        result1 = pool.apply_async(self.count_one, args=((range(0, 100)),))
        result2 = pool.apply_async(self.count_two, args=((range(0, 100)),))
        result3 = pool.apply(self.count_three, args=((range(0, 100)),))
    
    def count_one(self, x):
        a = 0
        for b in x :
            a += b * 15
        self.y = a
        return self.y
        
    
    def count_two(self, x):
        a = 0
        for b in x :
            a += b * 15
        self.y += a
        return self.y
        
    def count_three(self, x):
        a = 0
        for b in x :
            a += b * 15
        self.y += a
        return self.y
    
    def result(self, results):
        print(results)


if __name__ == '__main__':
    first = time.time()
    cass = counters()
    
    print(cass.y)
   
    last = time.time()

    print(last - first)

