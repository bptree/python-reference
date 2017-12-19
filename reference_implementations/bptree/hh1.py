from bitarray import bitarray
from math import floor, log2
from randomized.hash_family import generate_hash, Hash
from struct import pack
from typing import Generic, Hashable, Optional, TypeVar


C = 1 / 32
BETA = 3 / 4
T = TypeVar('T', bound=Hashable)


class HH1(Generic[T]):
    def __init__(self, stddev_estimate: float, n: int) -> None:
        self._stddev_estimate = stddev_estimate
        self._num_hash_bits = 3 * floor(log2(min(n, stddev_estimate**2) + 1))
        self._sign_hash = _generate_sign_hash()
        self._hash = generate_hash(2, range(2**self._num_hash_bits))
        self._learned_hash = bitarray()
        self._buckets = [0, 0]
        self._heavy_hitter = None  # type: Optional[T]

    def add_item(self, item: T) -> None:
        if self.is_done():
            return

        hash_value = int_to_bitarray(self._hash(item))

        # If it does match the HH, add its contribution to X_0/1
        if self._learned_hash == hash_value[:len(self._learned_hash)]:
            self._heavy_hitter = item

            bucket = hash_value[len(self._learned_hash)]
            self._buckets[bucket] += self._sign_hash(item)

            # If we've seen enough items for the HH to have made itself known
            # then record the next bit into b
            if abs(sum(self._buckets)) >= \
                    (C * self._stddev_estimate * BETA**len(self._learned_hash)):
                # Record the bit
                bit = abs(self._buckets[1]) > abs(self._buckets[0])
                self._learned_hash.append(bit)

                # Refresh everything
                self._buckets = [0, 0]
                self._sign_hash = _generate_sign_hash()

    def get_heavy_hitter(self) -> Optional[T]:
        return self._heavy_hitter if self.is_done() else None

    def is_done(self) -> bool:
        return len(self._learned_hash) == self._num_hash_bits


def int_to_bitarray(x):
   a = bitarray()
   a.frombytes(pack('q', x))
   return a


def _generate_sign_hash() -> Hash:
    return generate_hash(4, [-1, 1])
