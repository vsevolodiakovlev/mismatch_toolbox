import pandas as pd
import numpy as np
import statistics as st
import math
from src import utility
from src import clean

"""
LAST REVISED: 26.01.23

rm_mean(piaac_df, SDs): 
    - define mean_sl():
        * create variable for occupation specific skill level mean
        * create variable for occupation specific skill level SD
    - calculate country-specific skill level mean and SD using mean_sl() function
    - calculate country-spec mean-based RM mismatch using number of SDs

rm_mode(piaac_df, SDs): 
    - define mode_sl():
        * create variable for occupation specific skill level mode
        * create variable for occupation specific skill level SD
    - calculate country-specific skill level mode and SD using mean_sl() function
    - calculate country-spec mode-based RM mismatch using number of SDs

ja(piaac_df):
    - create variable for required skill using ISCO-08 mapping
    - create variable 'ja' for JA mismatch

isa(piaac_df, gap):
    - convert variable 'yrsget' (self-reported required education) to float
    - convert variable 'yrsqual' (years of education) to float
    - create variable 'isa'_gap for ISA mismatch using specified gap
 
"""


def rm_mean(piaac_df, SDs, log_df):

    def mean_sl(occ_variable, mean_name, std_name):
        conditions = []
        values = []
        # loop across occupation groups
        for group in piaac_df[occ_variable].unique():
            # compute mean skill level for an occupation group
            mean_sl = piaac_df.loc[piaac_df[occ_variable] == group, 'isco08_sl_o'].mean()
            # add the occupation group to the conditions and mean skill level to the values
            conditions.append((piaac_df[occ_variable] == group))
            values.append(mean_sl)
        # create mean_sl variable
        piaac_df[mean_name] = np.select(conditions, values, default=math.nan)

        # repeat for standard deviation
        conditions = []
        values = []
        for group in piaac_df[occ_variable].unique():
            std_sl = piaac_df.loc[piaac_df[occ_variable] == group, 'isco08_sl_o'].std()
            conditions.append((piaac_df[occ_variable] == group))
            values.append(std_sl)
        piaac_df[std_name] = np.select(conditions, values, default=math.nan)

    # calculating country-specific skill level mean and standard deviation
    log_record = 'calculating country-specific skill level mean and standard deviation'
    log_df = utility.log(log_df, log_record)
    mean_sl('cntry_isco_lbl', 'og_mean_sl', 'og_std_sl')

    # creating variable for country-spec mean-based RM mismatch
    log_record = 'creating [rm_mean_' + str(SDs).replace('.', '') +']: variable for country-spec mean-based RM mismatch with ' + str(SDs).replace('.', '') + ' SDs threshold'
    log_df = utility.log(log_df, log_record)
    piaac_df['rm_mean_' + str(SDs).replace('.', '')] = 0
    conditions = [
        piaac_df['isco08_sl_o'] >= piaac_df['og_mean_sl'] + SDs * piaac_df['og_std_sl'],
        ((piaac_df['isco08_sl_o'] < piaac_df['og_mean_sl'] + SDs * piaac_df['og_std_sl']) & 
         (piaac_df['isco08_sl_o'] >= piaac_df['og_mean_sl'] - SDs * piaac_df['og_std_sl'])),
        piaac_df['isco08_sl_o'] < piaac_df['og_mean_sl'] - SDs * piaac_df['og_std_sl']]
    values = [
        1,
        0,
        -1]
    piaac_df['rm_mean_' + str(SDs).replace('.', '')] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in mean-based RM mismatch (don't)
    var = 'rm_mean_' + str(SDs).replace('.', '')
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df


def rm_mode(piaac_df, SDs, log_df):

    # defining function calculating skill level mode and standard deviation
    log_record = 'defining function calculating skill level mode and standard deviation'
    log_df = utility.log(log_df, log_record)
    def mode_sl(occ_variable, mode_name, std_name):
        conditions = []
        values = []
        for group in piaac_df[occ_variable].unique():
            mode_sl = st.mode(piaac_df.loc[piaac_df[occ_variable] == group, 'isco08_sl_o'])
            conditions.append((piaac_df[occ_variable] == group))
            values.append(mode_sl)
        piaac_df[mode_name] = np.select(conditions, values, default=math.nan)

        conditions = []
        values = []
        for group in piaac_df[occ_variable].unique():
            std_sl = piaac_df.loc[piaac_df[occ_variable] == group, 'isco08_sl_o'].std()
            conditions.append((piaac_df[occ_variable] == group))
            values.append(std_sl)
        piaac_df[std_name] = np.select(conditions, values, default=math.nan)

    # calculating country-specific skill level mode and standard deviation
    log_record = 'calculating country-specific skill level mode and standard deviation'
    log_df = utility.log(log_df, log_record)
    mode_sl('cntry_isco_lbl', 'og_mode_sl', 'og_std_sl')

    # creating variable for country-spec mode-based RM mismatch
    log_record = 'creating [rm_mode_' + str(SDs).replace('.', '') + ']: variable for country-spec mode-based RM mismatch with ' + str(SDs).replace('.', '') + ' SDs threshold'
    log_df = utility.log(log_df, log_record)
    piaac_df['rm_mode_' + str(SDs).replace('.', '')] = 0
    conditions = [
        piaac_df['isco08_sl_o'] >= piaac_df['og_mode_sl'] + SDs * piaac_df['og_std_sl'],
        ((piaac_df['isco08_sl_o'] < piaac_df['og_mode_sl'] + SDs * piaac_df['og_std_sl']) & 
         (piaac_df['isco08_sl_o'] >= piaac_df['og_mode_sl'] - SDs * piaac_df['og_std_sl'])),
        piaac_df['isco08_sl_o'] < piaac_df['og_mode_sl'] - SDs * piaac_df['og_std_sl']]
    values = [
        1,
        0,
        -1]
    piaac_df['rm_mode_' + str(SDs).replace('.', '')] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in mode-based RM mismatch (don't)
    var = 'rm_mode_' + str(SDs).replace('.', '')
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df

def ja(piaac_df, log_df):

    # creating variable for required skill level
    log_record = 'creating [isco08_sl_r]: variable for required skill level'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['isco2c'] == 11),
        (piaac_df['isco2c'] == 12),
        (piaac_df['isco2c'] == 13),
        (piaac_df['isco2c'] == 14),
        (piaac_df['isco1c'] == 2),
        (piaac_df['isco1c'] == 3),
        (piaac_df['isco1c'] == 4),
        (piaac_df['isco1c'] == 5),
        (piaac_df['isco1c'] == 6),
        (piaac_df['isco1c'] == 7),
        (piaac_df['isco1c'] == 8),
        (piaac_df['isco1c'] == 9),
        (piaac_df['isco2c'] == 1),
        (piaac_df['isco2c'] == 2),
        (piaac_df['isco2c'] == 3)]
    values = [
        4,
        4,
        4,
        3,
        4,
        3,
        2,
        2,
        2,
        2,
        2,
        1,
        3,
        2,
        1]
    piaac_df['isco08_sl_r'] = np.select(conditions, values, default=math.nan)

    # creating variable for JA mismatch
    log_record = 'creating [ja]: variable for JA mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        piaac_df['isco08_sl_o'] > piaac_df['isco08_sl_r'],
        piaac_df['isco08_sl_o'] == piaac_df['isco08_sl_r'],
        piaac_df['isco08_sl_o'] < piaac_df['isco08_sl_r']]
    values = [
        1,
        0,
        -1]
    piaac_df['ja'] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in JA mismatch (don't)
    var = 'ja'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df


def isa(piaac_df, gap, log_df):
    # converting self-reported requirement to float
    log_record = 'converting self-reported requirement to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['yrsget'] = pd.to_numeric(piaac_df['yrsget'], errors='coerce')

    # converting years of education to float
    log_record = 'converting years of education to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['yrsqual'] = pd.to_numeric(piaac_df['yrsqual'], errors='coerce')

    piaac_df['isa_mismatch'] = piaac_df['yrsqual'] - piaac_df['yrsget']

    # creating variable for ISA mismatch
    log_record = 'creating [isa_' + str(gap).replace('.', '') +']: variable for ISA mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [(piaac_df['isa_mismatch'] >= gap),
                  ((piaac_df['isa_mismatch'] < gap) & (piaac_df['isa_mismatch'] >= gap * (-1))),
                  (piaac_df['isa_mismatch'] < gap * (-1))]
    values = [1,
              0,
              -1]
    piaac_df['isa_' + str(gap).replace('.', '')] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in ISA mismatch (don't)
    var = 'isa_' + str(gap).replace('.', '')
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df

