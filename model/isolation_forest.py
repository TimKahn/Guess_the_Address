from sklearn.ensemble import IsolationForest
from sklearn.model_selection import StratifiedKFold
import numpy as np
import split

if __name__ == '__main__':
    X, y = split.get_xy('../data/featurized_300.csv')
    ifo = IsolationForest(n_estimators=250, contamination=.1, n_jobs=-1, random_state=42)
    skf = StratifiedKFold(n_splits=5, random_state=40, shuffle=True)
    for train, test in skf.split(X, y):
        ifo.fit(X[train], y[train])
        predictions = ifo.predict(X[test])
        predict_positive = -predictions[np.where(predictions==-1)].sum()
        actual_positives = y[test].sum()
        actual_negatives = len(y[test])-actual_positives
        true_positives = -predictions[np.where(y[test]*predictions==-1)].sum()
        false_positives = -predictions[np.where(y[test]+predictions==-1)].sum()
        TPR = true_positives/actual_positives
        FPR = false_positives/actual_negatives
        print('True positives: {}, TPR: {}, False Positives: {}, FPR: {}'.format(true_positives, TPR, false_positives, FPR))
