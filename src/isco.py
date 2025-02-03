"""
Clean existing and create additional occupation and education variables based on ISCO-08.

Functions
---------

occupations(piaac_df, log_df)
    Clean ISCO-08 occpuation variables and create custom occupation groups.
    last update: 23/01/2025

education(piaac_df, log_df)
    Clean education variables and convert ISCED to ISCO-08 skill level.
    last update: 23/01/2025
"""

import pandas as pd
import numpy as np
from mismatch_toolbox.src import utilities
from mismatch_toolbox.src import clean

def occupations(piaac_df, log_df):

    """
    Clean ISCO-08 occpuation variables and create custom occupation groups

    Parameters
    ----------
    piaac_df : DataFrame
        PIAAC dataset
    log_df : DataFrame
        log DataFrame

    Returns
    -------
    piaac_df : DataFrame
        PIAAC dataset with cleaned occupation variables and created custom occupation groups
    log_df : DataFrame
        log DataFrame

    Description
    -----------
    1. Convert current job (isco1c, isco2c) and last job (isco1l, isco2l) 1-digit and 2-digit ISCO-08 occupation groups to float
    2. Check and drop missing values for 1-digit and 2-digit occupation groups
    3. Drop observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999)
    4. Create variables isco1c_lbl and isco2c_lbl for isco1c and isco2c labels
    5. Create vartiable isco_lbl for custom occupation groups based on ISCO-08 required skill level
    6. Check and drop missing values for custom occupation
    7. Drop armed orces due to small sample
    8. Create variables cntry_isco_lbl, cntry_isco1c_lbl and cntry_isco2c_lbl for country-specific occupation groups
    9. Drop country-specific occupations groups with n<30
    """

    # converting isco1c, isco2c, isco1l and isco2l to float
    log_record = 'converting isco1c, isco2c, isco1l and isco2l to float'
    log_df = utilities.log(log_df, log_record)
    piaac_df['isco1c'] = pd.to_numeric(piaac_df['isco1c'], errors='coerce')
    piaac_df['isco2c'] = pd.to_numeric(piaac_df['isco2c'], errors='coerce')
    piaac_df['isco1l'] = pd.to_numeric(piaac_df['isco1l'], errors='coerce')
    piaac_df['isco2l'] = pd.to_numeric(piaac_df['isco2l'], errors='coerce')

    # check and drop for 1-digit occupation groups
    log_record = 'check and drop for 1-digit occupation groups'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'isco1c', log_df)

    # check and drop for 2-digit occupation groups
    log_record = 'check and drop for 2-digit occupation groups'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'isco2c', log_df)

    # dropping observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999)
    log_record = 'dropping observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999)'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = clean.drop_val(piaac_df, 'isco1c', [9995, 9996, 9997, 9998, 9999], '==', log_df)

    # creating occupation group label variable for 1-digit groups
    log_record = 'creating occupation group label variable for 1-digit groups'
    log_df = utilities.log(log_df, log_record)
    conditions = [
        (piaac_df['isco1c'] == 1),
        (piaac_df['isco1c'] == 2),
        (piaac_df['isco1c'] == 3),
        (piaac_df['isco1c'] == 4),
        (piaac_df['isco1c'] == 5),
        (piaac_df['isco1c'] == 6),
        (piaac_df['isco1c'] == 7),
        (piaac_df['isco1c'] == 8),
        (piaac_df['isco1c'] == 9),
        (piaac_df['isco1c'] == 0)]
    values = [
        'Managers',
        'Professionals',
        'Technicians and associate professionals',
        'Clerical support workers',
        'Service and sales workers',
        'Skilled agricultural, forestry and fishery workers',
        'Craft and related trades workers',
        'Plant and machine operators, and assemblers',
        'Elementary occupations',
        'Armed forces occupations']
    piaac_df['isco1c_lbl'] = np.select(conditions, values, default='nan')

    # creating occupation group label variable for 2-digit groups
    log_record = 'creating occupation group label variable for 2-digit groups'
    log_df = utilities.log(log_df, log_record)
    conditions = [
        (piaac_df['isco2c'] == 11),
        (piaac_df['isco2c'] == 12),
        (piaac_df['isco2c'] == 13),
        (piaac_df['isco2c'] == 14),
        (piaac_df['isco2c'] == 21),
        (piaac_df['isco2c'] == 22),
        (piaac_df['isco2c'] == 23),
        (piaac_df['isco2c'] == 24),
        (piaac_df['isco2c'] == 25),
        (piaac_df['isco2c'] == 26),
        (piaac_df['isco2c'] == 31),
        (piaac_df['isco2c'] == 32),
        (piaac_df['isco2c'] == 33),
        (piaac_df['isco2c'] == 34),
        (piaac_df['isco2c'] == 35),
        (piaac_df['isco2c'] == 41),
        (piaac_df['isco2c'] == 42),
        (piaac_df['isco2c'] == 43),
        (piaac_df['isco2c'] == 44),
        (piaac_df['isco2c'] == 51),
        (piaac_df['isco2c'] == 52),
        (piaac_df['isco2c'] == 53),
        (piaac_df['isco2c'] == 54),
        (piaac_df['isco2c'] == 61),
        (piaac_df['isco2c'] == 62),
        (piaac_df['isco2c'] == 63),
        (piaac_df['isco2c'] == 71),
        (piaac_df['isco2c'] == 72),
        (piaac_df['isco2c'] == 73),
        (piaac_df['isco2c'] == 74),
        (piaac_df['isco2c'] == 75),
        (piaac_df['isco2c'] == 81),
        (piaac_df['isco2c'] == 82),
        (piaac_df['isco2c'] == 83),
        (piaac_df['isco2c'] == 91),
        (piaac_df['isco2c'] == 92),
        (piaac_df['isco2c'] == 93),
        (piaac_df['isco2c'] == 94),
        (piaac_df['isco2c'] == 95),
        (piaac_df['isco2c'] == 96),
        (piaac_df['isco2c'] == 1),
        (piaac_df['isco2c'] == 2),
        (piaac_df['isco2c'] == 3)]
    values = [
        'Chief executives, senior officials and legislators',
        'Administrative and commercial managers',
        'Production and specialised services managers',
        'Hospitality, retail and other services managers',
        'Science and engineering professionals',
        'Health professionals',
        'Teaching professionals',
        'Business and administration professionals',
        'Information and communications technology professionals',
        'Legal, social and cultural professionals',
        'Science and engineering associate professionals',
        'Health associate professionals',
        'Business and administration associate professionals',
        'Legal, social, cultural and related associate professionals',
        'Information and communications technicians',
        'General and keyboard clerks',
        'Customer services clerks',
        'Numerical and material recording clerks',
        'Other clerical support workers',
        'Personal service workers',
        'Sales workers',
        'Personal care workers',
        'Protective services workers',
        'Market-oriented skilled agricultural workers',
        'Market-oriented skilled forestry, fishery and hunting workers',
        'Subsistence farmers, fishers, hunters and gatherers',
        'Building and related trades workers, excluding electricians',
        'Metal, machinery and related trades workers',
        'Handicraft and printing workers',
        'Electrical and electronic trades workers',
        'Food processing, wood working, garment and other craft and related trades workers',
        'Stationary plant and machine operators',
        'Assemblers',
        'Drivers and mobile plant operators',
        'Cleaners and helpers',
        'Agricultural, forestry and fishery labourers',
        'Labourers in mining, construction, manufacturing and transport',
        'Food preparation assistants',
        'Street and related sales and service workers',
        'Refuse workers and other elementary workers',
        'Commissioned armed forces officers',
        'Non-commissioned armed forces officers',
        'Armed forces occupations, other ranks']
    piaac_df['isco2c_lbl'] = np.select(conditions, values, default='nan')

    # creating major custom occupation groups based on ISCO-08 required skill level
    log_record = 'creating major custom occupation groups based on ISCO-08 required skill level'
    log_df = utilities.log(log_df, log_record)
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
        'High skilled managers',
        'High skilled managers',
        'High skilled managers',
        'Low skilled managers',
        'Professionals',
        'Technicians and associate professionals',
        'Clerical support workers',
        'Service and sales workers',
        'Skilled agricultural, forestry and fishery workers',
        'Craft and related trades workers',
        'Plant and machine operators, and assemblers',
        'Elementary occupations',
        'High skilled armed forces occupations',
        'Medium skilled armed forces occupations',
        'Low skilled armed forces occupations']
    piaac_df['isco_lbl'] = np.select(conditions, values, default='nan')

    # check and drop for custom occupation groups
    log_record = 'check and drop for custom occupation groups'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'isco_lbl', log_df)

    # dropping armed orces due to small sample
    log_record = 'dropping armed orces due to small sample'
    log_df = utilities.log(log_df, log_record)
    piaac_df, log_df = clean.drop_val(piaac_df, 'isco2c', [1, 2, 3], '==', log_df)

    # creating variables for country-specific occupation groups
    log_record = 'creating variables for country-specific occupation groups'
    log_df = utilities.log(log_df, log_record)
    piaac_df['cntry_isco_lbl'] = piaac_df['cntrycode'] + ' ' + piaac_df['isco_lbl']
    piaac_df['cntry_isco1c_lbl'] = piaac_df['cntrycode'] + ' ' + piaac_df['isco1c_lbl']
    piaac_df['cntry_isco2c_lbl'] = piaac_df['cntrycode'] + ' ' + piaac_df['isco2c_lbl']
    
    # dropping country-specific occupations groups with n<30
    log_record = 'dropping occupations groups with n<30'
    log_df = utilities.log(log_df, log_record)
    low_sample_occs = []
    for group in piaac_df['cntry_isco_lbl'].unique():
        if float(piaac_df['cntry_isco_lbl'].value_counts()[group]) < 30:
            low_sample_occs.append(group)
    
    piaac_df, log_df = clean.drop_val(piaac_df, 'cntry_isco_lbl', low_sample_occs, '==', log_df)
        
    
    return piaac_df, log_df


