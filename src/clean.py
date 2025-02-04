"""
A set of functions for data cleaning.

Functions:
----------

drop_nan(df, var, log_df)
    Drop observations containing missing values for a given variable.
    last update: 22/01/2025

drop_val(df, var, values_list, operator, log_df)
    Drop observations with specific values for a given variable.
    last update: 22/01/2025

preparation(piaac_df, log_df)
    Prepare the dataset for analysis.
    last update: 23/01/2025
"""

from mismatch_toolbox.src import utilities
import pandas as pd
import numpy as np

def drop_nan(df, var, log_df):
    
    """
    Drop observations containing missing values for a given variable.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame, dataset.
    var : str, variable name.
    log_df : pandas.core.frame.DataFrame, log file.
    
    Returns
    -------
    df : pandas.core.frame.DataFrame, updated dataset. 
    log_df : pandas.core.frame.DataFrame, updated log file.

    Description
    -----------
    1. identify whether the variable is string or numeric;
    2. if string: identify observations containing 'nan';
    3. if nueric: identify observations containing missing values;
    4. drop observation containing either missing values or 'nan';
    5. repeat the missing values check;
    6. register the changes in [log_df].    
    """

    if (df[var].dtypes == 'O') == True:
        nan = 'nan'
        if (nan in df[var].unique()) == True:
            log_record = (str(df[var].value_counts()[nan]) + ' observations have the value of nan for [' + var + ']')
            log_df = utilities.log(log_df, log_record)
            n_before = df.shape[0]
            cntries_before = df['cntryname'].value_counts()
            cntries_before = cntries_before.rename(var + ': orig')
            log_record = ('n=' + str(n_before))
            log_df = utilities.log(log_df, log_record)
            log_record = ('removing the observations...')
            log_df = utilities.log(log_df, log_record)
            df.drop(df[df[var] == nan].index, inplace=True)
            if (nan in df[var].unique()) == True:
                log_record = ('It did not work, ' + str(
                    df[var].value_counts()[nan]) + ' observations still have the value of nan for [' + var + ']')
                log_df = utilities.log(log_df, log_record)
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                log_df = utilities.log(log_df, log_record)
                cntries_after = df['cntryname'].value_counts()
                cntries_after = cntries_after.rename(var + ': clnd')
                cntries_diff = cntries_before - cntries_after
                cntries_diff = cntries_diff.rename(var + ': diff')
            else:
                log_record = ('no observations have the value of nan for [' + var + ']')
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                cntries_after = df['cntryname'].value_counts()
                cntries_after = cntries_after.rename(var + ': clnd')
                cntries_diff = cntries_before - cntries_after
                cntries_diff = cntries_diff.rename(var + ': diff')
        else:
            log_record = ('no observations have the value of nan for [' + var + ']')
            log_df = utilities.log(log_df, log_record)
            log_record = ('n=' + str(df.shape[0]))
            log_df = utilities.log(log_df, log_record)
    else:
        if (df[var].isnull().values.any()) == True:
            log_record = (str(df[var].isnull().value_counts()[True]) + ' observations have the value of nan for [' + var + ']')
            log_df = utilities.log(log_df, log_record)
            n_before = df.shape[0]
            cntries_before = df['cntryname'].value_counts()
            cntries_before = cntries_before.rename(var + ': orig')
            log_record = ('n=' + str(n_before))
            log_df = utilities.log(log_df, log_record)
            log_record = ('removing the observations...')
            log_df = utilities.log(log_df, log_record)
            df.dropna(subset=var, inplace=True)
            if (df[var].isnull().values.any()) == True:
                log_record = ('It did not work, ' + str(df[var].isnull().value_counts()[
                                                    True]) + ' observations still have the value of nan for [' + var + ']')
                log_df = utilities.log(log_df, log_record)
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                log_df = utilities.log(log_df, log_record)
                cntries_after = df['cntryname'].value_counts()
                cntries_after = cntries_after.rename(var + ': clnd')
                cntries_diff = cntries_before - cntries_after
                cntries_diff = cntries_diff.rename(var + ': diff')
            else:
                log_record = ('no observations have the value of nan for [' + var + ']')
                log_df = utilities.log(log_df, log_record)
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                log_df = utilities.log(log_df, log_record)
                cntries_after = df['cntryname'].value_counts()
                cntries_after = cntries_after.rename(var + ': clnd')
                cntries_diff = cntries_before - cntries_after
                cntries_diff = cntries_diff.rename(var + ': diff')
        else:
            log_record = ('no observations have the value of nan for [' + var + ']')
            log_df = utilities.log(log_df, log_record)
            log_record = ('n=' + str(df.shape[0]))
            log_df = utilities.log(log_df, log_record)
    return df, log_df

