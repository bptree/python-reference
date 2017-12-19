from bptree.hh1 import HH1, C, BETA, int_to_bitarray
from collections import Counter
from math import sqrt
from unittest import main, TestCase

#from collections import defaultdict


class TestHH1(TestCase):
    # Tests a single HH1 computation
    def test_single_round(self):
        sigma = 5
        n = 30
        hh1 = HH1(sigma, n)
        item = 1

        hash_value = hh1._hash(item)
        hh1.add_item(item)
        self.assertEqual(item, hh1._heavy_hitter)
        self.assertEqual(1, len(hh1._learned_hash)) # (C * sigma * BETA) ~ 0.12

    """
    # Tests 3 rounds of HH1 computation with parameters such that the
    # computation should roll from r=1 to r=2 on round 3.
    def test_multiple_rounds(self):
        sigma = 100
        n = 30
        hh1 = HH1(sigma, n)

        # Round 1 : item = 1
        item = 1
        hash_value = hh1._hash(item)
        bit = int_to_bitarray(hash_value)[0]
        not_bit = 1 if (bit == 0) else 0

        hh1.compute_next(item)
        self.assertEqual(item, hh1.H)
        self.assertEqual(1, abs(hh1._buckets[bit]))
        self.assertEqual(0, hh1._buckets[not_bit])
        self.assertTrue(abs(hh1.X[0] + hh1.X[1]) < (C * sigma * BETA)) # ~ 2.34
        self.assertEqual(1, hh1.r)

        # Round 2 : item = something different, same X as 1, same Z value
        while (item == 1 or bit == not_bit or hh1.Z(item) != hh1.Z(1)):
            item = random.randint(0, n)
            h_item = hh1.h(item)
            bit = HH1.get_bit(h_item, 1)
        hh1.compute_next(item)
        self.assertEqual(item, hh1.H)
        self.assertEqual(2, abs(hh1.X[bit]))
        self.assertEqual(0, hh1.X[not_bit])
        self.assertTrue(abs(hh1.X[0] + hh1.X[1]) < (C * sigma * BETA)) # ~ 2.34

        # Round 3 : item = something different, same X as 1, same Z value
        prev_item = item
        while (item == prev_item or item == 1 or bit == not_bit \
                                 or hh1.Z(item) != hh1.Z(1)):
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

        self.assertTrue(total > 0)
        self.assertTrue(abs(counts[heavy] - total) < error_margin * total)"""

    def run_get_heavy_hitter_on_sequence(self):
        numbers = [10, 9, 21, 13, 21, 13, 11, 13]
        sqrt_f2 = sqrt(second_moment(numbers))
        assert sqrt_f2 <= stddev(numbers) <= 2 * sqrt_f2

        while True:
            hh1 = HH1(stddev(numbers), 5)

            for item in numbers:
                hh1.add_item(item)

            if hh1.is_done():
                break

        return hh1.get_heavy_hitter() == 13

    def test_get_heavy_hitter_on_sequence(self):
        num_instances = 50
        correct = sum(self.run_get_heavy_hitter_on_sequence()
                      for _ in range(num_instances))
        self.assertGreaterEqual(correct, (2 / 3) * num_instances)


def stddev(numbers):
    mean = sum(numbers) / len(numbers)
    return sqrt(sum((n - mean)**2 for n in numbers) / (len(numbers) - 1))


def second_moment(numbers):
    return sum(freq**2 for freq in Counter(numbers).values())


if __name__ == '__main__':
    main()
