from bptree.hh2 import HH2
from bptree.hh1 import HH1
from bptree.f2_estimator import F2_Estimator
import random
from unittest import main, TestCase
from collections import defaultdict

class TestHH2(TestCase):

    # Verify HH2 initializes correctly
    def test_init(self):
        n = 30
        hh2 = HH2(n)
        self.assertEqual(n, hh2.n)
        self.assertEqual(None, hh2.hh1_0)
        self.assertTrue(isinstance(hh2.hh1_1, HH1))
        self.assertEqual(n, hh2.hh1_1.n)
        self.assertEqual(1, hh2.hh1_1.sigma)
        self.assertTrue(isinstance(hh2.estimator, F2_Estimator))
        self.assertEqual(1, hh2.k)

    # Verifies that adding an item to HH2 behaves as expected
    def test_add_item(self):
        n = 5
        hh2 = HH2(n)
        item = 1
        hh2.add_item(random.randint(1,n))
        # Verify the 2^k threshold behavior and that the item was added into
        # the appropriate hh1s, causing the respective hh1.r == 2 (because of
        # the small n)
        est = hh2.estimator.update_estimate()
        if est < 2:
            self.assertEqual(1, hh2.k)
            self.assertTrue(hh2.hh1_0 is None)
            self.assertEqual(1, hh2.hh1_1.sigma)
            self.assertEqual(2, hh2.hh1_1.r)
        else:
            self.assertEqual(2, hh2.k)
            self.assertTrue(hh2.hh1_0 is not None)
            self.assertEqual(1, hh2.hh1_0.sigma)
            self.assertEqual(est, hh2.hh1_1.sigma)
            self.assertEqual(2, hh2.hh1_1.r)
            self.assertEqual(2, hh2.hh1_0.r)
        # Add items until 2^2 threshold is reached, and test result
        iter_count = 100000
        while (hh2.k < 3):
            hh2.add_item(random.randint(1,n))
            iter_count -= 1
            if (iter_count == 0):
                break
        self.assertNotEqual(0, iter_count)
        self.assertEqual(3, hh2.k)
        self.assertTrue(hh2.hh1_0 is not None)
        self.assertNotEqual(hh2.hh1_1.sigma, hh2.hh1_0.sigma)

    # Verifies that hh2.get_value behaves as expected under three cases:
    def test_get_value(self):
        n = 20
        hh2 = HH2(n)
        item = 5
        # Case 1 : hh1_0 is None
        self.assertEqual(None, hh2.get_value())
        # Case 2 : hh1_0 isn't done
        hh2.add_item(item)
        hh2.add_item(item)
        self.assertTrue(hh2.hh1_0 is not None)
        self.assertEqual(None, hh2.get_value())
        # Case 3 : hh1_0 is done
        for _ in range(100):
            hh2.add_item(item)
        self.assertTrue(hh2.hh1_0.isDone)
        self.assertEqual(item, hh2.get_value())

    # Tests with a larger and somewhat more realistic stream
    def test_large_set(self):
        n = 100
        heavy = 72
        error_margin = 0.1
        total = 0
        counts = defaultdict(int)
        error_margin = 0.1

        # Create Stream
        hh_freq = 20
        stream = []
        for _ in range(10000):
            if random.randint(1,100) <= hh_freq:
                stream.append(heavy)
            else:
                stream.append(random.randint(0,n))

        # Run 20 HH2s in parallel, feeding them the same stream
        # They'll have different hash functions so we don't expect them to all
        # produce the same results
        num_hh2s = 20
        hh2s = [HH2(n) for _ in range(num_hh2s)]
        for item in stream:
            for i in range(num_hh2s):
                hh2s[i].add_item(item)

        for i in range(num_hh2s):
            if hh2s[i].get_value():
                counts[hh2s[i].get_value()] += 1
                total += 1

        self.assertTrue(total > 0)
        self.assertTrue(abs(counts[heavy] - num_hh2s) < error_margin * num_hh2s)


