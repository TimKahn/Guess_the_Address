import pandas as pd
import geopy.distance
import re
from whoswho import who
from fuzzywuzzy import fuzz

'''FEATURES:
zipcode
neighbor_count: Number of 'neighbors' in radius
lat_offset: Difference in latitude (AirBNB minus Tax Assessor)
lon_offset: Difference in longitude (AirBNB minus Tax Assessor)

fireplace_a: boolean -- airbnb indoor_fireplace == True
fireplace_t: boolean -- tax assessor Fireplace code == 1.0
pool_a: boolean -- swimming pool in airbnb listing
pool_t: boolean -- swimming pool in tax assessor data

Bedrooms on AirBNB listing
Bedrooms on AirBNB listing - Bedrooms in Assessor Data
Bathrooms on AirBNB listing
Bathrooms on AirBNB listing - Bathrooms in Assessor Data
Similarity scores of AirBNB Host Name(s) and First Name on Deed etc. (each score is a different predictor?)

CANDIDATES DROPPED:
accomodates -- all NaN
AreaBuilding -- not useful without accomodates
pets_a, elevator_a, gym_a: all boolean, from airbnb listing
unit_number_t
Air Conditioning -- not included; mostly NaN in attom, mostly True in airbnb
Heating -- not included; assume the False listings in airbnb probably still have heating (it's Denver).
Pool (tax assessor) -- 5 matches had pools per airbnb; none showed a pool in tax assessor data.
'''

def get_name_set(df_row):
    '''
    Use regex to pull first name from all tax assessor 'owner' columns.  Combine all in a set.
    '''
    cols = ['PartyOwner1NameFull', 'PartyOwner2NameFull']
    name_set = set('')
    for col in cols:
        name_set.update(re.findall('(?<=,)\w+|(?<=&\W)\w+', df_row[col]))
    return name_set

def check_names(df_row):
    '''
    Check for set membership, set score to 100 if found.
    Else get best whoswho score from comparing all names.
    '''
    name_set = get_name_set(df_row)
    name1, name2 = df_row['first_name'], df_row['first_name2']
    print(name_set)
    if (name1 or name2) in name_set:
        df_row['name_score'] = 100.0
    else:
        scores = [who.ratio(x,y) for x in (name1, name2) for y in name_set]
        if len(scores) > 0 and max(scores) >= 25:
            df_row['name_score'] = max(scores)
        else:
            df_row['name_score'] = 0
    print(name1, name2, df_row['name_score'])

def clean_up_names(df):
    df[['PartyOwner1NameFull', 'PartyOwner2NameFull']] = df[['PartyOwner1NameFull', 'PartyOwner2NameFull']].fillna('')
    df['first_name'] = df['first_name'].fillna('')
    df['first_name'] = df['first_name'].apply(lambda x: str(x).upper())
    df['first_name2'] = df['first_name2'].fillna('')
    df['first_name2'] = df['first_name2'].apply(lambda x: str(x).upper())
    return df

def get_features(df):
    featurized_df = pd.DataFrame([])
    featurized_df['MATCH'] = df.loc[:, 'MATCH'].apply(lambda x: 1 if x == True else 0) #whether this a confirmed address match.  This will be y.
    featurized_df['attom_id'] = df.loc[:, '[ATTOM ID]']
    featurized_df['airbnb_property_id'] = df.loc[:, 'airbnb_property_id']
    featurized_df['airbnb_host_id'] = df.loc[:, 'airbnb_host_id']
    featurized_df['first_name'] = df.loc[:, 'first_name']
    featurized_df['first_name2'] = df.loc[:, 'first_name2']
    #predictors start here...
    featurized_df['zipcode'] = df.loc[:, 'zipcode']
    featurized_df['neighbor_count'] = df.loc[:, 'neighbor_count']
    featurized_df['lat_offset'] = df.loc[:, 'latitude'] - df.loc[:, 'PropertyLatitude']
    featurized_df['lon_offset'] = df.loc[:, 'longitude'] - df.loc[:, 'PropertyLongitude']
    featurized_df['fireplace_a'] = df['indoor_fireplace'].apply(lambda x: 1 if x == True else 0)
    featurized_df['fireplace_t'] = df['Fireplace'].apply(lambda x: 1 if x == 1.0 else 0)
    featurized_df['beds_a'] = df.loc[:, 'bedrooms']
    featurized_df['baths_a'] = df.loc[:, 'bathrooms']
    featurized_df['bed_diff'] = df.loc[:, 'bedrooms'] - df.loc[:, 'BedroomsCount']
    featurized_df['bath_diff'] = df.loc[:, 'bathrooms'] - df.loc[:, 'BathCount']
    m = df.query('MATCH == 1')
    m = m.apply(check_names, axis=1)
    return featurized_df

if __name__ == '__main__':
    df = pd.read_csv('../data/merged.csv')
    df = clean_up_names(df)
    featurized_df = get_features(df)
