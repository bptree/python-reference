from itertools import islice
from collections import Counter
from operator import itemgetter
from typing import Any, Counter, Hashable, TypeVar

T = TypeVar('T', bound=Hashable)


# TODO: more efficient than just inheriting Counter behavior
class SizedCounter(Counter[T]):
    def __init__(self, max_size: int, *args: Any, **kwargs: Any) -> None:
        if max_size <= 0:
            raise ValueError('max_size must be a positive integer')

        super().__init__(*args, **kwargs)
        self._max_size = max_size

    def __setitem__(self, item: T, frequency: int) -> None:
        super().__setitem__(item, frequency)

        # Maintain max size invariant
        if len(self) > self._max_size:
            sorted_items = sorted(self.items(), key=itemgetter(1))
            (smallest_item, _), = islice(sorted_items, 0, 1)
            del self[smallest_item]
