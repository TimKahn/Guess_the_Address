#Note: pad latitude by .005, longitude by .0065

import pandas as pd

if __name__ == '__main__':
    matches = pd.read_csv('../data/matches.csv')
    matches = matches.query("score >= 85 & distance <= .5 & room_type == 'Entire home/apt'")
