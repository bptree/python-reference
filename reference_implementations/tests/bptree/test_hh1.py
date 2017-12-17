from bptree.hh1 import HH1, C, BETA
import random
from unittest import main, TestCase
from collections import defaultdict

class TestHH1(TestCase):

    # Does generate_Z create the vector we expect?
    def test_generate_Z(self):
        n = 10000
        count_pos = 0
        count_neg = 0
        total = 0
        epsilon = .05
        hh1 = HH1(5, n)

        self.assertEqual(n+1, len(hh1.Z))
        for item in hh1.Z:
            self.assertEqual(1, abs(item))
            if (item == 1):
                count_pos += 1
            if (item == -1):
                count_neg += 1
            total += 1

        self.assertEqual(total, count_pos + count_neg)
        # May fail probabalistically
        self.assertTrue(abs(count_pos/total - .5) < epsilon)

    # Tests that get_bit() returns the correct bits
    def test_get_bit(self):
        self.assertEqual(0, HH1.get_bit(0,1))
        self.assertEqual(1, HH1.get_bit(1,1))
        self.assertEqual(0, HH1.get_bit(1,2))
        self.assertEqual(1, HH1.get_bit(2,2))
        self.assertEqual(0, HH1.get_bit(2,1))
        self.assertEqual(0, HH1.get_bit(2,3))
        self.assertEqual(1, HH1.get_bit(3,1))
        self.assertEqual(1, HH1.get_bit(3,2))
        self.assertEqual(0, HH1.get_bit(3,3))
        self.assertEqual(1, HH1.get_bit(5,1))
        self.assertEqual(0, HH1.get_bit(5,2))
        self.assertEqual(1, HH1.get_bit(5,3))
        self.assertEqual(0, HH1.get_bit(5,4))
        self.assertEqual(1, HH1.get_bit(9001,14))

    # Tests that the HH1 constructor initializes itself as expected
    def test_init(self):
        sigma = 5
        n = 30
        hh1 = HH1(sigma, n)

        self.assertEqual(sigma, hh1.sigma)
        self.assertEqual(n, hh1.n)
        self.assertEqual(12, hh1.R)
        self.assertEqual(hh1.R+1,len(hh1.b))
        for item in hh1.b:
            self.assertEqual(0, item)
        self.assertEqual(2, len(hh1.X))
        self.assertEqual(0, hh1.X[0])
        self.assertEqual(0, hh1.X[1])
        self.assertEqual(1, hh1.r)
        self.assertEqual(-1, hh1.H)

    # Tests a single HH1 computation
    def test_single_round(self):
        sigma = 5
        n = 30
        hh1 = HH1(sigma, n)

        item = 1
        h_item = hh1.h(item)
        bit = HH1.get_bit(h_item, 1)
        hh1.compute_next(1);
        self.assertEqual(item, hh1.H)
        self.assertEqual(2, hh1.r) # (C * sigma * BETA) ~ 0.12

    # Tests 3 rounds of HH1 computation with parameters such that the
    # computation should roll from r=1 to r=2 on round 3.
    def test_multiple_rounds(self):
        sigma = 100
        n = 30
        hh1 = HH1(sigma, n)

        # Round 1 : item = 1
        item = 1
        h_item = hh1.h(item)
        bit = HH1.get_bit(h_item, 1)
        not_bit = 1 if (bit == 0) else 0

        hh1.compute_next(1);
        self.assertEqual(item, hh1.H)
        self.assertEqual(1, abs(hh1.X[bit]))
        self.assertEqual(0, hh1.X[not_bit])
        self.assertTrue(abs(hh1.X[0] + hh1.X[1]) < (C * sigma * BETA)) # ~ 2.34
        self.assertEqual(1, hh1.r)

        # Round 2 : item = somthing different, same X as 1, same Z value
        while (item == 1 or bit == not_bit or hh1.Z[item] != hh1.Z[1]):
            item = random.randint(0, n)
            h_item = hh1.h(item)
            bit = HH1.get_bit(h_item, 1)
        hh1.compute_next(item)
        self.assertEqual(item, hh1.H)
        self.assertEqual(2, abs(hh1.X[bit]))
        self.assertEqual(0, hh1.X[not_bit])
        self.assertTrue(abs(hh1.X[0] + hh1.X[1]) < (C * sigma * BETA)) # ~ 2.34

        # Round 3 : item = somthing different, same X as 1, same Z value
        prev_item = item
        while (item == prev_item or item == 1 or bit == not_bit \
                                 or hh1.Z[item] != hh1.Z[1]):
            item = random.randint(0, n)
            h_item = hh1.h(item)
            bit = HH1.get_bit(h_item, 1)
        hh1.compute_next(item)
        self.assertEqual(item, hh1.H)
        self.assertEqual(2, hh1.r)
        self.assertEqual(bit, hh1.b[1])
        self.assertEqual(0, hh1.X[0])
        self.assertEqual(0, hh1.X[1])

    # Tests with a larger and somewhat more realistic stream
    def test_large_set(self):
        sigma = 1000
        n = 100
        heavy = 62
        total = 0
        counts = defaultdict(int)
        error_margin = 0.1

        # Create Stream
        hh_freq = 5
        stream = []
        for _ in range(10000):
            if random.randint(1,10) <= hh_freq:
                stream.append(heavy)
            else:
                stream.append(random.randint(0,n))

        # Run HH1
        hh1 = HH1(sigma, n)
        for item in stream:
            hh1.compute_next(item)
            if hh1.isDone:
                counts[hh1.get_value()] += 1
                total += 1
                hh1 = HH1(sigma, n)

        #print(counts[heavy], total)
        #print("Hashed heavy hitter: {}".format(hh1.h(heavy)))
        #print("Bits: {}".format(bin(hh1.h(heavy))))
        #print("Hashed wrong: {}".format(hh1.h(hh1.get_value())))
        #print("Bits: {}".format(bin(hh1.h(hh1.get_value()))))
        self.assertTrue(total > 0)
        self.assertTrue(abs(counts[heavy] - total) < error_margin * total)
