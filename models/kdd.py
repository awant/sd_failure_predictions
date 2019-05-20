from collections import namedtuple
import pandas as pd
import numpy as np


# Probability for change
Prediction = namedtuple('Prediction', ['probability', 'confidence'])


class KDD_Hardcoded(object):
    """
    Hardcoded model from https://www.kdd.org/kdd2016/papers/files/adf0849-botezatuA.pdf
    Used only these SMART atttributes:
    Seagate:
        smart_188_raw
        smart_197_raw
        smart_240_raw
        smart_1_normalized
        smart_187_normalized
    Hitachi:
        smart_1_raw
        smart_3_raw
        smart_5_raw
        smart_197_raw
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
        return self.HEALTHY_PREDICTION

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
        return self.HEALTHY_PREDICTION

    def _predict(self, metrics):
        vendor = metrics.get('vendor', 'Seagate')
        if vendor and (vendor not in self._supported_models):
            return self.UNC_PREDICTION
        if vendor == 'Seagate':
            return self._seagate_predict(metrics)
        elif vendor == 'Hitachi':
            return self._hitachi_predict(metrics)
        return self.UNC_PREDICTION

    def _predict_pd(self, df):
        predictions = []
        for _, metrics in df.iterrows():
            prob = self._predict(metrics).probability
            predictions.append(prob)
        return np.array(predictions)

    def predict(self, df):
        if isinstance(df, pd.DataFrame):
            return self._predict_pd(df)

