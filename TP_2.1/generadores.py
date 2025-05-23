import time

class RandomGeneratorGLC :
    def __init__ (self, seed=None):
        if seed is None: 
          seed = int(time.time())
        self.seed = seed
        self.a = 25214903917
        self.c = 11
        self.m = 2**48
    
    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed
    
    def capear(self):
        return self.seed / self.m
    

import time

class MiddleSquare:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time()) 
        else:
            seed = int(str(seed).zfill(10)[-10:])
        self.seed = seed
        self.mod = 10**10

    def next(self):
        square = self.seed ** 2
        sq_str = str(square).zfill(20) 
        mid_start = (len(sq_str) - 10) // 2
        mid = sq_str[mid_start:mid_start + 10]
        if mid == '0000000000':
            self.seed = 1 
        else:
            self.seed = int(mid)
        return self.seed

    def capear(self):
        return self.seed / self.mod


class FibonacciGenerator:
    def __init__(self, seed1=None, seed2=None):
        if seed1 is None:
            seed1 = int(time.time()) % 10000
        if seed2 is None:
            seed2 = (int(time.time()) + 1) % 10000
        self.prev = seed1
        self.curr = seed2
        self.m = 10000

    def next(self):
        next_val = (self.prev + self.curr) % self.m
        self.prev, self.curr = self.curr, next_val
        return next_val

    def capear(self):
        return self.curr / self.m
    
    
class LehmerGenerator:
    def __init__(self, seed=None, a=48271, m=2**31 - 1):
        if seed is None:
            seed = int(time.time()) % m
        self.seed = seed
        self.a = a
        self.m = m

    def next(self):
        self.seed = (self.a * self.seed) % self.m
        return self.seed

    def capear(self):
        return self.seed / self.m