import pandas as pd
import tabulate as tab
import numpy as np
import math
from sklearn.metrics import matthews_corrcoef

"""
version: 27.07.23

FUNCTIONS
    - section(new_section, log_df)
    - log(log_df, record)
    - print_tab(df)
    - mismatch_shares(piaac_df, mismatch_variable, feature):
        - generate empty conditions and values lists
        - for each unique value of a specified feature,
            * generate normilized value counts series for a specified mismatch variable
            * identify a row corresponding to the mismatch value of 0 (well-matched) in the index
            * append the corresponding value (share) from column 1 of the series to the list of values
            * if desired row is not identified, append 0
            * append the value of the feature to the conditions list
        - using the conditions and values lists, generate variable for the sares of well-matched workers
        - repeat the above for under-matched and over-matched workers
"""


def section(new_section, log_df):

    """
    Parameters
    ----------
    new_section : str, contains new sectio title.
    log_df : pandas.core.frame.DataFrame, log dataframe with 3 columns ('index', 'section', 'record').
    
    Returns
    -------
    log_df : pandas.core.frame.DataFrame, updated log dataframe
    
    Description
    -----------
    1. print the [new_section];
    2. append a record to [log_df] containing [new_section]
    (new log records will be entered under [new_section] until renewed);
    3. return updated [log_df]
    """
    
    if log_df.size > 0:
        log_index = log_df.iloc[-1,0] + 1
    else: 
        log_index = 0
    
    new_section_record = pd.DataFrame([[log_index, new_section, "new section started"]], columns=['index', 'section', 'record'])
    log_df = pd.concat(objs=[log_df, new_section_record], axis=0, ignore_index=True)
    print()
    print(new_section)
    print('---------------------------------------------')
    print()
    return log_df


def log(log_df, record):

    """
    Parameters
    ----------
    log_df : pandas.core.frame.DataFrame, log dataframe with 3 columns ('index', 'section', 'record').
    record : str, contains new log record.
    
    Returns
    -------
    log_df : pandas.core.frame.DataFrame, updated log dataframe.
    
    Description
    -----------
    1. print [record];
    2. append [record] to [log_df];
    3. return updated [log_df].
    """
    
    if log_df.size > 0:
        log_index = log_df.iloc[-1,0] + 1
        section_title = log_df.iloc[-1,1]
    else: 
        log_index = 0
        section_title = "no section has been started"
        
    new_rec = pd.DataFrame([[log_index, section_title, record]], columns=['index', 'section', 'record'])
    log_df = pd.concat(objs=[log_df, new_rec], axis=0, ignore_index=True)
    message = 'log[' + str(log_index) + '] ' + str(record)
    print(message)
    return log_df


def print_tab(df):
    """
    Parameters
    ----------
    df : pandas.core.frame.DataFrame, any dataframe.
    
    Returns
    -------
    None.

    Description
    -----------
    1. use tabulate package to print [df] with the following settings:
        headers='keys',
        tablefmt='psql'.

    """
    print()
    print(tab.tabulate(df, headers='keys', tablefmt='psql'))


