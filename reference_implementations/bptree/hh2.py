from bptree.f2_estimator import Brute_Force_F2_Estimator
from bptree.hh1 import HH1
from math import sqrt

class HH2():

    def __init__(self, n):
        self.n = n
        # This is HH1_k-1
        self.hh1_0 = None
        # This is HH1_k
        self.hh1_1 = HH1(1, self.n)
        self.estimator = Brute_Force_F2_Estimator(self.n)
        self.k = 1

    def add_item(self, item):
        self.estimator.add_item(item)
        F2_estimate = self.estimator.update_estimate()
        # If we've crossed a threshold move HH1_k to HH1_k-1 and make a new HH1
        if F2_estimate >= 2**self.k:
            self.hh1_0 = self.hh1_1
            self.hh1_1 = HH1(sqrt(F2_estimate), self.n)
            self.k += 1
        # Pass the item into our two most recent HH1s.
        if self.hh1_0 is not None:
            self.hh1_0.compute_next(item)
        self.hh1_1.compute_next(item)

    def get_value(self):
        if self.hh1_0 is not None and self.hh1_0.isDone:
            return self.hh1_0.get_value()
        else:
            #print("HH1 is on: {} out of {}".format(self.hh1_0.r, self.hh1_0.R))
            return None

