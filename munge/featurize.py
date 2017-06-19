import pandas as pd

'''FEATURES:
zipcode
neighbor_count: Number of 'neighbors' in radius
lat_offset: Difference in latitude (AirBNB minus Tax Assessor)
lon_offset: Difference in longitude (AirBNB minus Tax Assessor)
fireplace_a: boolean -- airbnb indoor_fireplace == True
fireplace_t: boolean -- tax assessor Fireplace code == 1.0
beds_a: Bedrooms on AirBNB listing
bed_diff: Bedrooms on AirBNB listing minus Bedrooms in Assessor Data
baths_a: Bathrooms on AirBNB listing
bath_diff: Bathrooms on AirBNB listing minus Bathrooms in Assessor Data
name_score: Max similarity scores of AirBNB Host Name(s) and PartyOwner 1 and 2.

CANDIDATES DROPPED:
pool_a: boolean -- swimming pool in airbnb listing
pool_t: boolean -- swimming pool in tax assessor data
AreaBuilding: not useful without 'accomodates' data
pets_a, elevator_a, gym_a: all boolean, from airbnb listing.  Could indicated whether property is a unit in apt/condo.
unit_number_t: boolean -- 1 if tax assessor data shows a unit number.  Too few in training data to be a viable predictor.
Air Conditioning -- not included; mostly NaN in attom, mostly True in airbnb
Heating -- not included; assume the False listings in airbnb probably still have heating (it's Denver).
Pool (tax assessor) -- 5 matches had pools in airbnb data; none of these five showed a pool in tax assessor data.
'''

def get_features(df):
    featurized_df = pd.DataFrame([])
    featurized_df['MATCH'] = df.loc[:, 'MATCH'].apply(lambda x: 1 if x == True else 0) #whether this a confirmed address match.  This will be y.
    featurized_df['attom_id'] = df.loc[:, '[ATTOM ID]']
    featurized_df['airbnb_property_id'] = df.loc[:, 'airbnb_property_id']
    featurized_df['airbnb_host_id'] = df.loc[:, 'airbnb_host_id']
    featurized_df['first_name'] = df.loc[:, 'first_name']
    featurized_df['first_name2'] = df.loc[:, 'first_name2']
    featurized_df['title'] = df.loc[:, 'title'].astype(str).fillna('')
    #predictors start here...
    # featurized_df['zipcode'] = df.loc[:, 'zipcode'].fillna(0).apply(lambda x: int(x))
    # featurized_df = pd.concat([featurized_df, pd.get_dummies(featurized_df['zipcode'])], axis=1)
    # featurized_df = featurized_df.drop('zipcode', 1)
    featurized_df['neighbor_count'] = df.loc[:, 'neighbor_count']
    featurized_df['lat_offset'] = df.loc[:, 'latitude'] - df.loc[:, 'PropertyLatitude']
    featurized_df['lon_offset'] = df.loc[:, 'longitude'] - df.loc[:, 'PropertyLongitude']
    featurized_df['fireplace_a'] = df['indoor_fireplace'].apply(lambda x: 1 if x == True else 0)
    featurized_df['fireplace_t'] = df['Fireplace'].apply(lambda x: 1 if x == 1.0 else 0)
    featurized_df['beds_a'] = df.loc[:, 'bedrooms'].fillna(0)
    featurized_df['bed_diff'] = df.loc[:, 'bedrooms'] - df.loc[:, 'BedroomsCount'].fillna(0).apply(lambda x: max(x, 10))
    featurized_df['baths_a'] = df.loc[:, 'bathrooms'].fillna(0)
    featurized_df['bath_diff'] = df.loc[:, 'bathrooms'] - df.loc[:, 'BathCount'].fillna(0)
    # featurized_df['square_feet'] = df.loc[:, 'AreaBuilding'].fillna(0)
    # featurized_df['accommodates'] = df.loc[:, 'accommodates'].astype(int).fillna(0)
    featurized_df['name_score'] = df.loc[:, 'name_score']
    return featurized_df

if __name__ == '__main__':
    df = pd.read_csv('../data/merged.csv', low_memory=False)
    featurized_df = get_features(df)
    featurized_df.to_csv('../data/featurized_data.csv')
