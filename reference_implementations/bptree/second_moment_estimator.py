from math import ceil, log2
from randomized.hash_family import generate_hash, Hash
from randomized.utils import mean, median
from typing import Generic, Hashable, List, TypeVar


T1 = TypeVar('T1', bound=Hashable)
T2 = TypeVar('T2', bound=Hashable)


class SecondMomentEstimator(Generic[T1]):
    def __init__(self, num_estimators: int, num_buckets: int) -> None:
        self._estimators = \
            [SingleEstimator(num_buckets)
             for _ in range(num_estimators)]  # type: List[SingleEstimator[T1]]

    def add_item(self, item: T1) -> None:
        for estimator in self._estimators:
            estimator.add_item(item)

    def estimate(self) -> int:
        return median([estimator.estimate() for estimator in self._estimators])


class SingleEstimator(Generic[T2]):
    def __init__(self, num_buckets: int) -> None:
        self._buckets = [0] * num_buckets
        self._index_hash = _generate_index_hash(num_buckets)
        self._sign_hash = _generate_sign_hash()

    def add_item(self, item: T2) -> None:
        self._buckets[self._index_hash(item)] += self._sign_hash(item)

    def estimate(self) -> int:
        return sum(bucket ** 2 for bucket in self._buckets)


def _generate_index_hash(x: int) -> Hash[int]:
    return generate_hash(4, range(x))


def _generate_sign_hash() -> Hash:
    return generate_hash(8, [-1, 1])
