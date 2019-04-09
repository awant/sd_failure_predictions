
from collections import NamedTuple


# Probability for change
Prediction = NamedTuple('Prediction', ['probability', 'confidence'])


class KDD(object):
    """
    Hardcoded model from https://www.kdd.org/kdd2016/papers/files/adf0849-botezatuA.pdf
    """
    UNC_PREDICTION = Prediction(0, 0)
    HEALTHY_PREDICTION = Prediction(0, 1)

    def __init__(self):
        self._supported_models = ['Seagate', 'Hitachi']

    def _seagate_predict(self, metrics):
        if (metrics['smart_197_raw'] < 2 and metrics['smart_188_raw'] > 0
                and 0 <= metrics['smart_1_normalized'] < 117):
            return Prediction(0, 1)
        if metrics['smart_197_raw'] >= 2:
            return Prediction(1, 1)
        if (metrics['smart_197_raw'] < 2 and metrics['smart_188_raw'] > 0
                and metrics['smart_1_normalized'] > 117):
            return Prediction(1, 0.8)
        if (metrics['smart_197_raw'] < 2 and metrics['smart_188_raw'] == 0
                and metrics['smart_187_normalized'] < 100
                and metrics['smart_240_raw'] < 14780 * 10**6):
            return Prediction(1, 0.97)
        return HEALTHY_PREDICTION

    def _hitachi_predict(self, metrics):
        if (metrics['smart_197_raw'] > 1 and metrics['smart_3_raw'] > 626):
            return Prediction(1, 1)
        if (metrics['smart_197_raw'] > 5 and metrics['smart_3_raw'] < 626
                and metrics['smart_5_raw'] > 17):
            return Prediction(1, 0.92)
        if (metrics['smart_197_raw'] > 1 and metrics['smart_3_raw'] < 626
                and metrics['smart_5_raw'] < 17):
            return Prediction(1, 1)
        if (metrics['smart_197_raw'] < 1 and metrics['smart_5_raw'] < 7200
                and metrics['smart_3_raw'] > 629 and 0 <= metrics['smart_1_raw'] <= 109):
            return Prediction(0, 0.97)
        return HEALTHY_PREDICTION

    def predict(self, metrics):
        model = metrics.get('model', None)
        if model not in self._supported_models:
            return UNC_PREDICTION
        if model == 'Seagate':
            return self._seagate_predict(metrics)
        elif model == 'Hitachi':
            return self._hitachi_predict(metrics)
        return UNC_PREDICTION

