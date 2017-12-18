from math import floor, log2
import random
from randomized.hash_family import generate_hash


C = 1/32
BETA = 3/4


class HH1:
    def __init__(self, sigma, n):
        self.sigma = sigma
        self.n = n
        self.R = 3 * floor(log2(min(n, sigma**2) + 1))
        self.Z = self.generate_Z()
        self.h = generate_hash(2, range(2**self.R))
        self.b = [0] * (self.R + 1) # Waste slot 0 to index at 1
        self.X = [0, 0]
        self.r = 1
        self.H = -1
        self.isDone = False
        self.index = 0

    def compute_next(self, item):
        # If we've figured out all the bits, quit
        self.index += 1

        if self.r > self.R:
            self.isDone = True
            return

        hash_item = self.h(item)
        match = True

        for j in range(1, self.r):
            # Check if this item matches the known HH bits thus far
            if HH1.get_bit(hash_item, j) != self.b[j]:
                match = False
                break

        # If it does match the HH, add its contribution to X_0/1
        if match:
            self.H = item
            self.X[HH1.get_bit(hash_item, self.r)] = \
                    self.X[HH1.get_bit(hash_item, self.r)] + self.Z(item)

            # If we've seen enough items for the HH to have made itself known
            # then record the next bit into b
            #print("C * sigma * BETA**r: {}".format(C * self.sigma * BETA**self.r))
            if abs(self.X[0] + self.X[1]) >= (C * self.sigma * BETA**self.r):
                # Record the bit
                #print("Recording a bit, on index {}".format(self.index))
                self.b[self.r] = 1 if (abs(self.X[1]) > abs(self.X[0])) else 0

                # Refresh everything
                self.X = [0, 0]
                self.r = self.r + 1
                self.Z = self.generate_Z()

    def get_value(self):
        return self.H

    def generate_Z(self):
        return generate_hash(4, [-1,1])

    @staticmethod
    def get_bit(value, bit):
        # indexes at 1
        return (value >> (bit-1)) & 1
