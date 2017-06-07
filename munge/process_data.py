#Note: pad latitude by .005, longitude by .0065

import pandas as pd

if __name__ == '__main__':
    matches = pd.read_csv('../data/matches.csv')
    matches = matches.query("score >= 85 & distance <= .5 & room_type == 'Entire home/apt'")
    df_a = pd.read_pickle('../data/airbnb_titles.pkl')
    # positive_class = df_a[df_a['airbnb_property_id'].isin(matches['airbnb_property_id'])]
    matches.sort_values('airbnb_property_id', inplace=True)
    matches.reindex(matches['airbnb_property_id'])
    df_a.sort_values('airbnb_property_id', inplace=True)
    df_a.reindex(df_a['airbnb_property_id'])
    positive_class = pd.concat([df_a, matches], join='inner', axis = 1)
