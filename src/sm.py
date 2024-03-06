import pandas as pd
import numpy as np
import math
from labour_mismatch.src import utility
from labour_mismatch.src import clean
from labour_mismatch.src import prep

"""
LAST REVISED: 06.03.24

dsa(piaac_df):
    - create variable for not challenged enough (notchal)
    - create variable for feeling need in training (needtrain)
    - creating variable for DSA skill mismatch (dsa)
    
pf_thresholds(piaac_df, occ_variable, skill_variable, l_quantile, h_quantile):
    - create variable for Pellizzari and Fichen skill mismatch lower threshold:
      for each occupation group
        * identify the lower quantile in the distribution of skill of the workers who 
          are neither not challenged enough nor feel need in additional training
        * append occupation group to the list of conditions
        * append the lower quantile to the list values
        * create the variable using conditions and values 
    - create variable for Pellizzari and Fichen skill mismatch higher threshold:
      for each occupation group
        * identify the higher quantile in the distribution of skill of the workers who 
          are neither not challenged enough nor feel need in additional training
        * append occupation group to the list of conditions
        * append the lower quantile to the list values
        * create the variable using conditions and values 
        
alv(piaac_df, skill_var, precision, log_df):
    COMMENT NEEDED real soon

THE FOLLOWING COMMENTS NEED TO BE UPDATED
pf_lit(piaac_df, precision):
    - create variable for the average of literacy plausible values (lit)
    - create literacy skill mismatch thresholds using pf_thresholds()
    - create variable for literacy skill mismatch (pf_lit)

pf_num(piaac_df, precision):
    - create variable for the average of numeracy plausible values (num)
    - create numeracy skill mismatch thresholds using pf_thresholds()
    - create variable for numeracy skill mismatch (pf_num)

pf_psl(piaac_df, precision):
    - create variable for the average of problem-solving plausible values (psl)
      note: unlike for literacy and numeracy, for problem-solving, missing values are not removed
    - create problem-solving skill mismatch thresholds using pf_thresholds()
    - create variable for problem-solving skill mismatch (pf_psl)
"""

def dsa(piaac_df, log_df):

    # converting f_q07a to float
    log_record = 'converting [f_q07a] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['f_q07a'] = pd.to_numeric(piaac_df['f_q07a'], errors='coerce')

    # check and drop for missing values in f_q07a
    var = 'f_q07a'
    log_record = 'check and drop for missing values in [' + var +']'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, var, log_df)

    # creating variable for being not challenged enough
    log_record = 'creating variable for being not challenged enough'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['f_q07a'] == 1),
        (piaac_df['f_q07a'] == 2)]
    values = [
        1,
        0]
    piaac_df['notchal'] = np.select(conditions, values, default=math.nan)

    # converting f_q07b to float
    log_record = 'converting [f_q07b] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['f_q07b'] = pd.to_numeric(piaac_df['f_q07b'], errors='coerce')

    # check and drop for missing values in f_q07b
    var = 'f_q07b'
    log_record = 'check and drop for missing values in [' + var +']'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, var, log_df)

    # creating variable for feeling need in training
    log_record = 'creating variable for feeling need in training'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['f_q07b'] == 1),
        (piaac_df['f_q07b'] == 2)]
    values = [
        1,
        0]
    piaac_df['needtrain'] = np.select(conditions, values, default=math.nan)

    # creating variable for DSA skill mismatch
    log_record = 'creating [dsa]: variable for DSA skill mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 0),
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 1),
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 2),
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 3)]
    values = [
        0,
        1,
        -1,
        9999]
    piaac_df['dsa'] = np.select(conditions, values, default=math.nan)
    
    log_record = 'creating [dsa_relaxed]: variable for "relaxed" DSA skill mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 0),
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 1),
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 2),
        (piaac_df['notchal'] + piaac_df['needtrain']*2 == 3)]
    values = [
        0,
        1,
        -1,
        0]
    piaac_df['dsa_relaxed'] = np.select(conditions, values, default=math.nan)
    
    var = 'dsa'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df


