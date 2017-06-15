from sklearn.ensemble import IsolationForest
from sklearn.metrics import auc
import numpy as np
import split

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = split.get_split()
    ifo = IsolationForest(n_estimators=250, contamination=.025, n_jobs=-1, random_state=42)
    ifo.fit(X_train, y_train)
    predictions = ifo.predict(X_test)
    print(predictions[np.where(y_test==1)])
    print(len(predictions[np.where(predictions==-1)]))
