from bptree.f2_estimator import Brute_Force_F2_Estimator
import random
from unittest import main, TestCase
from collections import defaultdict

class TestBruteForceF2(TestCase):
    # Sets up a basic brute force estimator
    def setUp(self):
        self.n = 100
        self.bfe = Brute_Force_F2_Estimator(self.n)

    # Tests that the estimator is initialized properly
    def test_init(self):
        self.assertEqual(0, self.bfe.F2)
        self.assertEqual(self.n+1, len(self.bfe.f))
        for freq in self.bfe.f:
            self.assertEqual(0, freq)

    # Tests Brute_Force_F2_Estimator.add_item()
    def test_add_item(self):
        # Add values at the extremes of the domain
        self.bfe.add_item(0)
        self.assertEqual(1, self.bfe.f[0])
        # Verify adding items doesn't modifiy other frequencies
        for freq in self.bfe.f[1:]:
            self.assertEqual(0, freq)
        self.bfe.add_item(self.n)
        self.assertEqual(1, self.bfe.f[self.n])
        self.assertEqual(1, self.bfe.f[0])
        for freq in self.bfe.f[1:self.n-1]:
            self.assertEqual(0, freq)
        # Verify repeated additions
        self.bfe.add_item(1)
        self.bfe.add_item(1)
        self.bfe.add_item(1)
        self.assertEqual(3, self.bfe.f[1])

    # Tests Brute_Force_F2_Estimator.update_estimate()
    def test_update_estimate(self):
        self.assertEqual(0, self.bfe.F2)
        # Add single item
        self.bfe.add_item(1)
        self.bfe.update_estimate()
        self.assertEqual(1, self.bfe.F2)
        # Add second unique item
        self.bfe.add_item(2)
        self.bfe.update_estimate()
        self.assertEqual(2, self.bfe.F2)
        # Add multiple of existing item
        self.bfe.add_item(1)
        self.bfe.update_estimate()
        self.assertEqual(5, self.bfe.F2)

    # Tests that the Brute Force Estimator is still correct over a larger number
    # of insertions.
    def test_many_update_estimate(self):
        num_items = 100
        sum = 0
        # Create and input stream
        for _ in range(num_items):
            self.bfe.add_item(random.randint(1, self.n))
        # Check that the number of insertions was correct
        sum = 0
        for item in self.bfe.f:
            sum += item
        self.assertEqual(num_items, sum)
