from blagging import BlaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.combine import SMOTETomek, SMOTEENN
from imblearn.over_sampling import SMOTE, RandomOverSampler
import numpy as np
import roc_curve2 as rc2
import profit_avg
import split

if __name__ == '__main__':
    filename = '../data/featurized_500.csv'
    X, y = split.get_xy(filename)
    ros = RandomOverSampler()
    smt = SMOTETomek(ratio=.01)
    sme = SMOTEENN(ratio=.01)
    # gnb = GaussianNB()
    # rf = RandomForestClassifier(n_estimators=200, class_weight = 'balanced_subsample', random_state=42, n_jobs=-1)
    # knn = KNeighborsClassifier(n_neighbors=10)
    # adb = AdaBoostClassifier(n_estimators=200, learning_rate=.2, random_state=42)
    dtc = DecisionTreeClassifier(criterion='entropy', max_features=.6, min_samples_split=6)
    xg = XGBClassifier(scale_pos_weight=10, max_delta_step=1, colsample_bytree=.8, colsample_bylevel=.8, seed=42)
    blag = BlaggingClassifier(base_estimator=dtc, n_estimators=200, random_state=42, n_jobs=-1)
    xg2 = XGBClassifier(scale_pos_weight=10, max_delta_step=1, colsample_bytree=1, colsample_bylevel=.5, seed=42)
    blag_boost = BlaggingClassifier(base_estimator=xg2, random_state=42, n_jobs=-1)
    classifiers = [xg2]
    balancing = []
    # profit_avg.plot_avg_profits(blag, filename, revenue=50, cost=1)
    profit_avg.plot_avg_profits(xg2, filename, revenue=12.50, cost=.25)
    # rc2.plot_ROC_curve(classifiers, X, y, balancing=balancing, benchmarks=(.4, .7), save_path='../visualize/roc_xg_benchmarked.png')
