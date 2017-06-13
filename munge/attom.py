import pandas as pd
import geopy.distance
from fuzzywuzzy import fuzz, process
import re

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
    radius = .51
    df_near['distance'] = df_near.apply(lambda row: get_distance(row, match['latitude'], match['longitude']), axis=1)
    df_near['true_distance'] = df_near.apply(lambda row: get_distance(row, match['true_latitude'], match['true_longitude']), axis=1)
    radius_df = df_near[df_near['distance'] <= radius]
    return radius_df

def test_address(address, target):
    if address.split()[0] == target[0]: #check for same street number
        street_name = target[1]
        if len(street_name) == 1: #if target[1] has length 1, it's the direction, so the street name is in target[2]
            street_name == target[2]
        if street_name in address.split():
            return True
        else:
            return False

def alternate_matching(address, target):
    if address.split()[0] == target[0]: #Just test street number in this case -- maybe some small difference in street name
        print('***Nearby: {}'.format(address))
        return True
    # else: #if all else fails, try fuzzy-finding an address, but keep it only if street number is identical
    #     try:
    #         address, score, idx = process.extractOne(df_row['street_address'], radius_df['PropertyAddressFull'], scorer=fuzz.ratio, score_cutoff=75)
    #         if test_address(address, target):
    #             print('YAY!  Fuzzy match: {}'.format(address))
    #             return True
    #     except:
    #         return False

def find_matches(df_row):
    nearby_df = find_nearby(df_row, tax_df) #find properties +/- lat, lon tolerance to minimize distance calculations...
    radius_df = find_in_radius(df_row, nearby_df) #then find the subset of those properties within 500m
    closest = radius_df[radius_df['true_distance'] <= .05] #we'll look within 50m of true address to find a match in the tax assessor data.
    target = df_row['street_address'].split()
    attom_matches = []
    print('Target: {}'.format(target))
    for prop in closest.iterrows(): #check for matches within 50 meters
        attom_id, address = prop[1]['[ATTOM ID]'], prop[1]['PropertyAddressFull']
        if test_address(address, target):
            attom_matches.append(attom_id)
    if len(attom_matches) == 0: #if no exact text matches, try matching the nearest property based on street number only
        nearest_property = radius_df.loc[radius_df.true_distance.argmin()]
        address = nearest_property['PropertyAddressFull']
        if alternate_matching(address, target):
            attom_matches.append(attom_id)
    print('Number of Matches: {}'.format(len(attom_matches)))
    df_row['attom_matches'] = attom_matches
    df_row['number_of_matches'] = len(attom_matches)
    return df_row

def parse_names(df_row):
    if any(re.findall(r'&amp|\Wand', df_row['first_name'], re.IGNORECASE)):
        names = df_row['first_name'].split()
        df_row['first_name2'] = names[2]
        df_row['first_name'] = names[0]
    return df_row

def get_host_names(airbnb_df):
    hosts_df = pd.read_csv('../data/denver_hosts.csv')
    hosts_df = hosts_df[['airbnb_host_id', 'first_name']]
    airbnb_df = airbnb_df.merge(hosts_df, on='airbnb_host_id', how='left')
    airbnb_df['first_name'].fillna('', inplace=True)
    airbnb_df = airbnb_df.apply(parse_names, axis=1)
    airbnb_df['first_name2'].fillna('', inplace=True)
    return airbnb_df

def process_airbnb(airbnb_df):
    cols_a = ['airbnb_property_id', 'match_score', 'true_latitude', 'true_longitude',
       'prop_id_crosslist', 'title_crosslist', 'crosslisted_on',  'airbnb_host_id', 'first_name', 'first_name2', 'latitude', 'longitude', 'description', 'title',
       'property_type', 'bedrooms', 'bathrooms', 'accomodates', 'pets_allowed', 'aircon', 'heating', 'elevator', 'pool', 'gym', 'indoor_fireplace', 'full_address', 'street_address', 'zipcode', 'gmaps_place_id', 'distance', 'attom_matches']
    airbnb_df = get_host_names(airbnb_df)
    airbnb_df = airbnb_df.loc[:, cols_a]
    airbnb_df['attom_id'] = airbnb_df['attom_matches'].apply(lambda x: x[0])
    return airbnb_df

def append_neighbors(airbnb_df, tax_df):
    new_df = pd.DataFrame([])
    for idx, row in airbnb_df.iterrows():
        print(row['title'])
        nearby_df = find_nearby(row, tax_df) #find properties +/- lat, lon tolerance to minimize distance calculations...
        radius_df = find_in_radius(row, nearby_df) #then find the subset of those properties within 500m
        radius_df['airbnb_property_id'] = row.loc['airbnb_property_id']
        radius_df['MATCH'] = radius_df['[ATTOM ID]'].apply(lambda x: x == row['attom_id'])
        radius_df['neighbor_count'] = radius_df.shape[0]
        new_df = new_df.append(radius_df)
    new_df = new_df.merge(airbnb_df, on='airbnb_property_id', how='left')
    return new_df

if __name__ == '__main__':
    # matches_df = pd.read_csv('../data/matches_geo.csv')
    # matches_df = matches_df.query("match_score >= 40 & distance <= .51 & room_type == 'Entire home/apt'")
    # print('NUMBER OF POTENTIAL MATCHES: {}'.format(matches_df.shape[0]))

    tax_df = pd.read_csv('../data/tax_assessor_denver.csv')
    tax_df = tax_df.loc[tax_df['CompanyFlag'] != 'Y'] #consider dropping this restriction -- use as predictor?

    # matches_df = matches_df.apply(find_matches, axis=1)
    # non_matches = matches_df.loc[matches_df['number_of_matches']==0]
    # single_matches = matches_df.loc[matches_df['number_of_matches']==1]
    # multi_matches = matches_df.loc[matches_df['number_of_matches']>1]
    # single_matches.to_pickle('../data/single_matches.pkl')

    validated_matches = pd.read_pickle('../data/single_matches.pkl')
    validated_matches = process_airbnb(validated_matches)
    merged_data = append_neighbors(validated_matches, tax_df)
    merged_data.to_csv('../data/merged.csv')
