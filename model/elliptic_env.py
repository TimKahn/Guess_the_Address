import split
import numpy as np
from sklearn.covariance import EllipticEnvelope
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
import sklearn.metrics as skm

if __name__ == '__main__':
    # Note!  Using dummy variables may create a singular covariance matrix.  If so, remove logic to create dummies from ../munge/featurize.py
    scaler = StandardScaler()
    X, y = split.get_xy('../data/featurized_300.csv')
    X = scaler.fit_transform(X)
    ee = EllipticEnvelope(contamination=.02)
    skf = StratifiedKFold(n_splits=5, random_state=40, shuffle=True)
    for train, test in skf.split(X, y):
        ee.fit(X[train], y[train])
        predictions = ee.predict(X[test])
        predict_positive = -predictions[np.where(predictions==-1)].sum()
        actual_positives = y[test].sum()
        actual_negatives = len(y[test])-actual_positives
        true_positives = -predictions[np.where(y[test]*predictions==-1)].sum()
        false_positives = -predictions[np.where(y[test]+predictions==-1)].sum()
        TPR = true_positives/actual_positives
        FPR = false_positives/actual_negatives
        print('True positives: {}, TPR: {}, False Positives: {}, FPR: {}'.format(true_positives, TPR, false_positives, FPR))
        input('Press enter to continue...')
