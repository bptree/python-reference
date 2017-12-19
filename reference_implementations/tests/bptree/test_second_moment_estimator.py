from collections import Counter
from bptree.second_moment_estimator import SecondMomentEstimator
from math import ceil, fabs, floor, log2
from random import Random
from unittest import main, TestCase


class TestSecondMomentEstimator(TestCase):
    def run_estimator(self, items, error_margin, correctness):
        num_estimators = ceil(2 * log2(1 / correctness))
        num_buckets = ceil(16 / (error_margin**2))

        estimator = SecondMomentEstimator(num_estimators, num_buckets)

        for x in items:
            estimator.add_item(x)

        return estimator.estimate()

    def test_estimate(self):
        # TODO: seed random via CLI flag
        r = Random(420)

        num_estimates = 10
        items = [r.randint(-256, 255) for _ in range(num_estimates * 10)]
        error_margin, correctness = 0.25, 0.75
        estimates = [self.run_estimator(items, error_margin, correctness)
                     for _ in range(num_estimates)]

        actual_f2 = compute_second_moment(items)
        allow_delta = error_margin * actual_f2
        num_within_margin = sum(1 for e in estimates
                                if fabs(actual_f2 - e) <= allow_delta)
        self.assertGreaterEqual(num_within_margin,
                                floor(num_estimates * correctness))


def compute_second_moment(items):
    return sum(frequency**2 for frequency in Counter(items).values())


if __name__ == '__main__':
    main()
