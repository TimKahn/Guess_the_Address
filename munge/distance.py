import pandas as pd
import numpy as np
from scipy.stats import beta, gamma
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

def fit_gamma(distances):
    a, loc, scale = gamma.fit(distances)
    print(a, loc, scale)
    fig, ax = plt.subplots(1, 1)
    ax.hist(distances, normed=True, bins=20)
    xt = plt.xticks()[0]
    xmin, xmax = min(xt), max(xt)
    lnspc = np.linspace(xmin, xmax, len(distances))
    pdf = gamma.pdf(lnspc, a, loc, scale)
    ax.plot(lnspc, pdf, label="Gamma")
    plt.show()

if __name__ == '__main__':
    plt.close('all')
    matches = pd.read_pickle('../data/single_matches.pkl')
    # matches = matches.query('true_distance <= .3')
    distances = matches.true_distance.apply(lambda x: 1000*x)
