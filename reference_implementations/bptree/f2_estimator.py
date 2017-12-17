
class F2_Estimator(object):
    def __init__(self):
        pass

    def add_item(self, item):
        raise NotImplementedError

    def update_estimate(self):
        raise NotImplementedError

class Brute_Force_F2_Estimator(F2_Estimator):
    def __init__(self, n):
        self.f = [0]*n
        self.F2 = 0

    def add_item(self, item):
        self.f[item] += 1

    def update_estimate(self):
        self.F2 = 0
        for freq in self.f:
            self.F2 += freq**2
        return self.F2
