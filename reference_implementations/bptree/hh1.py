from collections import defaultdict
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
        self.b = [0] * (self.R + 1)
        self.X = [0, 0]
        self.r = 1
        self.H = -1

    def compute_next(self, item):
        # If we've figured out all the bits, quit
        if self.r >= self.R + 1:  # TODO: Confirm this +1 is okay
            return True

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
                self.X[HH1.get_bit(hash_item, self.r)] + self.Z[item]

            # If we've seen enough items for the HH to have made itself known
            # then record the next bit into b
            if abs(self.X[0] + self.X[1]) >= (C * self.sigma * BETA**self.r):
                # Record the bit
                self.b[self.r] = 1 if (abs(self.X[1]) > abs(self.X[0])) else 0

                # Refresh everything
                self.X = [0, 0]
                self.r = self.r + 1
                self.Z = self.generate_Z()

    def get_value(self):
        return self.H

    def generate_Z(self):
        # TODO: Talk to Bailey about this method of randomness
        return [random.choice([-1, 1]) for _ in range(self.n + 1)]

    @staticmethod
    def get_bit(value, bit):
        # indexes at 1
        return (value >> (bit-1)) & 1


def main():
    count = defaultdict(int)
    total = 0
    options = ([2] * 8) + [1, 3]
    stream = [random.choice(options) for _ in range(100000)]
    test = HH1(5, 30)

    for item in stream:
        if test.compute_next(item) is not None:
            count[test.get_value()] += 1
            total += 1
            test = HH1(5, 30)

    print(count)
    print('1:', count[1]/total)
    print('2:', count[2]/total)
    print('3:', count[3]/total)


if __name__ == '__main__':
    main()
