from benchmark.runner import compute_correct, compute_error
from unittest import main, TestCase

class TestRunner(TestCase):
    def test_compute_correct(self):
        actual = [('a', 3), ('b', 2), ('c', 1)]
        reporteds = [
            ([('a', 3), ('b', 2), ('c', 1)], [True, True, True]),
            ([('d', 3), ('b', 2), ('c', 1)], [False, True, True]),
            ([('d', 3), ('b', 2), ('e', 1)], [False, True, False]),
            ([('d', 3), ('b', 2)], [False, True, False]),
            ([('b', 2), ('c', 1)], [False, True, True]),
            ([('d', 2), ('c', 1)], [False, False, True]),
            ([('c', 1)], [False, False, True]),
            ([('d', 1)], [False, False, False]),
            ([], [False, False, False]),
        ]

        for reported, result in reporteds:
            self.assertEqual(compute_correct(actual, reported), result)

    def test_compute_error(self):
        inf = float('inf')
        actual = [('a', 8), ('b', 4), ('c', 2)]
        reporteds = [
            ([('a', 8), ('b', 4), ('c', 2)], [0, 0, 0]),
            ([('a', 10), ('b', 2), ('c', 1)], [0.25, 0.5, 0.5]),
            ([('d', 8), ('b', 12), ('c', 2)], [inf, 2, 0]),
            ([('d', 8), ('b', 4), ('e', 2)], [inf, 0, inf]),
            ([('d', 8), ('b', 2)], [inf, 0.5, inf]),
            ([('b', 4), ('c', 2)], [inf, 0, 0]),
            ([('d', 4), ('c', 2)], [inf, inf, 0]),
            ([('c', 2)], [inf, inf, 0]),
            ([('d', 2)], [inf, inf, inf]),
            ([], [inf, inf, inf]),
        ]

        for reported, result in reporteds:
            self.assertEqual(list(compute_error(actual, reported)),
                             [r * 100 for r in result])


if __name__ == '__main__':
    main()
