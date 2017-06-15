import split
import numpy as np
from sklearn.covariance import EllipticEnvelope
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
import sklearn.metrics as skm

if __name__ == '__main__':
    scaler = StandardScaler()
    X, X_test, y, y_test = split.get_split()
    X = scaler.fit_transform(X)
    ee = EllipticEnvelope(contamination=.004)
    skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
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


    # ee.fit(X_train, y_train)
    # ee_predictions = ee.predict(X_test)
    # true_positives = -ee_predictions[np.where((y_test==1) & (ee_predictions==-1))].sum()
    # tpr = true_positives/y_test.sum()
    # false_positives = -ee_predictions[np.where((y_test==0) & (ee_predictions==-1))].sum()
    # print('True positives: {}, tpr: {}, false_positives: {}'.format(true_positives, tpr, false_positives))
    # print(skm.recall_score(y_test, ee_predictions), skm.confusion_matrix(y_test, ee_predictions))
