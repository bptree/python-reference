
class F2_Estimator(object):
    def __init__(self):
        pass

    def update_estimate(self, item):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

class Brute_Force_F2_Estimator(F2_Estimator):
    def __init__(self, n):
        self.f = [0]*n
