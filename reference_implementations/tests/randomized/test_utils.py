from randomized.utils import median
from itertools import permutations
from unittest import main, TestCase


class TestUtil(TestCase):
    def test_exact_median(self):
        for seq in permutations([1, 2, 3]):
            self.assertEqual(2, median(seq))

    def test_averaged_median(self):
        for seq in permutations([1, 2, 4, 5]):
            self.assertEqual(3, median(seq))

    def test_median_empty_sequence(self):
        with self.assertRaises(ValueError):
            median([])


if __name__ == '__main__':
    main()
