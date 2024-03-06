import pandas as pd
import numpy as np
import os
import sys
import importlib
# for importlib.reload(lm.sm)

print('Please enter the path, where the labour_mismatch folder is stored (format: c:/Users/John/Desktop/code)')
print()
wd_path = input()
sys.path.insert(0, wd_path)
print('Spcified path: ' + wd_path)
print()

import labour_mismatch as lm

# 0 PRELIMINARIES
current_section = ""
log_file = pd.DataFrame(columns=['index', 'section', 'record'])

# 0.1 PIAAC Data
current_section = '0.1 Load PIAAC Data'
log_file = lm.utility.section(current_section, log_file)

# set the directory
os.chdir(wd_path)
log_record = 'directory is set to ' + wd_path
log_file = lm.utility.log(log_file, log_record)

# load PIAAC dataset
log_record = 'loading piaac dataset, please wait'
log_file = lm.utility.log(log_file, log_record)
piaac = pd.read_csv(wd_path + '/piaac_data.csv', low_memory=False)

# 0.2 Preparation
current_section = '0.2 Preparations'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.prep.preparation(piaac, log_file)