def pf_thresholds(piaac_df, occ_variable, skill_variable, dsa_relaxed, l_quantile, h_quantile, log_df):
    
    if dsa_relaxed == True:
        dsa_var = 'dsa_relaxed'
    else: 
        dsa_var = 'dsa'
    
    log_record = 'creating [' + dsa_var + '_' + skill_variable + '_min]: ' + occ_variable +'-specific thresholds at ' + str(l_quantile) + ' and ' + str(h_quantile) + ' percentiles'
    log_df = utility.log(log_df, log_record)
    conditions = []
    values = []
    
    for group in piaac_df[occ_variable].unique():
        sm_min = piaac_df.loc[(piaac_df[occ_variable] == group) * (piaac_df[dsa_var] == 0) == 1, skill_variable].quantile(l_quantile)
        conditions.append((piaac_df[occ_variable] == group))
        values.append(sm_min)
    piaac_df[dsa_var + '_' + skill_variable + '_min'] = np.select(conditions, values, default=math.nan)

    conditions = []
    values = []
    for group in piaac_df[occ_variable].unique():
        sm_max = piaac_df.loc[(piaac_df[occ_variable] == group) * (piaac_df[dsa_var] == 0) == 1, skill_variable].quantile(h_quantile)
        conditions.append((piaac_df[occ_variable] == group))
        values.append(sm_max)
    piaac_df[dsa_var + '_' + skill_variable + '_max'] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in mismatch thresholds (don't)
    var = dsa_var + '_' + skill_variable + '_max'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    var = dsa_var + '_' + skill_variable + '_min'
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)

    return piaac_df, log_df

