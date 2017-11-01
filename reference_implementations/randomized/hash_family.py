from random import randrange
from typing import Any, Generic, Hashable, Sequence, TypeVar

V = TypeVar('V')
H = TypeVar('H', bound=Hashable)

LARGE_PRIME = 2**61 - 1


class Hash(Generic[V]):
    def __init__(self, coefficients: Sequence[int], image: Sequence[V],
                 prime: int = LARGE_PRIME) -> None:
        # TODO: assert prime is actually prime
        if len(image) > prime:
            raise ValueError('prime field chosen not large enough for image')

        self._coefficients = tuple(coefficients)
        self._prime = prime
        self._image = image

    def __call__(self, item: H) -> V:
        x = hash(item)
        y = sum(c * x**p
                for p, c in enumerate(self._coefficients))  # type: int

        return self._image[(y % self._prime) % len(self._image)]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Hash) and \
                self._coefficients == other._coefficients


def generate_hash(k_independence: int, image: Sequence[V],
                  prime: int = LARGE_PRIME) -> Hash[V]:
    if k_independence < 1:
        raise ValueError('k_independence must be greater than 0')

    coefficients = [_random_coefficient(i == 0) for i in range(k_independence)]
    return Hash(coefficients, image, prime)


def _random_coefficient(allow_zero: bool = False) -> int:
    return randrange((0 if allow_zero else 1), LARGE_PRIME)
