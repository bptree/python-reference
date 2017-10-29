from random import randrange
from typing import Any, Generic, Hashable, Sequence, Tuple, TypeVar

V = TypeVar('V')
H = TypeVar('H', bound=Hashable)

LARGE_PRIME = 2**61 - 1


class Hash(Generic[V]):
    def __init__(self, params: Tuple[int], image: Sequence[V]) -> None:
        self._params = params
        self._image = image

    def __call__(self, item: H) -> V:
        x = hash(item)
        y = sum(c * x**p for p, c in enumerate(self._params))

        return self._image[(y % LARGE_PRIME) % len(self._image)]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Hash) and self._params == other._params


def generate_hash(k_independence: int, image: Sequence[V]) -> Hash[V]:
    return Hash([_random_coefficient(i == 0) for i in range(k_independence)],
                image)


def _random_coefficient(allow_zero: bool = False) -> int:
    return randrange((0 if allow_zero else 1), LARGE_PRIME)
