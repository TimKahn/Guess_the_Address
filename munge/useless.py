#Note: pad latitude by .005, longitude by .0065

import pandas as pd

def append_geo(df):
    service, prop_id = df['service'], df['id_other']
    if service == 'VRBO':
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = vrbo.iloc['full_address'], vrbo['street_address'], vrbo['zipcode'], vrbo['gmaps_place_id']
    else:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id']  = homeaway['full_address'], homeaway['street_address'], homeaway['zipcode'], homeaway['gmaps_place_id']
    return df

if __name__ == '__main__':
    matches = pd.read_csv('../data/matches.csv')
    matches = matches.query("score >= 85 & distance <= .5 & room_type == 'Entire home/apt'")
    df_a = pd.read_csv('../data/airbnb_denver.csv')
    # positive_class = df_a[df_a['airbnb_property_id'].isin(matches['airbnb_property_id'])]
    matches.sort_values('airbnb_property_id', inplace=True)
    matches.reindex(matches['airbnb_property_id'])
    df_a.sort_values('airbnb_property_id', inplace=True)
    df_a.reindex(df_a['airbnb_property_id'])
    positive_class = pd.concat([df_a, matches], join='inner', axis = 1)
    vrbo = pd.read_pickle('../data/vrbo.pkl')
    homeaway = pd.read_pickle('../data/homeaway.pkl')
    positive_class.apply(append_geo, axis=1)
