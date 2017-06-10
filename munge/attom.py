import pandas as pd
import geopy.distance
from fuzzywuzzy import fuzz, process

def get_distance(row, lat, lon):
    '''
    Takes a row from attom data and a fixed lat & lon; returns the distance.
    '''
    return geopy.distance.vincenty((lat, lon), (row['PropertyLatitude'], row['PropertyLongitude'])).km

def find_nearby(match, df):
    '''
    INPUTS: a single VRBO/Homeaway-to-AirBNB matched property; tax assessor data.
    OUTPUT: dataframe of properties within a lat/lon tolerance of the property.
    '''
    lat_pad = .005 #lat/lon pads correspond to ~550m.
    lon_pad = .0065
    lat = match['latitude']
    lon = match['longitude']
    lat_max = lat + lat_pad
    lat_min = lat - lat_pad
    lon_max = lon + lon_pad
    lon_min = lon - lon_pad
    df_near = df[(df['PropertyLatitude'] > lat_min) & (df['PropertyLatitude'] < lat_max) & (df['PropertyLongitude'] > lon_min) & (df['PropertyLongitude'] < lon_max)]
    return df_near

def find_in_radius(match, df_near):
    radius = .5
    df_near['distance'] = df_near.apply(lambda row: get_distance(row, match['latitude'], match['longitude']), axis=1)
    df_near['true_distance'] = df_near.apply(lambda row: get_distance(row, match['true_latitude'], match['true_longitude']), axis=1)
    df_radius = df_near[df_near['distance'] <= radius]
    find_true_match(match, df_radius)
    return df_radius

def find_true_match(match, df_radius):
    target = match['street_address'].split()
    closest = df_radius[df_radius['true_distance'] <= .1]
    matches = []
    print('Target: {}'.format(target))
    for address in closest['PropertyAddressFull']:
        if address.split()[0] == target[0]:
            street_name = target[1]
            if len(street_name) == 1:
                street_name == target[2]
            if street_name in address.split():
                matches.append(address)
    if len(matches) == 0:
        nearest = closest.loc[closest.true_distance.argmin(), 'PropertyAddressFull']
        if nearest.split()[0] == target[0]:
            matches.append(nearest)
        else:
            candidate = process.extractOne(match['street_address'], closest['PropertyAddressFull'], scorer=fuzz.ratio)[0]
            if candidate.split()[0] == target[0]:
                matches.append(candidate)
    print('Number of Matches: {}'.format(len(matches)))
    return


def find_all(matches_df, tax_df):
    for match in matches_df.iterrows():
        match = match[1]
        df_near = find_nearby(match, tax_df) #find properties +/- lat, lon tolerance
        df_radius = find_in_radius(match, df_near) #find properties within 500m
        find_true_match(match, df_radius)
    return

if __name__ == '__main__':
    matches_df = pd.read_csv('../data/matches_geo.csv')
    tax_df = pd.read_csv('../data/tax_assessor_denver.csv')
    tax_df = tax_df[tax_df['CompanyFlag'] != 'Y']
    find_all(matches_df, tax_df)
