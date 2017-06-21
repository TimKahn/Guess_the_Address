import pandas as pd
import numpy as np
import geopy.distance
from scipy.stats import beta, gamma, sem
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from matplotlib import cm
# plt.style.use('ggplot')
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
    xmin, xmax = 0, 525
    x = np.linspace(xmin, xmax, 200)
    ax.plot(x, gauss0.pdf(x))
    ax.plot(x, gauss1.pdf(x))
    plt.xlabel('Distance from circle center (meters)')
    plt.ylabel('Fraction of addresses')
    # ax.axvline(x=gauss0.ppf(.99), color='grey')
    plt.show()

def get_distances(df_row):
    lat1 = df_row['latitude']
    lon1 = df_row['longitude']
    lat2 = df_row['true_latitude']
    lon2 = df_row['true_longitude']
    lat_dir = (lat2-lat1)/abs(lat2-lat1) # 1 if address is north of circle center, -1 if south
    lon_dir = (lon2-lon1)/abs(lon2-lon1) # 1 if address is east of circle center, -1 if west
    df_row['lat_distance'] = geopy.distance.vincenty((lat1, lon1), (lat2, lon1)).km*1000*lat_dir
    df_row['lon_distance'] = geopy.distance.vincenty((lat1, lon1), (lat1, lon2)).km*1000*lon_dir
    return df_row

def plot_distances_2d(matches):
    fig, ax = plt.subplots(figsize=(8,8))
    plt.rcParams.update({'font.size': 18})
    circle1 = plt.Circle((0, 0), 500, color='.8', zorder=-3)
    circle2 = plt.Circle((0, 0), 300, color='.7', zorder=-2)
    circle3 = plt.Circle((0, 0), 200, color='cyan', zorder=-1)
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)
    ax.scatter(0, 0, s=60, color='red')
    ax.scatter(matches.lon_distance, matches.lat_distance, marker=(3,0,0), s=80, color='blue', alpha=.8, zorder=1, label='True Address')
    ax.vlines(x=200, ymin=-550, ymax=0, color='red', linestyle='--', linewidth=1.2)
    ax.vlines(x=300, ymin=-550, ymax=0, color='red', linestyle='--', linewidth=1.2)
    ax.set_xlim([-550, 550])
    ax.set_ylim([-550, 550])
    ax.set_xticks([-500, 0, 200, 300, 500])
    ax.set_yticks([])
    ax.spines['bottom'].set_color('grey')
    ax.xaxis.label.set_color('grey')
    ax.tick_params(axis='x', colors='grey')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # plt.legend(loc='upper left')
    plt.savefig('../visualize/distance_2d.png', dpi=600, transparent=True)
    # plt.show()

if __name__ == '__main__':
    plt.close('all')
    matches = pd.read_csv('../data/final_validated.csv')
    distances = matches.listing_distance.apply(lambda x: 1000*x).values.reshape((-1, 1)) #convert to meters, put in nx1 array.
    matches = matches.apply(get_distances, axis=1)
    plot_distances_2d(matches)
    # fit_gauss_mix(distances)
    # fit_gamma(distances)
    # fit_beta(distances)
