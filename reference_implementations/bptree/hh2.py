from bptree.second_moment_estimator import SecondMomentEstimator
from bptree.hh1 import HH1
from math import sqrt
from typing import cast, Generic, Hashable, Optional, TypeVar


T = TypeVar('T', bound=Hashable)


class HH2(Generic[T]):
    def __init__(self, n: int) -> None:
        self.n = n
        self.current_hh1 = None  # type: Optional[HH1[T]]
        self.next_hh1 = HH1(1, self.n)  # type: HH1[T]
        self.f2_estimator = \
            SecondMomentEstimator(1, 30)  # type: SecondMomentEstimator[T]
        self.k = 1

    def add_item(self, item: T) -> None:
        self.f2_estimator.add_item(item)
        f2_estimate = self.f2_estimator.estimate()

        # If we've crossed a threshold move HH1_k to HH1_k-1 and make a new HH1
        if f2_estimate >= 2**self.k:
            self.current_hh1 = self.next_hh1
            self.next_hh1 = HH1(sqrt(f2_estimate), self.n)
            self.k += 1

        # Pass the item into our two most recent HH1s
        for hh1 in filter(None, (self.current_hh1, self.next_hh1)):
            cast(HH1[T], hh1).add_item(item)

    def get_heavy_hitter(self) -> Optional[T]:
        if self.current_hh1 is not None:
            return self.current_hh1.get_heavy_hitter()

        return None