def pf(piaac_df, skill_var, precision, dsa_relaxed, log_df):

    # creating variable for the average of plausible values
    log_record = 'creating [' + skill_var + ']: variable for the average of literacy plausible values'
    log_df = utility.log(log_df, log_record)
    piaac_df[skill_var] = 0.1 * (piaac_df['pv' + skill_var + '1'] + 
                                 piaac_df['pv' + skill_var + '2'] + 
                                 piaac_df['pv' + skill_var + '3'] + 
                                 piaac_df['pv' + skill_var + '4'] + 
                                 piaac_df['pv' + skill_var + '5'] + 
                                 piaac_df['pv' + skill_var + '6'] +
                                 piaac_df['pv' + skill_var + '7'] +
                                 piaac_df['pv' + skill_var + '8'] +
                                 piaac_df['pv' + skill_var + '9'] +
                                 piaac_df['pv' + skill_var + '10'])

    # converting [skill_var] to float
    log_record = 'converting [' + skill_var + '] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df[skill_var] = pd.to_numeric(piaac_df[skill_var], errors='coerce')
    
    # check and drop for missing values in [skill_var] (don't)
    var = skill_var
    log_record = 'missing values cleaning skipped for [' + var + ']'
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for [' + var + ']')
    log_df = utility.log(log_df, log_record)
    
    # creating skill mismatch thresholds
    if dsa_relaxed == True:
        log_record = 'creating [' + skill_var + '] skill mismatch thresholds, [dsa_relaxed] = True'
        log_df = utility.log(log_df, log_record)
        piaac_df, log_df = pf_thresholds(piaac_df, 'cntry_isco_lbl', skill_var, True, precision, 1-precision, log_df)
        mismatch_var = 'pf_' + skill_var + '_' + str(precision).replace('.', '') + '_relaxed'
        skill_var_min = 'dsa_relaxed_' + skill_var + '_min'
        skill_var_max = 'dsa_relaxed_' + skill_var + '_max'
    else:
        log_record = 'creating [' + skill_var + '] skill mismatch thresholds, [dsa_relaxed] = False'
        log_df = utility.log(log_df, log_record)
        piaac_df, log_df = pf_thresholds(piaac_df, 'cntry_isco_lbl', skill_var, False, precision, 1-precision, log_df)
        mismatch_var = 'pf_' + skill_var + '_' + str(precision).replace('.', '')
        skill_var_min = 'dsa_' + skill_var + '_min'
        skill_var_max = 'dsa_' + skill_var + '_max'

    # creating variable for skill mismatch
    log_record = 'creating [' + mismatch_var + ']: variable for literacy skill mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df[skill_var] < piaac_df[skill_var_min]),
        ((piaac_df[skill_var] < piaac_df[skill_var_max]) & (piaac_df[skill_var] >= piaac_df[skill_var_min])),
        (piaac_df[skill_var] >= piaac_df[skill_var_max])]
    values = [
        -1,
        0,
        1]
    piaac_df[mismatch_var] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in [mismatch_var] (don't)
    var = mismatch_var
    log_record = 'missing values cleaning skipped for [' + var + ']'
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for [' + var + ']')
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df

def alv(piaac_df, skill_var, precision, log_df):

    # creating variable for the average of plausible values
    log_record = 'creating [' + skill_var + ']: variable for the average of literacy plausible values'
    log_df = utility.log(log_df, log_record)
    piaac_df[skill_var] = 0.1 * (piaac_df['pv' + skill_var + '1'] +
                                 piaac_df['pv' + skill_var + '2'] +
                                 piaac_df['pv' + skill_var + '3'] +
                                 piaac_df['pv' + skill_var + '4'] +
                                 piaac_df['pv' + skill_var + '5'] +
                                 piaac_df['pv' + skill_var + '6'] +
                                 piaac_df['pv' + skill_var + '7'] +
                                 piaac_df['pv' + skill_var + '8'] +
                                 piaac_df['pv' + skill_var + '9'] +
                                 piaac_df['pv' + skill_var + '10'])

    # converting [skill_var] to float
    log_record = 'converting [' + skill_var + '] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df[skill_var] = pd.to_numeric(piaac_df[skill_var], errors='coerce')

    # check and drop for missing values in [skill_var] (don't)
    var = skill_var
    log_record = 'missing values cleaning skipped for [' + var + ']'
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[
        False]) + ' observations have the value of nan for [' + var + ']')
    log_df = utility.log(log_df, log_record)

    # creating a standardised version of the skill variable
    log_record = 'creating [' + skill_var + '_zscore] (standardising)'
    log_df = utility.log(log_df, log_record)
    piaac_df[skill_var + '_zscore'] = (piaac_df[skill_var] - piaac_df[skill_var].mean()) / piaac_df[skill_var].std()

    if skill_var == 'lit':

        # converting literacy use variables to float
        log_record = 'converting literacy use variables to float'
        log_df = utility.log(log_df, log_record)
        varlist = ['g_q01a', 'g_q01b', 'g_q01c', 'g_q01d', 'g_q01e', 'g_q01f', 'g_q01g', 'g_q01h',
                   'g_q02a', 'g_q02b', 'g_q02c', 'g_q02d']
        for var in varlist:
            piaac_df[var] = pd.to_numeric(piaac_df[var], errors='coerce')

        # creating and standardising aggregate literacy use variable
        log_record = 'creating and standardising aggregate literacy use variables'
        log_df = utility.log(log_df, log_record)
        conditions = [
            (piaac_df['g_q01a'].isnull().astype(int) +
            piaac_df['g_q01b'].isnull().astype(int) +
            piaac_df['g_q01c'].isnull().astype(int) +
            piaac_df['g_q01d'].isnull().astype(int) +
            piaac_df['g_q01e'].isnull().astype(int) +
            piaac_df['g_q01f'].isnull().astype(int) +
            piaac_df['g_q01g'].isnull().astype(int) +
            piaac_df['g_q01h'].isnull().astype(int) +
            piaac_df['g_q02a'].isnull().astype(int) +
            piaac_df['g_q02b'].isnull().astype(int) +
            piaac_df['g_q02c'].isnull().astype(int) +
            piaac_df['g_q02d'].isnull().astype(int) == 0)
        ]
        values = [
            ((piaac_df['g_q01a'] +
             piaac_df['g_q01b'] +
             piaac_df['g_q01c'] +
             piaac_df['g_q01d'] +
             piaac_df['g_q01e'] +
             piaac_df['g_q01f'] +
             piaac_df['g_q01g'] +
             piaac_df['g_q01h'] +
             piaac_df['g_q02a'] +
             piaac_df['g_q02b'] +
             piaac_df['g_q02c'] +
             piaac_df['g_q02d']) / 12)
        ]
        piaac_df['alv_lit_use'] = np.select(conditions, values, default=math.nan)
        piaac_df['alv_lit_use_zscore'] = (piaac_df['alv_lit_use'] - piaac_df['alv_lit_use'].mean()) / piaac_df['alv_lit_use'].std()

        # creating Allen-Levels-van-der-Velden skill mismatch variable for literacy
        log_record = 'creating Allen-Levels-van-der-Velden skill mismatch variable for literacy'
        log_df = utility.log(log_df, log_record)
        conditions = [
            (piaac_df['lit_zscore'] - piaac_df['alv_lit_use_zscore'] < -precision),
            ((piaac_df['lit_zscore'] - piaac_df['alv_lit_use_zscore'] > -precision) & (piaac_df['lit_zscore'] - piaac_df['alv_lit_use_zscore'] < precision)),
            (piaac_df['lit_zscore'] - piaac_df['alv_lit_use_zscore'] > precision)
        ]
        values = [
            -1,
            0,
            1
        ]
        piaac_df['alv_lit_' + str(precision).replace('.', '')] = np.select(conditions, values, default=math.nan)

        # check and drop for missing values in [alv_lit_] (don't)
        var = 'alv_lit_' + str(precision).replace('.', '')
        log_record = 'missing values cleaning skipped for [' + var + ']'
        log_df = utility.log(log_df, log_record)
        log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[
            False]) + ' observations have the value of nan for [' + var + ']')
        log_df = utility.log(log_df, log_record)

    elif skill_var == 'num':

        # converting numeracy use variables to float
        log_record = 'numeracy numeracy use variables to float'
        log_df = utility.log(log_df, log_record)
        varlist = ['g_q03b', 'g_q03c', 'g_q03d', 'g_q03f', 'g_q03g', 'g_q03h']
        for var in varlist:
            piaac_df[var] = pd.to_numeric(piaac_df[var], errors='coerce')

        # creating and standardising aggregate numeracy use variable
        log_record = 'creating and standardising aggregate numeracy use variables'
        log_df = utility.log(log_df, log_record)
        conditions = [
            (piaac_df['g_q03b'].isnull().astype(int) +
             piaac_df['g_q03c'].isnull().astype(int) +
             piaac_df['g_q03d'].isnull().astype(int) +
             piaac_df['g_q03f'].isnull().astype(int) +
             piaac_df['g_q03g'].isnull().astype(int) +
             piaac_df['g_q03h'].isnull().astype(int) == 0)
        ]
        values = [
            ((piaac_df['g_q03b'] +
              piaac_df['g_q03c'] +
              piaac_df['g_q03d'] +
              piaac_df['g_q03f'] +
              piaac_df['g_q03g'] +
              piaac_df['g_q03h']) / 6)
        ]
        piaac_df['alv_num_use'] = np.select(conditions, values, default=math.nan)
        piaac_df['alv_num_use_zscore'] = (piaac_df['alv_num_use'] - piaac_df['alv_num_use'].mean()) / piaac_df[
            'alv_num_use'].std()

        # creating Allen-Levels-van-der-Velden skill mismatch variable for numeracy
        log_record = 'creating Allen-Levels-van-der-Velden skill mismatch variable for numeracy'
        log_df = utility.log(log_df, log_record)
        conditions = [
            (piaac_df['num_zscore'] - piaac_df['alv_num_use_zscore'] < -precision),
            ((piaac_df['num_zscore'] - piaac_df['alv_num_use_zscore'] > -precision) & (
                        piaac_df['num_zscore'] - piaac_df['alv_num_use_zscore'] < precision)),
            (piaac_df['num_zscore'] - piaac_df['alv_num_use_zscore'] > precision)
        ]
        values = [
            -1,
            0,
            1
        ]
        piaac_df['alv_num_' + str(precision).replace('.', '')] = np.select(conditions, values, default=math.nan)

        # check and drop for missing values in [alv_num_] (don't)
        var = 'alv_num_' + str(precision).replace('.', '')
        log_record = 'missing values cleaning skipped for [' + var + ']'
        log_df = utility.log(log_df, log_record)
        log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[
            False]) + ' observations have the value of nan for [' + var + ']')
        log_df = utility.log(log_df, log_record)


    elif skill_var == 'psl':

        # converting problem-solving use variables to float
        log_record = 'problem-solving numeracy use variables to float'
        log_df = utility.log(log_df, log_record)
        varlist = ['f_q05a', 'f_q05b']
        for var in varlist:
            piaac_df[var] = pd.to_numeric(piaac_df[var], errors='coerce')

        # creating and standardising aggregate problem-solving use variable
        log_record = 'creating and standardising aggregate problem-solving use variables'
        log_df = utility.log(log_df, log_record)
        conditions = [
            (piaac_df['f_q05a'].isnull().astype(int) +
             piaac_df['f_q05b'].isnull().astype(int) == 0)
        ]
        values = [
            ((piaac_df['f_q05a'] +
              piaac_df['f_q05b']) / 2)
        ]
        piaac_df['alv_psl_use'] = np.select(conditions, values, default=math.nan)
        piaac_df['alv_psl_use_zscore'] = (piaac_df['alv_psl_use'] - piaac_df['alv_psl_use'].mean()) / piaac_df[
            'alv_psl_use'].std()

        # creating Allen-Levels-van-der-Velden skill mismatch variable for problem-solving
        log_record = 'creating Allen-Levels-van-der-Velden skill mismatch variable for problem-solving'
        log_df = utility.log(log_df, log_record)
        conditions = [
            (piaac_df['psl_zscore'] - piaac_df['alv_psl_use_zscore'] < -precision),
            ((piaac_df['psl_zscore'] - piaac_df['alv_psl_use_zscore'] > -precision) & (
                    piaac_df['psl_zscore'] - piaac_df['alv_psl_use_zscore'] < precision)),
            (piaac_df['psl_zscore'] - piaac_df['alv_psl_use_zscore'] > precision)
        ]
        values = [
            -1,
            0,
            1
        ]
        piaac_df['alv_psl_' + str(precision).replace('.', '')] = np.select(conditions, values, default=math.nan)

        # check and drop for missing values in [alv_psl_] (don't)
        var = 'alv_psl_' + str(precision).replace('.', '')
        log_record = 'missing values cleaning skipped for [' + var + ']'
        log_df = utility.log(log_df, log_record)
        log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[
            False]) + ' observations have the value of nan for [' + var + ']')
        log_df = utility.log(log_df, log_record)

