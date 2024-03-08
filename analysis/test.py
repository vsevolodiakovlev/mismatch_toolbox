import pandas as pd
import numpy as np
import os
import sys
import importlib
# for importlib.reload(lm.sm)

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

# check the directory
log_record = 'directory is set to ' + os.getcwd()
log_file = lm.utility.log(log_file, log_record)

# load PIAAC dataset
log_record = 'loading piaac dataset, please wait'
log_file = lm.utility.log(log_file, log_record)
piaac = pd.read_csv(wd + '/piaac_data.csv', low_memory=False)

# 0.2 Preparation
current_section = '0.2 Preparations'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.prep.preparation(piaac, log_file)