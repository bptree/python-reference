def HH2(stream):
    # This is HH1_k-1
    hh1_0 = HH1(1)
    # This is HH1_k
    hh1_1 = 0

    F2 = F2_estimator()
    k = 1
    for item in stream:
        f2_estimate = F2.compute_next(item)
        # If we've crossed a threshold move HH1_k to HH1_k-1 and make a new HH1
        if f2_estimate >= 2**k:
            hh1_0 = hh1_1
            hh1_1 = HH1(F2.value)
            k += 1

        hh1_0.compute_next(item)
        hh1_1.compute_next(item)

    return hh1_0.get_value()


class F2_estimator():
    def __init__():
        # Do stuff
        pass

    def compute_next():
        # Takes in another item and returns the new F2 estimate
        pass
