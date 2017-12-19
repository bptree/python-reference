from collections import Counter
from countsketch.count_sketch import CountSketch
from math import ceil, log2
from operator import itemgetter
from random import Random
from unittest import main, TestCase


class TestCountSketch(TestCase):
    def setUp(self):
        self.cs = CountSketch(32, 64, 3)

    def test_most_common_with_repeated_item(self):
        self.cs.add_items('aaa')
        self.assertEqual([('a', 3)], self.cs.most_common())

    def test_most_common_sequence(self):
        self.cs.add_items('abaacddbeba')
        self.assertEqual([('a', 4), ('b', 3), ('d', 2)], self.cs.most_common())

    def run_cs(self, items, k, error_margin, correctness):
        counts = Counter(items)
        heavy_hitters = counts.most_common(k)
        hh = sum(f**2 for _, f in heavy_hitters)
        non_hh = sum(f**2 for _, f in counts.most_common()[k:])

        num_rows = ceil(log2(len(items) / correctness))
        num_buckets = ceil(8 * max(k, 32 * non_hh / (hh * error_margin) ** 2))

        cs = CountSketch(num_rows, num_buckets, k)
        cs.add_items(items)
        reported_freq = dict(cs.most_common())

        # Assert that list is in descending sorted order
        mc = cs.most_common()
        self.assertEqual(list(sorted(mc, key=itemgetter(1), reverse=True)),
                         mc)

        return all(hh in reported_freq and \
                   abs(freq - reported_freq[hh]) <= (freq * error_margin)
                   for hh, freq in heavy_hitters)

    def test_random_sequence(self):
        # TODO: seed with CLI arg
        r = Random(42)

        num_instances = 20
        items = [r.randint(-256, 256) for _ in range(num_instances * 10)]
        error_margin, correctness = 0.25, 0.75

        corrects = sum(self.run_cs(items, 3, error_margin, correctness)
                       for _ in range(num_instances))
        self.assertGreaterEqual(corrects, num_instances * correctness)


if __name__ == '__main__':
    main()
