import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.metrics import confusion_matrix
import split

def get_cost_benefit(revenue, cost):
    '''
    Takes two integers: Revenue of correctly identified property, and mechanical turk cost per property
    Returns cost-benefit matrix
    '''
    benefit = revenue - cost
    cost = -cost
    return np.array([[benefit, cost],[0, 0]])

def standard_confusion_matrix(y_true, y_pred):
    """Make confusion matrix with format:
                  -----------
                  | TP | FP |
                  -----------
                  | FN | TN |
                  -----------
    """
    [[tn, fp], [fn, tp]] = confusion_matrix(y_true, y_pred)
    return np.array([[tp, fp], [fn, tn]])

def profit_curve(predicted_probs, labels, revenue, cost, thresholds):
    """Calculates a list of profits based on:
    1) cost-benefit matrix;
    2) predicted probabilities of data points;
    3) the true labels.

    Parameters
    ----------
    predicted_probs : ndarray - 1D, predicted probability for each datapoint
                                    in labels, in range [0, 1]
    labels          : ndarray - 1D, true label of datapoints, 0 or 1

    Returns
    -------
    profits    : ndarray - 1D
    thresholds : ndarray - 1D
    """
    actual_positives = float(sum(labels))
    cost_benefit = get_cost_benefit(revenue, cost)
    profits = []
    pred_positive_rates = []
    for threshold in thresholds:
        y_predict = np.array([1 if p >= threshold else 0 for p in predicted_probs])
        confusion_matrix = standard_confusion_matrix(labels, y_predict)
        threshold_profit = np.sum(confusion_matrix * cost_benefit)/actual_positives #divide by n_obs to get 'per observation' profit
        # print(confusion_matrix)
        # print(threshold_profit)
        # print('----------------')
        profits.append(threshold_profit)
    return np.array(profits)

def plot_avg_profits(classifier, n_splits=5, revenue=50, cost=1.50):
    plt.close('all')
    fig = plt.figure(figsize=(10,8))
    ax1 = fig.add_subplot(1,1,1)
    X, y = split.get_xy()
    skf = StratifiedKFold(n_splits=n_splits, random_state=40, shuffle=True)
    thresholds = np.linspace(.05, 1, 200)
    avg_profits = np.zeros(len(thresholds))
    i=1
    for train, test in skf.split(X, y):
        print('Predicting fold {}...'.format(i))
        classifier.fit(X[train], y[train])
        predicted_probs = classifier.predict_proba(X[test])[:,1]
        profits = profit_curve(predicted_probs, y[test], revenue, cost, thresholds)
        avg_profits += profits
        i += 1
        # plot_model_profits(y[test], predicted_probs, revenue, cost, ax1)
    ax1.plot(thresholds, avg_profits*10000)
    plt.title("Profit Curve")
    plt.xlabel("<-- Classify everything as a match | Classify nothing as a match -->")
    plt.ylabel("Profit per 10,000 AirBNB properties")
    plt.ylim([-250000, 1250000])
    # plt.legend(loc='best')
    plt.tight_layout()
    plt.show()
    return

if __name__ == '__main__':
    plot_all_profits()
