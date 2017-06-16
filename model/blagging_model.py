from blagging import BlaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import auc, roc_auc_score, roc_curve, precision_recall_curve
from scipy import interp
import matplotlib.pyplot as plt
import split

def plot_ROC_curve(classifier, X, y, pos_label=1, n_folds=3):
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []
    skf = StratifiedKFold(n_splits=n_folds, random_state=42, shuffle=True)
    i = 1
    for train, test in skf.split(X, y):
        classifier.fit(X[train], y[train])
        probas_ = classifier.predict_proba(X[test])
        for t in [.68, .7, .72]:
            predictions = np.array([1 if p > t else 0 for p in probas_[:,1]])
            true_positives = predictions[np.where(predictions + y[test] == 2)].sum()
            actual_positives = y[test].sum()
            false_positives = predictions.sum() - true_positives
            print(t, true_positives, actual_positives, false_positives/true_positives)
        # Compute ROC curve and area under the curve
        fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1], pos_label=1)
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
        i += 1
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Random')
    mean_tpr /= n_folds
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
    plt.axvline(x=.1)
    plt.axhline(y=.6)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate (of ~35,000 addresses)')
    plt.ylabel('True Positive Rate (of ~100 addresses)')
    plt.title('ROC curve')
    plt.legend(loc="lower right")
    plt.show()

def plot_PR_curve(classifier, X, y, n_folds=5):
    skf = StratifiedKFold(n_splits=n_folds, random_state=42, shuffle=True)
    i = 1
    for train, test in skf.split(X, y):
        classifier.fit(X[train], y[train])
        probas_ = classifier.predict_proba(X[test])
        precision, recall, thresholds = precision_recall_curve(y[test], probas_[:,1], pos_label=1)
        plt.plot(recall, precision, lw=1, label='PR fold %d' % (i,))
        i += 1
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-recall curve')
    plt.legend(loc="lower right")
    plt.show()

if __name__ == '__main__':
    plt.close('all')
    X_train, X_test, y_train, y_test = split.get_split()
    bc = BlaggingClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    plot_ROC_curve(bc, X_train, y_train)

    # cl = AdaBoostClassifier()
    # plot_ROC_curve(cl, X_train, y_train)