def mismatch_shares(piaac_df, mismatch_variable, feature, log_df):
    
    """
    Parameters
    ----------
    piaac_df : pandas.core.frame.DataFrame, piaac dataset.
    mismatch_variable : str, mismatch variable name.
    feature: : str, group variable.
    log_df : pandas.core.frame.DataFrame, log file.

    Returns
    -------
    df : pandas.core.frame.DataFrame, piaac dataset with mismatch shares added.
    log_df : pandas.core.frame.DataFrame, updated log file.
    
    Description
    -----------
    1. compute relative frequencies of each mismatch value (shares) within each group;
    2. create respective mismatch share variables;
    3. register the changes in [log_df].
    """
    
    log_record = ('creating mismatch shares for [' + mismatch_variable + '] across [' + feature + ']')
    log_df = log(log_df, log_record)
    
    conditions = []
    values = []
    for value in piaac_df[feature].unique():
        mismatch_shares = piaac_df.loc[piaac_df[feature] == value, mismatch_variable].value_counts(normalize=True)
        if (0 in mismatch_shares.index) == True:
            values.append(mismatch_shares[0])
        else:
            values.append(0)
        conditions.append(piaac_df[feature] == value)
    piaac_df[mismatch_variable + '_wellshare_by_' + feature] = np.select(conditions, values, default=math.nan)
    
    log_record = ('[' + mismatch_variable + '_wellshare_by_' + feature + '] created')
    log_df = log(log_df, log_record)
    
    conditions = []
    values = []
    for value in piaac_df[feature].unique():
        mismatch_shares = piaac_df.loc[piaac_df[feature] == value, mismatch_variable].value_counts(normalize=True)
        if (1 in mismatch_shares.index) == True:
            values.append(mismatch_shares[1])
        else:
            values.append(0)
        conditions.append(piaac_df[feature] == value)
    piaac_df[mismatch_variable + '_overshare_by_' + feature] = np.select(conditions, values, default=math.nan)

    log_record = ('[' + mismatch_variable + '_overshare_by_' + feature + '] created')
    log_df = log(log_df, log_record)

    conditions = []
    values = []
    for value in piaac_df[feature].unique():
        mismatch_shares = piaac_df.loc[piaac_df[feature] == value, mismatch_variable].value_counts(normalize=True)
        if (-1 in mismatch_shares.index) == True:
            values.append(mismatch_shares[-1])
        else:
            values.append(0)
        conditions.append(piaac_df[feature] == value)
    piaac_df[mismatch_variable + '_undershare_by_' + feature] = np.select(conditions, values, default=math.nan)

    log_record = ('[' + mismatch_variable + '_undershare_by_' + feature + '] created')
    log_df = log(log_df, log_record)
    
    if mismatch_variable == 'dsa':
        conditions = []
        values = []
        for value in piaac_df[feature].unique():
            mismatch_shares = piaac_df.loc[piaac_df[feature] == value, mismatch_variable].value_counts(normalize=True)
            if (9999 in mismatch_shares.index) == True:
                values.append(mismatch_shares[9999])
            else:
                values.append(0)
            conditions.append(piaac_df[feature] == value)
        piaac_df[mismatch_variable + '_errorshare_by_' + feature] = np.select(conditions, values, default=math.nan)
        
        log_record = ('[' + mismatch_variable + '_errorshare_by_' + feature + '] created')
        log_df = log(log_df, log_record)
    
    return piaac_df, log_df


def mcc_matrix(df, feature_list):
    mcc_matrix = pd.DataFrame(index = feature_list,
                              columns = feature_list)
    for measure_row in feature_list:
        for measure_col in feature_list:
            true_cleaned = df.loc[(df[measure_row].isnull()==False)*(df[measure_col].isnull()==False), measure_row]
            pred_cleaned = df.loc[(df[measure_row].isnull()==False)*(df[measure_col].isnull()==False), measure_col]
            mcc = matthews_corrcoef(true_cleaned, pred_cleaned)
            mcc_matrix.loc[measure_row, measure_col] = mcc
    
    mcc_matrix = mcc_matrix.astype(float)
            
    return mcc_matrix
            

def mismatch_split(piaac_df, measure_list, log_df):
    for measure in measure_list:
        
        log_record = ('splitting [' + measure + '] into 3 binary variables')
        log_df = log(log_df, log_record)
        conditions = []
        
        values =[]
        conditions = [piaac_df[measure] == -1,
                      piaac_df[measure] == 0,
                      piaac_df[measure] == 1,
                      piaac_df[measure] == 9999]
        values = [1, 0, 0, 0]
        piaac_df[measure + "_u"] = np.select(conditions, values, default=math.nan)
        log_record = ('[' + measure + "_u" + '] created')
        log_df = log(log_df, log_record)
        
        values = [0, 1, 0, 0]
        piaac_df[measure + "_w"] = np.select(conditions, values, default=math.nan)
        log_record = ('[' + measure + "_w" + '] created')
        log_df = log(log_df, log_record)
        
        values = [0, 0, 1, 0]
        piaac_df[measure + "_o"] = np.select(conditions, values, default=math.nan)
        log_record = ('[' + measure + "_o" + '] created')
        log_df = log(log_df, log_record)
        
    return piaac_df, log_df


