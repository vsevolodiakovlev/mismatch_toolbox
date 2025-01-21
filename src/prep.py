import pandas as pd
import numpy as np
from src import utility
from src import clean

"""
LAST REVISED: 26.07.23

preparation(piaac_df):
    - convert cntryid to float
    - check and drop for missing values in countries ID
    - create a variable with country names
    - create a variable with country codes
    - identify the respondents who are unemployed or out of the labour force and drop the from the dataset
    - create a variable earn as a float of earnhrbonusppp, drop missing values, and trim at the 1st and 99th percentiles
"""

def preparation(piaac_df, log_df):
    
    # converting cntryid to float
    log_record = 'converting cntryid to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['cntryid'] = pd.to_numeric(piaac_df['cntryid'], errors='coerce')

    # create a variable with country names
    log_record = 'creating [cntryname]: variable for country names'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['cntryid'] == 276),
        (piaac_df['cntryid'] == 643),
        (piaac_df['cntryid'] == 392),
        (piaac_df['cntryid'] == 152),
        (piaac_df['cntryid'] == 702),
        (piaac_df['cntryid'] == 604),
        (piaac_df['cntryid'] == 300),
        (piaac_df['cntryid'] == 233),
        (piaac_df['cntryid'] == 398),
        (piaac_df['cntryid'] == 246),
        (piaac_df['cntryid'] == 724),
        (piaac_df['cntryid'] == 372),
        (piaac_df['cntryid'] == 218),
        (piaac_df['cntryid'] == 528),
        (piaac_df['cntryid'] == 578),
        (piaac_df['cntryid'] == 616),
        (piaac_df['cntryid'] == 250),
        (piaac_df['cntryid'] == 348),
        (piaac_df['cntryid'] == 554),
        (piaac_df['cntryid'] == 376),
        (piaac_df['cntryid'] == 840),
        (piaac_df['cntryid'] == 380),
        (piaac_df['cntryid'] == 410),
        (piaac_df['cntryid'] == 705),
        (piaac_df['cntryid'] == 208),
        (piaac_df['cntryid'] == 56),
        (piaac_df['cntryid'] == 484),
        (piaac_df['cntryid'] == 752),
        (piaac_df['cntryid'] == 703),
        (piaac_df['cntryid'] == 40),
        (piaac_df['cntryid'] == 440),
        (piaac_df['cntryid'] == 203),
        (piaac_df['cntryid'] == 826),
        (piaac_df['cntryid'] == 792),
        (piaac_df['cntryid'] == 124)]
    values = [
        'Germany',
        'Russian Federation',
        'Japan',
        'Chile',
        'Singapore',
        'Peru',
        'Greece',
        'Estonia',
        'Kazakhstan',
        'Finland',
        'Spain',
        'Ireland',
        'Ecuador',
        'Netherlands',
        'Norway',
        'Poland',
        'France',
        'Hungary',
        'New Zealand',
        'Israel',
        'United States',
        'Italy',
        'Korea',
        'Slovenia',
        'Denmark',
        'Belgium',
        'Mexico',
        'Sweden',
        'Slovak Republic',
        'Austria',
        'Lithuania',
        'Czech Republic',
        'United Kingdom',
        'Turkey',
        'Canada']
    piaac_df['cntryname'] = np.select(conditions, values, default=float('nan'))

    # create a variable with country codes
    log_record = 'creating [cntrycode]: variable for country codes'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['cntryid'] == 276),
        (piaac_df['cntryid'] == 643),
        (piaac_df['cntryid'] == 392),
        (piaac_df['cntryid'] == 152),
        (piaac_df['cntryid'] == 702),
        (piaac_df['cntryid'] == 604),
        (piaac_df['cntryid'] == 300),
        (piaac_df['cntryid'] == 233),
        (piaac_df['cntryid'] == 398),
        (piaac_df['cntryid'] == 246),
        (piaac_df['cntryid'] == 724),
        (piaac_df['cntryid'] == 372),
        (piaac_df['cntryid'] == 218),
        (piaac_df['cntryid'] == 528),
        (piaac_df['cntryid'] == 578),
        (piaac_df['cntryid'] == 616),
        (piaac_df['cntryid'] == 250),
        (piaac_df['cntryid'] == 348),
        (piaac_df['cntryid'] == 554),
        (piaac_df['cntryid'] == 376),
        (piaac_df['cntryid'] == 840),
        (piaac_df['cntryid'] == 380),
        (piaac_df['cntryid'] == 410),
        (piaac_df['cntryid'] == 705),
        (piaac_df['cntryid'] == 208),
        (piaac_df['cntryid'] == 56),
        (piaac_df['cntryid'] == 484),
        (piaac_df['cntryid'] == 752),
        (piaac_df['cntryid'] == 703),
        (piaac_df['cntryid'] == 40),
        (piaac_df['cntryid'] == 440),
        (piaac_df['cntryid'] == 203),
        (piaac_df['cntryid'] == 826),
        (piaac_df['cntryid'] == 792),
        (piaac_df['cntryid'] == 124)]
    values = [
        'DEU',
        'RUS',
        'JPN',
        'CHL',
        'SGP',
        'PER',
        'GRC',
        'EST',
        'KAZ',
        'FIN',
        'ESP',
        'IRL',
        'ECU',
        'NLD',
        'NOR',
        'POL',
        'FRA',
        'HUN',
        'NZL',
        'ISR',
        'USA',
        'ITA',
        'KOR',
        'SVN',
        'DNK',
        'BEL',
        'MEX',
        'SWE',
        'SVK',
        'AUT',
        'LTU',
        'CZE',
        'GBR',
        'TUR',
        'CAN']
    piaac_df['cntrycode'] = np.select(conditions, values, default=float('nan'))

    # check and drop for missing values in country ID
    log_record = 'check and drop for missing values in country ID'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'cntryid', log_df)

    # converting c_d05 (employment status) to float
    log_record = 'converting [c_d05] (employment status) to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['c_d05'] = pd.to_numeric(piaac_df['c_d05'], errors='coerce')

    # drop all respondents who are unemployed or out of the labour force
    log_record = 'drop all respondents who are unemployed or out of the labour force'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_val(piaac_df, 'c_d05', [1], '!=', log_df)

    # generate variable earn as a float of an earnings variable of choice
    log_record = 'creating [earn]: variable earn as a float of an earnings variable of choice'
    log_df = utility.log(log_df, log_record)
    piaac_df['earn'] = pd.to_numeric(piaac_df['earnhrbonusppp'], errors='coerce')

    # check and drop for missing values in earnings
    log_record = 'check and drop for missing values in earnings'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'earn', log_df)

    # trim earningns at the 1st and 99th percentiles
    log_record = 'trim earningns at the 1st and 99th percentiles'
    log_df = utility.log(log_df, log_record)
    piaac_df.drop(piaac_df[piaac_df['earn'] < piaac_df['earn'].quantile(0.01)].index, inplace=True)
    piaac_df.drop(piaac_df[piaac_df['earn'] > piaac_df['earn'].quantile(0.99)].index, inplace=True)
    log_record = 'n=' + str(piaac_df.shape[0])
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df
    
    
    