def drop_val(df, var, values_list, operator, log_df):
    
    """
    Drop observations with specific values for a given variable.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame, dataset.
    var : str, variable name.
    values_list : list, values to be either dropped or kept
    operator : either "==" or "!="
    log_df : pandas.core.frame.DataFrame, log file.

    Returns
    -------
    df : pandas.core.frame.DataFrame, updated dataset.
    log_df : pandas.core.frame.DataFrame, updated log file.
    
    Description
    -----------
    for each value in [values_list]:  
        1. drop observations that satisfy the following expression: "observation [operator] [value]";
        2. register the changes in [log_df].

    """
    
    n_before = df.shape[0]
    log_record = ('n=' + str(n_before))
    log_df = utilities.log(log_df, log_record)
    log_record = ('dropping observations with ' + '[' +var + ']' + operator + str(values_list))
    log_df = utilities.log(log_df, log_record)
    for value in values_list:
        if operator == '==':
            df.drop(df[df[var] == value].index, inplace=True)
        elif operator == '!=':
            df.drop(df[df[var] != value].index, inplace=True)
    n_after = df.shape[0]
    log_record = 'n=' + str(n_after) + '; ' + str(n_before - n_after) + ' observations have been removed'
    log_df = utilities.log(log_df, log_record)
    
    return df, log_df


def preparation(piaac_df, log_df):

    """
    Prepare the dataset for analysis.

    Parameters
    ----------
    piaac_df : pandas.core.frame.DataFrame, dataset.
    log_df : pandas.core.frame.DataFrame, log file.

    Returns
    -------
    piaac_df : pandas.core.frame.DataFrame, updated dataset.
    log_df : pandas.core.frame.DataFrame, updated log file.

    Description
    -----------
    1. convert cntryid to float;
    2. create a variable with country names;
    3. create a variable with country codes;
    4. check and drop for missing values in country ID;
    5. identify the respondents who are unemployed or out of the labour force and drop the from the dataset;
    6. create a variable earn as a float of earnhrbonusppp, drop missing values, and trim at the 1st and 99th percentiles;
    7. register the changes in [log_df].
    """
    
    # converting cntryid to float
    log_record = 'converting cntryid to float'
    log_df = utilities.log(log_df, log_record)
    piaac_df['cntryid'] = pd.to_numeric(piaac_df['cntryid'], errors='coerce')

    # create a variable with country names
    log_record = 'creating [cntryname]: variable for country names'
    log_df = utilities.log(log_df, log_record)
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
    piaac_df['cntryname'] = np.select(conditions, values, default='nan')

    # create a variable with country codes
    log_record = 'creating [cntrycode]: variable for country codes'
    log_df = utilities.log(log_df, log_record)
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
    piaac_df['cntrycode'] = np.select(conditions, values, default='nan')

    # check and drop for missing values in country ID
    log_record = 'check and drop for missing values in country ID'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = drop_nan(piaac_df, 'cntryid', log_df)

    # converting c_d05 (employment status) to float
    log_record = 'converting [c_d05] (employment status) to float'
    log_df = utilities.log(log_df, log_record)
    piaac_df['c_d05'] = pd.to_numeric(piaac_df['c_d05'], errors='coerce')

    # drop all respondents who are unemployed or out of the labour force
    log_record = 'drop all respondents who are unemployed or out of the labour force'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = drop_val(piaac_df, 'c_d05', [1], '!=', log_df)

    # generate variable earn as a float of an earnings variable of choice
    log_record = 'creating [earn]: variable earn as a float of an earnings variable of choice'
    log_df = utilities.log(log_df, log_record)
    piaac_df['earn'] = pd.to_numeric(piaac_df['earnhrbonusppp'], errors='coerce')

    # check and drop for missing values in earnings
    log_record = 'check and drop for missing values in earnings'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = drop_nan(piaac_df, 'earn', log_df)

    # trim earningns at the 1st and 99th percentiles
    log_record = 'trim earningns at the 1st and 99th percentiles'
    log_df = utilities.log(log_df, log_record)
    piaac_df.drop(piaac_df[piaac_df['earn'] < piaac_df['earn'].quantile(0.01)].index, inplace=True)
    piaac_df.drop(piaac_df[piaac_df['earn'] > piaac_df['earn'].quantile(0.99)].index, inplace=True)
    log_record = 'n=' + str(piaac_df.shape[0])
    log_df = utilities.log(log_df, log_record)
    
    return piaac_df, log_df
            