from collections import Counter
from countsketch.count_sketch import CountSketch
from random import Random
from unittest import main, TestCase


class TestCountSketch(TestCase):
    def setUp(self):
        self.cs = CountSketch(32, 64, 3)

    def test_repeated_item(self):
        self.cs.add_items('aaa')
        self.assertEqual(3, self.cs.estimate_frequency('a'))
        self.assertEqual([('a', 3)], self.cs.most_common())

    def test_sequence(self):
        self.cs.add_items('abaacddbeba')
        self.assertEqual([('a', 4), ('b', 3), ('d', 2)], self.cs.most_common())

    # TODO: This test is fragile. We need a way to tune parameters and input
    # sequence to give the exact count, or to bound the error and somehow
    # account for that in tests
    def test_random_sequence(self):
        # TODO: seed random via CLI flag
        random = Random(420)
        seq = [random.randint(0, 8) for _ in range(16)]

        self.cs.add_items(seq)

        self.assertEqual(Counter(seq).most_common(3), self.cs.most_common())


if __name__ == '__main__':
    main()
