
"""
LITTLE EXPERIMENT
    - take a real dataset
    - calculate mismatch measrues
    - randomly re-match firms and workers N times
    - compare the measures by the difference in the output between the original and random matching and its variance
    - (ideally you want a measure with large distance and small variance)

CURRENT STAGE: 
    - started coding the thing up. The plan is to split the dataset in the one with workers' characteristics
      and one with the jobs' requirements, loop for 1000 reps to reshuffle the jobs dataset and compute the mismatch.
    - TEMPORARILY DISCONTINUED: failed to see how it could be useful... perhaps it comes to mind later.w
"""

import pandas as pd
import numpy as np
import os
import sys
import importlib
import math
# for importlib.reload(lm)

file_wd = os.getcwd()
if '/' in file_wd:
    wd = '/'.join(file_wd.split('/')[:-1])
elif '\\' in file_wd:
    wd = '/'.join(file_wd.split('\\')[:-1])
sys.path.insert(0, wd)
print()
print('Working directory is set to: ' + os.getcwd())
print()

import labour_mismatch as lm

# 0 PRELIMINARIES
current_section = ""
log_file = pd.DataFrame(columns=['index', 'section', 'record'])

# 0.1 PIAAC Data
current_section = '0.1 Load PIAAC Data'
log_file = lm.utility.section(current_section, log_file)

# load PIAAC dataset
log_record = 'loading piaac dataset, please wait'
log_file = lm.utility.log(log_file, log_record)
piaac = pd.read_csv("/Users/seva/Desktop/projects/labour_mismatch/code/python/processed_data/lm_python_v1.csv", low_memory=False)

piaac['worker_id'] = range(1,len(piaac)+1) 
piaac['job_id'] = range(1,len(piaac)+1) 

piaac_orig = piaac['worker_id', 'isco08_sl_o', 'yrsqual', 'lit', 'num', 'psl',
                   'lit_zscore', 'num_zscore', 'psl_zscore',
                   'job_id',
                   'isco08_sl_r',
                   'og_mean_sl', 'og_std_sl', 'og_mode_sl',
                   'yrsget',
                   'dsa_lit_min', 'dsa_lit_max', 'dsa_relaxed_lit_min', 'dsa_relaxed_lit_max', 
                   'dsa_num_min', 'dsa_num_max', 'dsa_relaxed_num_min', 'dsa_relaxed_num_max',
                   'dsa_psl_min', 'dsa_psl_max', 'dsa_relaxed_psl_min', 'dsa_relaxed_psl_max',
                   'alv_lit_use_zscore', 'alv_num_use_zscore', 'alv_psl_use_zscore'
                   ]

piaac_workers = piaac['worker_id', 'isco08_sl_o', 'yrsqual', 'lit', 'num', 'psl',
                      'lit_zscore', 'num_zscore', 'psl_zscore']

piaac_jobs = piaac['job_id',
                   'isco08_sl_r',
                   'og_mean_sl', 'og_std_sl', 'og_mode_sl',
                   'yrsget',
                   'dsa_lit_min', 'dsa_lit_max', 'dsa_relaxed_lit_min', 'dsa_relaxed_lit_max', 
                   'dsa_num_min', 'dsa_num_max', 'dsa_relaxed_num_min', 'dsa_relaxed_num_max',
                   'dsa_psl_min', 'dsa_psl_max', 'dsa_relaxed_psl_min', 'dsa_relaxed_psl_max',
                   'alv_lit_use_zscore', 'alv_num_use_zscore', 'alv_psl_use_zscore']

