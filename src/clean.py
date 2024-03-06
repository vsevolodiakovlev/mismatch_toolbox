from labour_mismatch.src import utility

"""
THIS REQUIRES REVIEW AND UPDATE

version: 27.07.23
FUNCTIONS
    drop_nan(df, var, log_df)
    drop_val(df, var, values_list, operator, log_df)
"""

def drop_nan(df, var, log_df):
    
    """
    Parameters
    ----------
    df : pandas.core.frame.DataFrame, dataset.
    var : str, variable name.
    log_df : pandas.core.frame.DataFrame, log file.

    Returns
    -------
    df : pandas.core.frame.DataFrame, dataset cleaned of missing values.
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
            log_df = utility.log(log_df, log_record)
            n_before = df.shape[0]
            cntries_before = df['cntryname'].value_counts()
            cntries_before = cntries_before.rename(var + ': orig')
            log_record = ('n=' + str(n_before))
            log_df = utility.log(log_df, log_record)
            log_record = ('removing the observations...')
            log_df = utility.log(log_df, log_record)
            df.drop(df[df[var] == nan].index, inplace=True)
            if (nan in df[var].unique()) == True:
                log_record = ('It did not work, ' + str(
                    df[var].value_counts()[nan]) + ' observations still have the value of nan for [' + var + ']')
                log_df = utility.log(log_df, log_record)
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                log_df = utility.log(log_df, log_record)
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
            log_df = utility.log(log_df, log_record)
            log_record = ('n=' + str(df.shape[0]))
            log_df = utility.log(log_df, log_record)
    else:
        if (df[var].isnull().values.any()) == True:
            log_record = (str(df[var].isnull().value_counts()[True]) + ' observations have the value of nan for [' + var + ']')
            log_df = utility.log(log_df, log_record)
            n_before = df.shape[0]
            cntries_before = df['cntryname'].value_counts()
            cntries_before = cntries_before.rename(var + ': orig')
            log_record = ('n=' + str(n_before))
            log_df = utility.log(log_df, log_record)
            log_record = ('removing the observations...')
            log_df = utility.log(log_df, log_record)
            df.dropna(subset=var, inplace=True)
            if (df[var].isnull().values.any()) == True:
                log_record = ('It did not work, ' + str(df[var].isnull().value_counts()[
                                                    True]) + ' observations still have the value of nan for [' + var + ']')
                log_df = utility.log(log_df, log_record)
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                log_df = utility.log(log_df, log_record)
                cntries_after = df['cntryname'].value_counts()
                cntries_after = cntries_after.rename(var + ': clnd')
                cntries_diff = cntries_before - cntries_after
                cntries_diff = cntries_diff.rename(var + ': diff')
            else:
                log_record = ('no observations have the value of nan for [' + var + ']')
                log_df = utility.log(log_df, log_record)
                n_afetr = df.shape[0]
                log_record = ('n=' + str(n_afetr) + '; ' + str(n_before - n_afetr) + ' observations have been removed')
                log_df = utility.log(log_df, log_record)
                cntries_after = df['cntryname'].value_counts()
                cntries_after = cntries_after.rename(var + ': clnd')
                cntries_diff = cntries_before - cntries_after
                cntries_diff = cntries_diff.rename(var + ': diff')
        else:
            log_record = ('no observations have the value of nan for [' + var + ']')
            log_df = utility.log(log_df, log_record)
            log_record = ('n=' + str(df.shape[0]))
            log_df = utility.log(log_df, log_record)
    return df, log_df

def drop_val(df, var, values_list, operator, log_df):
    
    """
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
    log_df = utility.log(log_df, log_record)
    log_record = ('dropping observations with ' + '[' +var + ']' + operator + str(values_list))
    log_df = utility.log(log_df, log_record)
    for value in values_list:
        if operator == '==':
            df.drop(df[df[var] == value].index, inplace=True)
        elif operator == '!=':
            df.drop(df[df[var] != value].index, inplace=True)
    n_after = df.shape[0]
    log_record = 'n=' + str(n_after) + '; ' + str(n_before - n_after) + ' observations have been removed'
    log_df = utility.log(log_df, log_record)
    
    return df, log_df

            
            