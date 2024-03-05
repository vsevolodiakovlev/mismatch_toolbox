import pandas as pd
import numpy as np
# noinspection PyUnresolvedReferences
from labour_mismatch.src import utility
from labour_mismatch.src import clean

"""
version: 27.07.23

occupations(piaac_df):
    - convert current job (isco1c, isco2c) and last job (isco1l, isco2l) 1-digit and 2-digit ISCO-08 occupation groups to float
    - check and drop missing values for 1-digit and 2-digit occupation groups
    - drop observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999) 
    - create variables isco1c_lbl and isco2c_lbl for isco1c and isco2c labels
    - create vartiable isco_lbl for custom occupation groups based on ISCO-08 required skill level
    - check and drop missing values for custom occupation groups
    - drop armed orces due to small sample
    - create variables cntry_isco_lbl, cntry_isco1c_lbl and cntry_isco2c_lbl for country-specific occupation groups

"""

def occupations(piaac_df, log_df):

    # converting isco1c, isco2c, isco1l and isco2l to float
    log_record = 'converting isco1c, isco2c, isco1l and isco2l to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['isco1c'] = pd.to_numeric(piaac_df['isco1c'], errors='coerce')
    piaac_df['isco2c'] = pd.to_numeric(piaac_df['isco2c'], errors='coerce')
    piaac_df['isco1l'] = pd.to_numeric(piaac_df['isco1l'], errors='coerce')
    piaac_df['isco2l'] = pd.to_numeric(piaac_df['isco2l'], errors='coerce')

    # check and drop for 1-digit occupation groups
    log_record = 'check and drop for 1-digit occupation groups'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'isco1c', log_df)

    # check and drop for 2-digit occupation groups
    log_record = 'check and drop for 2-digit occupation groups'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'isco2c', log_df)

    # dropping observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999)
    log_record = 'dropping observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999)'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_val(piaac_df, 'isco1c', [9995, 9996, 9997, 9998, 9999], '==', log_df)

    # creating occupation group label variable for 1-digit groups
    log_record = 'creating occupation group label variable for 1-digit groups'
    log_df = utility.log(log_df, log_record)
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
    piaac_df['isco1c_lbl'] = np.select(conditions, values, default=float('nan'))

    # creating occupation group label variable for 2-digit groups
    log_record = 'creating occupation group label variable for 2-digit groups'
    log_df = utility.log(log_df, log_record)
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
    piaac_df['isco2c_lbl'] = np.select(conditions, values, default=float('nan'))

    # creating major custom occupation groups based on ISCO-08 required skill level
    log_record = 'creating major custom occupation groups based on ISCO-08 required skill level'
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
    piaac_df['isco_lbl'] = np.select(conditions, values, default=float('nan'))

    # check and drop for custom occupation groups
    log_record = 'check and drop for custom occupation groups'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'isco_lbl', log_df)

    # dropping armed orces due to small sample
    log_record = 'dropping armed orces due to small sample'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_val(piaac_df, 'isco2c', [1, 2, 3], '==', log_df)

    # creating variables for country-specific occupation groups
    log_record = 'creating variables for country-specific occupation groups'
    log_df = utility.log(log_df, log_record)
    piaac_df['cntry_isco_lbl'] = piaac_df['cntrycode'] + ' ' + piaac_df['isco_lbl']
    piaac_df['cntry_isco1c_lbl'] = piaac_df['cntrycode'] + ' ' + piaac_df['isco1c_lbl']
    piaac_df['cntry_isco2c_lbl'] = piaac_df['cntrycode'] + ' ' + piaac_df['isco2c_lbl']
    
    # dropping country-specific occupations groups with n<30
    log_record = 'dropping occupations groups with n<30'
    log_df = utility.log(log_df, log_record)
    low_sample_occs = []
    for group in piaac_df['cntry_isco_lbl'].unique():
        if float(piaac_df['cntry_isco_lbl'].value_counts()[group]) < 30:
            low_sample_occs.append(group)
    
    piaac_df, log_df = clean.drop_val(piaac_df, 'cntry_isco_lbl', low_sample_occs, '==', log_df)
        
    
    return piaac_df, log_df
