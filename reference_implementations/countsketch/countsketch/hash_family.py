from random import random
from typing import Any, Generic, Hashable, Sequence, TypeVar

V = TypeVar('V')
H = TypeVar('H', bound=Hashable)


class Hash(Generic[V]):
    def __init__(self, a: int, b: int, image: Sequence[V]) -> None:
        self._a = a
        self._b = b
        self._image = image

    def __call__(self, item: H) -> V:
        return self._image[(self._a * hash(item) + self._b) % len(self._image)]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Hash) \
            and (self._a, self._b) == (other._a, other._b)


def generate_hash(image: Sequence[V]) -> Hash[V]:
    return Hash(_generate_parameter(), _generate_parameter(), image)


# TODO hash must be larger than num_buckets
LARGE_PRIME = 32993


def _generate_parameter() -> int:
    return int(random() * LARGE_PRIME) + 1
