from bptree.bptree import BpTree
from collections import Counter
from math import ceil, log2
from operator import itemgetter
from random import Random, shuffle
from unittest import main, TestCase


class TestBpTree(TestCase):
    def setUp(self):
        self.bp = BpTree(1, 30, 3)

    def test_most_common_repeated_item(self):
        self.bp.add_items([1] * 20)
        self.assertEqual([(1, 20)], self.bp.most_common())

    def run_bptree(self, items, k, error_margin, correctness):
        counts = Counter(items)
        heavy_hitters = counts.most_common(k)

        num_rows = 10 * ceil(log2(1 / (error_margin * correctness)))
        num_buckets = ceil(10 / (error_margin ** 2))

        bp = BpTree(num_rows, num_buckets, 3)
        bp.add_items(items)
        mc = bp.most_common()
        reported_freq = dict(mc)

        # Assert that list is in descending sorted order
        self.assertEqual(list(sorted(mc, key=itemgetter(1), reverse=True)),
                         mc)

        return all(hh in reported_freq and \
                   abs(freq - reported_freq[hh]) <= (freq * error_margin)
                   for hh, freq in heavy_hitters)

    def test_random_sequence(self):
        # TODO: seed with CLI arg
        r = Random(42)

        num_instances = 5
        items = r.choices(range(3, 8), k=10) + [0] * 30 + [1] * 20
        r.shuffle(items)
        error_margin, correctness = 0.25, 0.75

        corrects = sum(self.run_bptree(items, 2, error_margin, correctness)
                       for _ in range(num_instances))
        self.assertGreaterEqual(corrects, num_instances * correctness)


if __name__ == '__main__':
    main()
