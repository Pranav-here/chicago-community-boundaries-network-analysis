import pandas as pd
import numpy as np
from data_fetch import VARIABLES

def compute_features(df):
    for var in VARIABLES.keys():
        df[var] = pd.to_numeric(df[var], errors='coerce')

    df = df.replace(-666666666, np.nan)
    df = df.replace(-999999999, np.nan)

    df['share_white'] = df['B02001_002E'] / df['B01003_001E']
    df['share_black'] = df['B02001_003E'] / df['B01003_001E']
    df['share_hispanic'] = df['B03003_003E'] / df['B01003_001E']

    ba_plus_cols = ['B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E']
    df['ba_plus_total'] = df[ba_plus_cols].sum(axis=1)
    df['share_ba_plus'] = df['ba_plus_total'] / df['B15003_001E']

    df['renter_share'] = df['B25003_003E'] / df['B25003_001E']
    df['med_income'] = df['B19013_001E']
    df['med_rent'] = df['B25064_001E']
    df['foreign_born_share'] = df['B05002_013E'] / df['B01003_001E']
    df['vacancy_rate'] = df['B25002_003E'] / df['B25002_001E']
    df['homeownership_rate'] = df['B25003_002E'] / df['B25003_001E']
    df['walk_to_work_share'] = df['B08301_019E'] / df['B08301_001E']

    return df

def get_feature_cols():
    return [
        'share_white', 'share_black', 'share_hispanic',
        'share_ba_plus', 'renter_share', 'med_income', 'med_rent',
        'foreign_born_share', 'vacancy_rate', 'homeownership_rate', 'walk_to_work_share'
    ]
