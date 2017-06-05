'''
This script finds the AirBNB property with a title most similar to a VRBO or Homeaway property.
'''

import pandas as pd

if __name__ == '__main__':
    cols = ['gmaps_place_id', 'service', 'prop_id', 'title']
    vrbo = pd.read_pickle('../data/vrbo.pkl')
    vrbo['service'] = 'VRBO'
    df_v = vrbo[['gmaps_place_id', 'service', 'listingNumber', 'headline']]
    df_v.columns = cols
    homeaway = pd.read_pickle('../data/homeaway.pkl')
    homeaway['service'] = 'Homeaway'
    df_h = homeaway[['gmaps_place_id', 'service', 'homeaway_property_id', 'title']]
    df_h.columns = cols
    df_all = pd.concat([df_h, df_v], axis=0)
    df_all.drop_duplicates('prop_id', inplace='True')
