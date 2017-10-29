from countsketch.hash_family import generate_hash, Hash
from typing import Generic, Hashable, TypeVar

T = TypeVar('T', bound=Hashable)


# TODO: conform to typing.Counter?
class Counter(Generic[T]):
    def __init__(self, num_buckets: int) -> None:
        self._buckets = [0] * num_buckets
        # TODO: a bit of tight coupling here, creating Hash inside constructor
        self._index_hash = _generate_index_hash(num_buckets)  # type: Hash[int]
        self._sign_hash = _generate_sign_hash()  # type: Hash[int]

    def add_item(self, item: T) -> None:
        self._buckets[self._index_hash(item)] += self._sign_hash(item)

    def estimate_frequency(self, item: T) -> int:
        return self._buckets[self._index_hash(item)] * self._sign_hash(item)


def _generate_index_hash(x: int) -> Hash:
    return generate_hash(4, range(x))


def _generate_sign_hash() -> Hash:
    return generate_hash(4, [-1, 1])
