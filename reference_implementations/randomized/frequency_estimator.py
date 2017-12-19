from randomized.hash_family import Hash, generate_hash
from randomized.utils import median
from typing import Generic, Hashable, List, TypeVar

T = TypeVar('T', bound=Hashable)
U = TypeVar('U', bound=Hashable)


class FrequencyEstimator(Generic[T]):
    def __init__(self, num_estimators: int, num_buckets: int) -> None:
        self._estimators = \
            [SingleEstimator(num_buckets)
             for _ in range(num_estimators)]  # type: List[SingleEstimator[T]]

    def add_item(self, item: T) -> None:
        for estimator in self._estimators:
            estimator.add_item(item)

    def estimate(self, item: T) -> int:
        return median([e.estimate(item) for e in self._estimators])


class SingleEstimator(Generic[U]):
    def __init__(self, num_buckets: int) -> None:
        self._buckets = [0] * num_buckets
        # TODO: a bit of tight coupling here, creating Hash inside constructor
        self._index_hash = _generate_index_hash(num_buckets)
        self._sign_hash = _generate_sign_hash()

    def add_item(self, item: T) -> None:
        self._buckets[self._index_hash(item)] += self._sign_hash(item)

    def estimate(self, item: T) -> int:
        return self._buckets[self._index_hash(item)] * self._sign_hash(item)


def _generate_index_hash(x: int) -> Hash[int]:
    return generate_hash(4, range(x))


def _generate_sign_hash() -> Hash[int]:
    return generate_hash(4, [-1, 1])
