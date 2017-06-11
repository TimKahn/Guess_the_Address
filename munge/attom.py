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
    radius_df = df_near[df_near['distance'] <= radius]
    return radius_df

def find_matches(df_row):
    nearby_df = find_nearby(df_row, tax_df) #find properties +/- lat, lon tolerance to minimize distance calculations...
    radius_df = find_in_radius(df_row, nearby_df) #then find subset of those properties within 500m
    closest = radius_df[radius_df['true_distance'] <= .05] #look for true match within 50m of true address -- label this 1 if found.
    target = df_row['street_address'].split()
    attom_matches = []
    print('Target: {}'.format(target))
    for prop in closest.iterrows(): #check for matches within 50 meters
        address = prop[1]['PropertyAddressFull']
        if address.split()[0] == target[0]: #check for same street number
            street_name = target[1]
            if len(street_name) == 1: #if target[1] has length 1, it's the direction, so the street name is in target[2]
                street_name == target[2]
            if street_name in address.split():
                attom_matches.append(address)
    if len(attom_matches) == 0: #if no exact text matches, try matching the nearest property based on street number only
        nearest_property = radius_df.loc[radius_df.true_distance.argmin()]
        address = nearest_property['PropertyAddressFull']
        if address.split()[0] == target[0]:
            print('***Nearby: {}'.format(address))
            attom_matches.append(address)
        else: #if all else fails, try fuzzy-finding an address, but keep it only if street number is identical
            candidate, score, idx = process.extractOne(match['street_address'], radius_df['PropertyAddressFull'], scorer=fuzz.ratio, score_cutoff=75)
            if candidate.split()[0] == target[0]:
                print('YAY!  Fuzzy match: {}'.format(candidate))
                matches.append(candidate)
    print('Number of Matches: {}'.format(len(attom_matches)))
    df_row['attom_matches']
    return df_row

if __name__ == '__main__':
    matches_df = pd.read_csv('../data/matches_geo.csv')
    matches_df = matches_df.query("match_score >= 40 & distance <= .52 & room_type == 'Entire home/apt'")
    tax_df = pd.read_csv('../data/tax_assessor_denver.csv')
    tax_df = tax_df[tax_df['CompanyFlag'] != 'Y']
    matches_df['attom_matches'] = matches_df.apply(find_matches, axis=1)
