import pandas as pd
import numpy as np
from labour_mismatch.src import clean
from labour_mismatch.src import utility

"""
LAST REVISED: 26.01.23

isco08_sl(piaac_df):
    - convert b_q01a (ISCED) to a float
    - check and drop for missing values in ISCED
    - create skill level variable using specified conditions and values lists
    - print table of ISCED - ISCO-08 skill level mapping
    - converting obtained ISCO-08 skill level (isco08_sl_o) to float
    - check and drop for missing values in obtained ISCO-08 skill level
    - convert year of finish (b_q01c2) to float
    - creating a variable for the year when higher education decision was made
    - creating a variable for country specific decision year bins
"""

def isco08_sl(piaac_df, log_df):
    
    drop_count_sl = pd.DataFrame(columns=[])

    # convert ISCED (b_q01a) to a float
    log_record = 'converting ISCED level to a float'
    log_df = utility.log(log_df, log_record)
    piaac_df['b_q01a'] = pd.to_numeric(piaac_df['b_q01a'], errors='coerce')
    
    # check and drop for missing values in ISCED (don't)
    var = 'b_q01a'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)

    log_record = 'creating a variable for obtained ISCO-08 skill level'
    log_df = utility.log(log_df, log_record)
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
    log_df = utility.log(log_df, log_record)
    utility.print_tab(pd.crosstab(index=piaac_df['b_q01a'], columns=piaac_df['isco08_sl_o'], margins=True))

    # converting isco08_sl_o to float
    log_record = 'converting isco08_sl_o to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['isco08_sl_o'] = pd.to_numeric(piaac_df['isco08_sl_o'], errors='coerce')
    
    # check and drop for missing values in obtained skill level (don't)
    var = 'isco08_sl_o'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)

    # convert b_q01c2 (year of finish) to float
    log_record = 'convert b_q01c2 (year of finish) to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['b_q01c2'] = pd.to_numeric(piaac_df['b_q01c2'], errors='coerce')

    # creating a variable for the year when higher education decision was made
    log_record = 'creating a variable for the year when higher education decision was made'
    log_df = utility.log(log_df, log_record)
    conditions =[
        (piaac_df['b_q01a'] < 11),
        (piaac_df['b_q01a'] >= 11)]
    values = [
        piaac_df['b_q01c2'],
        piaac_df['b_q01c2'] - 3]
    piaac_df['decis_yr'] = np.select(conditions, values, default=float('nan'))

    # creating a variable for country specific decision year bins
    log_record = 'creating a variable for country specific decision year bins'
    log_df = utility.log(log_df, log_record)
    piaac_df['cntry_yr'] = piaac_df['cntrycode'] + ' ' + piaac_df['decis_yr'].astype(str).str[:4]
    
    return piaac_df, log_df
