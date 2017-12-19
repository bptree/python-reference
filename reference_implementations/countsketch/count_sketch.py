from countsketch.counter import Counter
from countsketch.sized_counter import SizedCounter
from randomized.frequency_estimator import FrequencyEstimator
from randomized.utils import median
from typing import Generic, Hashable, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar('T', bound=Hashable)


# TODO: conform to typing.Counter and rename to Counter in __init__.py
class CountSketch(Generic[T]):
    def __init__(self, num_rows: int, num_buckets: int,
                 num_heavy_hitters: int) -> None:
        self._frequency_estimator = \
                FrequencyEstimator(num_rows,
                                   num_buckets)  # type: FrequencyEstimator[T]
        self._heavy_hitters = \
            SizedCounter(num_heavy_hitters)  # type: SizedCounter[T]

    def add_items(self, items: Iterable[T]) -> None:
        for item in items:
            self.add_item(item)

    def add_item(self, item: T) -> None:
        self._frequency_estimator.add_item(item)
        self._heavy_hitters[item] = self._frequency_estimator.estimate(item)

    def most_common(self, n: Optional[int] = None) -> List[Tuple[T, int]]:
        return self._heavy_hitters.most_common(n)
