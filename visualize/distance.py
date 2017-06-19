import pandas as pd
import numpy as np
from scipy.stats import beta, gamma, sem
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import scipy.stats as scs

def fit_gamma(distances):
    a, loc, scale = gamma.fit(distances)
    print(a, loc, scale)
    fig, ax = plt.subplots(1, 1)
    ax.hist(distances, normed=True, bins=20)
    xt = plt.xticks()[0]
    xmin, xmax = min(xt), max(xt)
    lnspc = np.linspace(xmin, xmax, len(distances))
    pdf = gamma.pdf(lnspc, a, loc, scale)
    q = .95
    ax.axvline(x = gamma.ppf(q, a, loc, scale), color='grey', label='{} quantile'.format(q))
    ax.plot(lnspc, pdf, label="Gamma")
    ax.legend()
    plt.show()

def fit_beta(distances):
    # a, b, loc, scale = 2, 5, distances.mean(), sem(distances)[0]
    a, b, loc, scale = beta.fit(distances)
    print(a, b, loc, scale)
    fig, ax = plt.subplots(1, 1)
    ax.hist(distances, normed=True, bins=20)
    xt = plt.xticks()[0]
    xmin, xmax = min(xt), max(xt)
    lnspc = np.linspace(xmin, xmax, len(distances))
    pdf = beta.pdf(lnspc, a, b, loc, scale)
    ax.plot(lnspc, pdf, label="Beta")
    plt.show()

def fit_gauss_mix(distances):
    # labels = np.array([1 if x > 300 else 0 for x in distances])
    # mean0 = distances[np.where(labels==0)].mean()
    # mean1 = distances[np.where(labels==1)].mean()
    # means_init = np.array([mean0, mean1]).reshape((-1,1))
    gm = GaussianMixture(n_components=2, random_state=42)
    gm.fit(distances)
    means, covs = gm.means_.flatten(), gm.covariances_.flatten()
    gauss0 = scs.norm(loc=means[0], scale=covs[0]**.5)
    gauss1 = scs.norm(loc=means[1], scale=covs[1]**.5)
    print('AIC: {}, BIC: {}'.format(gm.aic(distances), gm.bic(distances)))
    fig, ax = plt.subplots(1, 1)
    ax.hist(distances, normed=True, bins=20)
    xmin, xmax = 0, 600
    x = np.linspace(xmin, xmax, 200)
    ax.plot(x, gauss0.pdf(x))
    ax.plot(x, gauss1.pdf(x))
    ax.axvline(x=gauss0.ppf(.99), color='grey')
    plt.show()

if __name__ == '__main__':
    plt.close('all')
    matches = pd.read_csv('../data/final_validated.csv')
    distances = matches.listing_distance.apply(lambda x: 1000*x).values.reshape((-1, 1)) #convert to meters, put in nx1 array.
    fit_gauss_mix(distances)
    # fit_gamma(distances)
    # fit_beta(distances)