def education(piaac_df, log_df):

    """
    Clean education variables and convert ISCED to ISCO-08 skill level.

    Parameters
    ----------
    piaac_df : DataFrame
        PIAAC dataset
    log_df : DataFrame
        log DataFrame

    Returns
    -------
    piaac_df : DataFrame
        PIAAC dataset with cleaned education variables and created ISCO-08 skill level
    log_df : DataFrame
        log DataFrame

    Description
    -----------
    1. Convert ISCED (b_q01a) to a float
    2. Count missing values in ISCED
    3. Create skill level variable using specified conditions and values lists
    4. Print table of ISCED - ISCO-08 skill level mapping
    5. Converting obtained ISCO-08 skill level (isco08_sl_o) to float
    6. Count missing values in obtained ISCO-08 skill level
    7. Convert year of finish (b_q01c2) to float
    8. Creating a variable for the year when higher education decision was supposedly made
    9. Creating a variable for country specific decision year bins
    """
    
    drop_count_sl = pd.DataFrame(columns=[])

    # convert ISCED (b_q01a) to a float
    log_record = 'converting ISCED level to a float'
    log_df = utilities.log(log_df, log_record)
    piaac_df['b_q01a'] = pd.to_numeric(piaac_df['b_q01a'], errors='coerce')
    
    # count missing values in ISCED
    var = 'b_q01a'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utilities.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utilities.log(log_df, log_record)

    log_record = 'creating a variable for obtained ISCO-08 skill level'
    log_df = utilities.log(log_df, log_record)
    # create a list of conditions for conversion of ISCED into skill level
    conditions = [
        (piaac_df['b_q01a'] == 1),
        (piaac_df['b_q01a'] > 1) & (piaac_df['b_q01a'] < 11),
        (piaac_df['b_q01a'] == 11),
        (piaac_df['b_q01a'] > 11)]
    # create a list of values for skill level
    values = [1,
              2,
              3,
              4]
    # create skill level variable using specified conditions and respective values
    piaac_df['isco08_sl_o'] = np.select(conditions, values, default=float('nan'))

    # print table of ISCED - skill level mapping
    log_record = 'print table of ISCED - skill level mapping'
    log_df = utilities.log(log_df, log_record)
    utilities.print_tab(pd.crosstab(index=piaac_df['b_q01a'], columns=piaac_df['isco08_sl_o'], margins=True))

    # converting isco08_sl_o to float
    log_record = 'converting isco08_sl_o to float'
    log_df = utilities.log(log_df, log_record)
    piaac_df['isco08_sl_o'] = pd.to_numeric(piaac_df['isco08_sl_o'], errors='coerce')
    
    # count missing values in obtained skill level
    var = 'isco08_sl_o'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utilities.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utilities.log(log_df, log_record)

    # convert b_q01c2 (year of finish) to float
    log_record = 'convert b_q01c2 (year of finish) to float'
    log_df = utilities.log(log_df, log_record)
    piaac_df['b_q01c2'] = pd.to_numeric(piaac_df['b_q01c2'], errors='coerce')

    # creating a variable for the year when higher education decision was supposedly made
    log_record = 'creating a variable for the year when higher education decision was supposedly made'
    log_df = utilities.log(log_df, log_record)
    conditions =[
        (piaac_df['b_q01a'] < 11),
        (piaac_df['b_q01a'] >= 11)]
    values = [
        piaac_df['b_q01c2'],
        piaac_df['b_q01c2'] - 3]
    piaac_df['decis_yr'] = np.select(conditions, values, default=float('nan'))

    # creating a variable for country specific decision year bins
    log_record = 'creating a variable for country specific decision year bins'
    log_df = utilities.log(log_df, log_record)
    piaac_df['cntry_yr'] = piaac_df['cntrycode'] + ' ' + piaac_df['decis_yr'].astype(str).str[:4]
    
    return piaac_df, log_df
