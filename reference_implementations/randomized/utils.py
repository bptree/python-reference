from itertools import islice
from typing import Sequence


def median(numbers: Sequence[int]) -> int:
    if len(numbers) == 0:
        raise ValueError('median on empty sequence')

    sorted_numbers = sorted(numbers)
    median_idx = len(numbers) // 2

    if len(numbers) % 2 == 1:
        median, = islice(sorted_numbers, median_idx, median_idx + 1)
    else:
        left, right = islice(sorted_numbers, median_idx - 1, median_idx + 1)
        median = int((left + right) / 2)

    return median
