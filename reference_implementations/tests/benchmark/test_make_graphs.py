from benchmark.make_graphs import count_columns
from unittest import main, TestCase


class TestMakeGraphs(TestCase):
    def test_count_columns(self):
        columns = {0: 'a', 1: 'b'}
        rows = {0: columns, 1: columns}
        third = {0: rows, 1: rows}

        self.assertEqual(2, count_columns(rows))
        self.assertEqual(4, count_columns(third))
        self.assertEqual(8, count_columns({0: third, 1: third}))


if __name__ == '__main__':
    main()
