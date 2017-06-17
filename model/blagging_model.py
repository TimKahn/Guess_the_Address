from blagging import BlaggingClassifier
from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
from xgboost import XGBClassifier
import numpy as np
import evaluation as ev #evaluation functions and plotting
import split
import matplotlib.pyplot as plt


if __name__ == '__main__':
    plt.close('all')
    X, y = split.get_split()
    bc = BlaggingClassifier(base_estimator=DecisionTreeClassifier(criterion='entropy', max_features=.6), n_estimators=200, random_state=42, n_jobs=-1)
    ev.plot_ROC_curve(bc, X, y, 'r--')
    xg = XGBClassifier()
    ev.plot_ROC_curve(xg, X, y, 'b--')