"""
def pf_lit(piaac_df, precision, dsa_relaxed, log_df):

    # creating variable for the average of literacy plausible values
    log_record = 'creating [lit]: variable for the average of literacy plausible values'
    log_df = utility.log(log_df, log_record)
    piaac_df['lit'] = 0.1 * (piaac_df['pvlit1'] + piaac_df['pvlit2'] + piaac_df['pvlit3'] + piaac_df['pvlit4'] + piaac_df['pvlit5'] + piaac_df['pvlit6'] +piaac_df['pvlit7'] +piaac_df['pvlit8'] +piaac_df['pvlit9'] +piaac_df['pvlit10'])

    # converting lit to float
    log_record = 'converting [lit] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['lit'] = pd.to_numeric(piaac_df['lit'], errors='coerce')

    # check and drop for missing values in lit
    log_record = 'check and drop for missing values in [lit]'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'lit', log_df)

    # creating literacy skill mismatch thresholds
    if dsa_relaxed == True:
        log_record = 'creating literacy skill mismatch thresholds, [dsa_relaxed] = True'
        log_df = utility.log(log_df, log_record)
        piaac_df, log_df = pf_thresholds(piaac_df, 'cntry_isco_lbl', 'lit', True, precision, 1-precision, log_df)
    else:
        log_record = 'creating literacy skill mismatch thresholds, [dsa_relaxed] = False'
        log_df = utility.log(log_df, log_record)
        piaac_df, log_df = pf_thresholds(piaac_df, 'cntry_isco_lbl', 'lit', False, precision, 1-precision, log_df)

    # creating variable for literacy skill mismatch
    log_record = 'creating [pf_lit_' + str(precision).replace('.', '') + ']: variable for literacy skill mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['lit'] < piaac_df['lit_min']),
        ((piaac_df['lit'] < piaac_df['lit_max']) & (piaac_df['lit'] >= piaac_df['lit_min'])),
        (piaac_df['lit'] >= piaac_df['lit_max'])]
    values = [
        -1,
        0,
        1]
    piaac_df['pf_lit_' + str(precision).replace('.', '')] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in literacy skill mismatch
    log_record = 'check and drop for missing values in [pf_lit_' + str(precision).replace('.', '') + ']'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'pf_lit_' + str(precision).replace('.', ''), log_df)
    
    return piaac_df, log_df


def pf_num(piaac_df, precision, log_df):

    # creating variable for the average of numeracy plausible values
    log_record = 'creating [num]: variable for the average of numeracy plausible values'
    log_df = utility.log(log_df, log_record)
    piaac_df['num'] = 0.1 * (
                piaac_df['pvnum1'] + piaac_df['pvnum2'] + piaac_df['pvnum3'] + piaac_df['pvnum4'] + piaac_df['pvnum5'] + piaac_df[
            'pvnum6'] + piaac_df['pvnum7'] + piaac_df['pvnum8'] + piaac_df['pvnum9'] + piaac_df['pvnum10'])

    # converting num to float
    log_record = 'converting [num] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['num'] = pd.to_numeric(piaac_df['num'], errors='coerce')

    # check and drop for missing values in num
    log_record = 'check and drop for missing values in [num]'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'num', log_df)

    # creating numeracy skill mismatch thresholds
    log_record = 'creating numeracy skill mismatch thresholds'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = pf_thresholds(piaac_df, 'cntry_isco_lbl', 'num', precision, 1-precision, log_df)

    # creating variable for numeracy skill mismatch
    log_record = 'creating [pf_num_' + str(precision).replace('.', '') + ']: variable for numeracy skill mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['num'] < piaac_df['num_min']),
        ((piaac_df['num'] < piaac_df['num_max']) & (piaac_df['num'] >= piaac_df['num_min'])),
        (piaac_df['num'] >= piaac_df['num_max'])]
    values = [
        -1,
        0,
        1]
    piaac_df['pf_num_' + str(precision).replace('.', '')] = np.select(conditions, values, default=math.nan)
    
    # check and drop for missing values in numeracy skill mismatch
    log_record = 'check and drop for missing values in [pf_num_' + str(precision).replace('.', '') + ']'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = clean.drop_nan(piaac_df, 'pf_num_' + str(precision).replace('.', ''), log_df)
    
    return piaac_df, log_df



def pf_psl(piaac_df, precision, log_df):


    # creating variable for the average of problem-solving plausible values
    log_record = 'creating [psl]: variable for the average of problem-solving plausible values'
    log_df = utility.log(log_df, log_record)
    piaac_df['psl'] = 0.1 * (
                piaac_df['pvpsl1'] + piaac_df['pvpsl2'] + piaac_df['pvpsl3'] + piaac_df['pvpsl4'] + piaac_df['pvpsl5'] + piaac_df[
            'pvpsl6'] + piaac_df['pvpsl7'] + piaac_df['pvpsl8'] + piaac_df['pvpsl9'] + piaac_df['pvpsl10'])

    # converting psl to float
    log_record = 'converting [psl] to float'
    log_df = utility.log(log_df, log_record)
    piaac_df['psl'] = pd.to_numeric(piaac_df['psl'], errors='coerce')

    # creating problem-solving skill mismatch thresholds
    log_record = 'creating problem-solving skill mismatch thresholds'
    log_df = utility.log(log_df, log_record)
    piaac_df, log_df = pf_thresholds(piaac_df, 'cntry_isco_lbl', 'psl', precision, 1-precision, log_df)

    # creating variable for problem-solving skill mismatch
    log_record = 'creating [pf_psl_' + str(precision).replace('.', '') + ']: variable for problem-solving skill mismatch'
    log_df = utility.log(log_df, log_record)
    conditions = [
        (piaac_df['psl'] < piaac_df['psl_min']),
        ((piaac_df['psl'] < piaac_df['psl_max']) & (piaac_df['psl'] >= piaac_df['psl_min'])),
        (piaac_df['psl'] >= piaac_df['psl_max'])]
    values = [
        -1,
        0,
        1]
    piaac_df['pf_psl_' + str(precision).replace('.', '')] = np.select(conditions, values, default=math.nan)
    
    var = 'pf_psl_' + str(precision).replace('.', '')
    log_record = 'missing values cleaning skipped for ' + var
    log_df = utility.log(log_df, log_record)
    log_record = (str(piaac_df.shape[0] - piaac_df[var].isnull().value_counts()[False]) + ' observations have the value of nan for ' + var)
    log_df = utility.log(log_df, log_record)
    
    return piaac_df, log_df

"""