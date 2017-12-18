from math import ceil, log2
from randomized.hash_family import generate_hash, Hash
from randomized.utils import assert_percentage, mean, median
from typing import Generic, Hashable, List, TypeVar


T1 = TypeVar('T1', bound=Hashable)
T2 = TypeVar('T2', bound=Hashable)


class SecondMomentEstimator(Generic[T1]):
    def __init__(self, error_margin: float, correctness: float) -> None:
        assert_percentage(correctness, 'correctness')

        num_estimates = ceil(2 * log2(1 / correctness))
        self._estimators = \
            [SingleEstimator(error_margin)
             for _ in range(num_estimates)]  # type: List[SingleEstimator[T1]]

    def add_item(self, item: T1) -> None:
        for estimator in self._estimators:
            estimator.add_item(item)

    def estimate(self) -> int:
        return median([estimator.estimate() for estimator in self._estimators])


class SingleEstimator(Generic[T2]):
    def __init__(self, error_margin: float) -> None:
        assert_percentage(error_margin, 'correctness')
        num_buckets = ceil(16 / (error_margin ** 2))

        self._buckets = [0] * num_buckets
        self._sign_hashes = [_generate_sign_hash() for _ in range(num_buckets)]

    def add_item(self, item: T2) -> None:
        for i, sign_hash in enumerate(self._sign_hashes):
            self._buckets[i] += sign_hash(item)

    def estimate(self) -> int:
        return int(mean(bucket ** 2 for bucket in self._buckets))


def _generate_sign_hash() -> Hash:
    return generate_hash(8, [-1, 1])
