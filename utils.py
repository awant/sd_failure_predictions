import numpy as np

### Metircs


def FAR(y_true, y_pred):
    '''
    False alarm rate / false positive rate
    '''
    assert isinstance(y_true, np.ndarray) and isinstance(y_pred, np.ndarray)
    y_pred = (y_pred >= 0.5).astype(int)
    FP = ((y_true == 0) * (y_true != y_pred)).sum()
    TN = ((y_true == 0) * (y_true == y_pred)).sum()
    return FP / (FP + TN)


def FDR(y_true, y_pred):
    '''
    Failure detection rate
    '''
    y_pred = (y_pred >= 0.5).astype(int)
    TP = ((y_true == 1) * (y_true == y_pred)).sum()
    return TP / len(y_true)


def FNR(y_true, y_pred):
    '''
    False negative rate
    '''
    y_pred = (y_pred >= 0.5).astype(int)
    TP = ((y_true == 1) * (y_true == y_pred)).sum()
    FN = ((y_true == 1) * (y_true != y_pred)).sum()
    return FN / (FN + TP)

