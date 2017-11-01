from countsketch.counter import Counter
from countsketch.sized_counter import SizedCounter
from randomized.utils import median
from typing import Generic, Hashable, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar('T', bound=Hashable)


# TODO: conform to typing.Counter and rename to Counter in __init__.py
class CountSketch(Generic[T]):
    def __init__(self, num_hashes: int, buckets_per_hash: int,
                 num_heavy_hitters: int) -> None:
        # TODO: tight coupling here, creating Counter/SizedCounter in init
        self._counters = [Counter(buckets_per_hash)
                          for _ in range(num_hashes)]  # type: List[Counter[T]]
        self._heavy_hitters = \
            SizedCounter(num_heavy_hitters)  # type: SizedCounter[T]

    def add_items(self, items: Iterable[T]) -> None:
        for item in items:
            self.add_item(item)

    def add_item(self, item: T) -> None:
        for counter in self._counters:
            counter.add_item(item)

        self._heavy_hitters[item] = self.estimate_frequency(item)

    def estimate_frequency(self, item: T) -> int:
        return median([c.estimate_frequency(item) for c in self._counters])

    def most_common(self, n: Optional[int] = None) -> List[Tuple[T, int]]:
        return self._heavy_hitters.most_common(n)


def _make_counters(num_hashes: int, buckets_per_hash: int) -> List[Counter[T]]:
    return [Counter(buckets_per_hash) for _ in range(num_hashes)]
