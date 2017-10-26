from countsketch.counter import Counter
from unittest import main, TestCase


class TestCounter(TestCase):
    def setUp(self):
        self.counter = Counter(4)

    def test_adding_item_multiple_times(self):
        for i in range(3):
            self.assertEqual(i, self.counter.estimate_frequency(1))
            self.counter.add_item(1)
            self.assertEqual(i + 1, self.counter.estimate_frequency(1))

    # TODO: stub out hashes, better test their use


if __name__ == '__main__':
    main()
