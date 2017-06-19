import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

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

def profit_curve(predicted_probs, labels, revenue, cost):
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
    n_obs = float(len(labels))
    cost_benefit = get_cost_benefit(revenue, cost)
    thresholds = np.linspace(.01, 1, 200)
    profits = []
    pred_positive_rates = []
    for threshold in thresholds:
        y_predict = predicted_probs >= threshold
        positive = np.sum(y_predict)
        pred_positive_rates.append(positive/y_predict.shape[0])
        confusion_matrix = standard_confusion_matrix(labels, y_predict)
        threshold_profit = np.sum(confusion_matrix * cost_benefit) / positive #divide by positive to get per-property profit
        # print(confusion_matrix)
        # print(threshold_profit)
        # print('----------------')
        profits.append(threshold_profit)
    return np.array(profits), np.array(thresholds), np.array(pred_positive_rates)

def plot_model_profits(cost_fraud, cost_investigate, save_path='static/img/'):
    """Plotting function to compare profit curves of different models.

    Parameters
    ----------
    save_path: str, file path to save the plot to. If provided plot will be saved and not shown.
    """
    plt.close('all')
    labels = get_labels()
    predicted_probs = get_predicted_probs()
    profits, thresholds, flag_rates = profit_curve(predicted_probs, labels, cost_fraud, cost_investigate)
    # percentages = np.linspace(0, 100, profits.shape[0])
    # plt.plot(thresholds, profits)
    fig = plt.figure(figsize=(10,8))
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(thresholds, profits*flag_rates*10000)
    plt.title("Profit Curve")
    plt.xlabel("Flag case if fraud probability is greater than...")
    plt.ylabel("Profit per 10,000 events")
    # plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(save_path+str(cost_fraud)+'_'+str(cost_investigate)+'.png')
    return
