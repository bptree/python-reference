from countsketch.sized_counter import SizedCounter
from unittest import main, TestCase


class TestSizedCounter(TestCase):
    def setUp(self):
        self.counter = SizedCounter(3)

        self.counter['a'] = 2
        self.counter['b'] = 1
        self.counter['c'] = 3

    def test_most_common(self):
        self.assertEqual([('c', 3), ('a', 2), ('b', 1)],
                         self.counter.most_common())

    def test_update_count(self):
        self.counter['c'] = 4

        self.assertEqual([('c', 4), ('a', 2), ('b', 1)],
                         self.counter.most_common())

    def test_max_size_invariant(self):
        self.counter['d'] = 2

        self.assertEqual([('c', 3), ('a', 2), ('d', 2)],
                         self.counter.most_common())


if __name__ == '__main__':
    main()
