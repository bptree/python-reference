from heapq import heapify, heappop
from itertools import islice
from typing import Iterable, Sequence


def median(numbers: Sequence[int]) -> int:
    if len(numbers) == 0:
        raise ValueError('median on empty sequence')

    # TODO: Might want modified quickselect (for median or left/right),
    #       but that might be overkill
    sorted_numbers = isorted(numbers)
    median_idx = len(numbers) // 2

    if len(numbers) % 2 == 1:
        median, = islice(sorted_numbers, median_idx, median_idx + 1)
    else:
        left, right = islice(sorted_numbers, median_idx - 1, median_idx + 1)
        median = int((left + right) / 2)

    return median


def isorted(sequence: Sequence[int]) -> Iterable[int]:
    heap = list(sequence)[:]
    heapify(heap)

    while len(heap) > 0:
        yield heappop(heap)
