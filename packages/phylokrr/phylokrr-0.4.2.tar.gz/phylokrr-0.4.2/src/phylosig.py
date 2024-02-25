from phylokrr.kernels import KRR

class PagelsLambda:

    def __init__(self, bounds = (0.1, 1), model = KRR(kernel='rbf')):
        self.bounds = bounds
        self.model = model

    def fit(self, model, X, y, vcv):
        pass


