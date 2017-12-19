from collections import Counter
from math import ceil, log2
from random import Random
from randomized.frequency_estimator import FrequencyEstimator, SingleEstimator
from unittest import main, TestCase


class TestFrequencyEstimator(TestCase):
    def setUp(self):
        self.estimator = FrequencyEstimator(4, 24)

    def test_repeated_item_estimate(self):
        for _ in range(3):
            self.estimator.add_item('a')
        self.assertEqual(3, self.estimator.estimate('a'))

    def test_fixed_sequence_estimate(self):
        sequence = 'abaacddbeba'

        for c in sequence:
            self.estimator.add_item(c)

        self.assertEqual(4, self.estimator.estimate('a'))
        self.assertEqual(3, self.estimator.estimate('b'))
        self.assertEqual(2, self.estimator.estimate('d'))

    def run_estimator(self, items, k, error_margin, correctness):
        counts = Counter(items)
        heavy_hitters = counts.most_common(k)
        hh = sum(f**2 for _, f in heavy_hitters)
        non_hh = sum(f**2 for _, f in counts.most_common()[k:])

        num_estimators = ceil(log2(len(items) / correctness))
        num_buckets = ceil(8 * max(k, 32 * non_hh / (hh * error_margin) ** 2))
        estimator = FrequencyEstimator(num_estimators, num_buckets)

        for item in items:
            estimator.add_item(item)

        return all(abs(f - estimator.estimate(hh)) <= (f * error_margin)
                   for hh, f in heavy_hitters)

    def test_estimate(self):
        # TODO: seed with CLI arg
        r = Random(42)

        num_estimates = 20
        items = [r.randint(-256, 256) for _ in range(num_estimates * 10)]
        error_margin, correctness = 0.25, 0.75

        corrects = sum(self.run_estimator(items, 3, error_margin, correctness)
                       for _ in range(num_estimates))
        self.assertGreaterEqual(corrects, num_estimates * correctness)


class TestSingleEstimator(TestCase):
    def setUp(self):
        self.estimator = SingleEstimator(4)

    def test_adding_item_multiple_times(self):
        for i in range(3):
            self.assertEqual(i, self.estimator.estimate(1))
            self.estimator.add_item(1)
            self.assertEqual(i + 1, self.estimator.estimate(1))

    # TODO: stub out hashes, better test their use


if __name__ == '__main__':
    main()
