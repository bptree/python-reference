from unittest import main, TestCase
from countsketch.hash_family import Hash


class TestHashFamily(TestCase):
    def setUp(self):
        self.hash = Hash([2, 1], 'ABCD')

    def test_hash(self):
        self.assertEqual('C', self.hash(0))
        self.assertEqual('D', self.hash(1))
        self.assertEqual('A', self.hash(2))
        self.assertEqual('B', self.hash(3))
        self.assertEqual('C', self.hash(4))
        self.assertEqual('C', self.hash(-3))


if __name__ == '__main__':
    main()
