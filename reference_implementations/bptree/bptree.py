from bptree.hh2 import HH2
from bptree.second_moment_estimator import SecondMomentEstimator
from collections import Counter
from itertools import takewhile
from math import ceil, log2
from randomized.frequency_estimator import FrequencyEstimator
from randomized.hash_family import generate_hash, Hash
from typing import Generic, Hashable, Iterable, List, Optional, Tuple, TypeVar


T = TypeVar('T', bound=Hashable)
U = TypeVar('U', bound=Hashable)


class BpTree(Generic[T]):
    def __init__(self, num_rows: int, num_buckets: int, num_bits: int) -> None:
        self._rows = [Row(num_buckets, num_bits)
                      for _ in range(num_rows)]  # type: List[Row[T]]
        self._frequency_estimator = \
            FrequencyEstimator(num_rows,
                               num_buckets)  # type: FrequencyEstimator[T]
        self._f2_estimator = \
            SecondMomentEstimator(1, 30)  # type: SecondMomentEstimator[T]

    def add_items(self, items: Iterable[T]) -> None:
        for item in items:
            self.add_item(item)

    def add_item(self, item: T) -> None:
        self._f2_estimator.add_item(item)
        self._frequency_estimator.add_item(item)

        for row in self._rows:
            row.add_item(item)

    def most_common(self, n: Optional[int] = None) -> List[Tuple[T, int]]:
        heavy_hitters = \
            Counter({h: self._frequency_estimator.estimate(h)
                    for h in self._get_heavy_hitters()}).most_common()

        f2_estimate = self._f2_estimator.estimate()
        epsilon_heavy_hitters = \
            list(takewhile(lambda x: x[1]**2 >= .25 * f2_estimate, heavy_hitters))
        assert n is None or n <= len(epsilon_heavy_hitters), \
            'unable to accurately report that number of heavy hitters'

        return epsilon_heavy_hitters[:n]

    def _get_heavy_hitters(self) -> Iterable[T]:
        for row in self._rows:
            yield from row.get_heavy_hitters()


class Row(Generic[U]):
    def __init__(self, num_buckets: int, num_bits: int) -> None:
        self._buckets = [HH2(num_bits)
                         for _ in range(num_buckets)]  # type: List[HH2[U]]
        self._index_hash = _generate_index_hash(num_buckets)

    def add_item(self, item: U) -> None:
        self._buckets[self._index_hash(item)].add_item(item)

    def get_heavy_hitters(self) -> Iterable[U]:
        for bucket in self._buckets:
            heavy_hitter = bucket.get_heavy_hitter()
            if heavy_hitter is not None:
                yield heavy_hitter


def _generate_index_hash(x: int) -> Hash[int]:
    return generate_hash(4, range(x))
