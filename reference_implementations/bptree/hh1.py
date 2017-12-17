"""
Implementation of BPTree based on the paper by Braverman et al
"""
import random
from math import floor,log
from randomized.hash_family import generate_hash

class HH1(object):

    def __init__(self, sigma, n):
        # Setting up constants and variables we need later
        self.sigma = sigma
        self.n = n
        self.R = self.calculate_R()
        self.Z = self.generate_Z()
        self.h = generate_hash(2, range(2**self.R))
        self.b = [0]*(self.R+1)
        self.X = [0,0]
        self.r = 1
        self.H = -1
        self.Beta = (3/4)
        self.c = (1/32)

    def compute_next(self, item):
        # If we've figured out all the bits, quit
        if self.r >= self.R+1: #TODO: Confirm this +1 is okay
            #print("DONE: {0} >= {1}".format(self.r,self.R+1))
            return True#TODO: Return something to HH2?
            
        hash_item = self.h(item)
        match = True
        
        #print("b: {0}, item: {1}".format(self.b, item))
        #print("r: {0}".format(self.r))
        for j in range(1, self.r):
            # Check if this item matches the known HH bits thus far
            if HH1.get_bit(hash_item, j) != self.b[j]:
                match = False
                #print("NO MATCH hash: {0}".format(hash_item))
                break

        # If it does match the HH, add its contribution to X_0/1
        if match:
            #print("MATCH hash: {0}".format(hash_item))
            self.H = item
            #print("   Going into X", HH1.get_bit(hash_item, self.r))
            self.X[HH1.get_bit(hash_item, self.r)] = \
                    self.X[HH1.get_bit(hash_item, self.r)] + self.Z[item]

            # If we've seen enough items for the HH to have made itself known then
            # record the next bit into b
            if abs(self.X[0] + self.X[1]) >= (self.c * self.sigma * self.Beta**self.r):
                # Record the bit
                self.b[self.r] = 1 if (abs(self.X[1]) > abs(self.X[0])) else 0
                #print("Seen enough!")
                # Refresh everything
                self.X = [0,0]
                self.r = self.r + 1
                self.Z = self.generate_Z()

    def get_value(self):
        return self.H

    def calculate_R(self):
        return 3*floor(log(min(self.n,self.sigma**2)+1,2))

    def generate_Z(self):
        z = []
        for i in range(self.n+1):
            # TODO: Talk to Bailey about this method of randomness
            z.append(random.choice([1,-1]))
        return z
        
    @staticmethod
    def get_bit(value, bit):
        # indexes at 1
        return (value >> (bit-1)) & 1

def main():
    count = {}
    total = 0
    count[1] = count[2] = count[3] = 0
    options = [2,2,2,2,2,2,2,2,1,3]
    stream = []
    for i in range(100000):
        stream.append(random.choice(options))
    test = HH1(5, 30)
    for item in stream:
        if test.compute_next(item) is not None:
            count[test.get_value()] = count[test.get_value()] + 1
            total = total + 1
            test = HH1(5, 30)
    print(count)
    print("1:", count[1]/total)
    print("2:", count[2]/total)
    print("3:", count[3]/total)
    
if __name__ == "__main__": main()
