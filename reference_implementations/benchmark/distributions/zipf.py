from numpy.random import RandomState


def zipf(seed, size):
    state = RandomState(seed)

    for _ in range(size):
        yield state.zipf(1.6)
