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

# 1 QUALIFICATION MISMATCH

# 1.1 ISCO-08 skill level
current_section = '1.1 ISCO-08 skill level'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.isco_sl.isco08_sl(piaac, log_file)

# 1.2 ISCO-08 occupation groups
current_section = '1.2 ISCO-08 occupation groups'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.isco_occ.occupations(piaac, log_file)

# 1.3 Realised Matches - meam
current_section = '1.3 Realised Matches - mean'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.em.rm_mean(piaac, 0.5, log_file)
piaac, log_file = lm.em.rm_mean(piaac, 1.5, log_file)
piaac, log_file = lm.em.rm_mean(piaac, 1, log_file)

# 1.4  Realised Matches - mode
current_section = '1.4 Realised Matches - mode'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.em.rm_mode(piaac, 0.1, log_file)
piaac, log_file = lm.em.rm_mode(piaac, 1, log_file)
piaac, log_file = lm.em.rm_mode(piaac, 2, log_file)

# 1.5 Job Assessment
current_section = '1.5 Job Assessment'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.em.ja(piaac, log_file)

# 1.6 Indirect Self-Assessment
current_section = '1.6 Indirect Self-Assessment'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.em.isa(piaac, 1, log_file)
piaac, log_file = lm.em.isa(piaac, 2, log_file)
piaac, log_file = lm.em.isa(piaac, 3, log_file)
piaac, log_file = lm.em.isa(piaac, 4, log_file)
piaac, log_file = lm.em.isa(piaac, 5, log_file)

# 2 SKILL MISMATCH

# 2.1 Direct Self Assessment
current_section = '2.1 Direct Self Assessment'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.dsa(piaac, log_file)

# 2.2 Pellizzari-Fichen Literacy
current_section = '2.2 Pellizzari-Fichen Literacy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.pf(piaac, 'lit', 0.025, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'lit', 0.05, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'lit', 0.1, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'lit', 0.025, True, log_file)
piaac, log_file = lm.sm.pf(piaac, 'lit', 0.05, True, log_file)
piaac, log_file = lm.sm.pf(piaac, 'lit', 0.1, True, log_file)

# 2.3 Pellizzari-Fichen Numeracy
current_section = '2.3 Pellizzari-Fichen Numeracy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.pf(piaac, 'num', 0.025, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'num', 0.05, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'num', 0.1, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'num', 0.025, True, log_file)
piaac, log_file = lm.sm.pf(piaac, 'num', 0.05, True, log_file)
piaac, log_file = lm.sm.pf(piaac, 'num', 0.1, True, log_file)

# 2.4 Pellizzari-Fichen Problem-Solving
current_section = '2.4 Pellizzari-Fichen Problem-Solving'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.pf(piaac, 'psl', 0.025, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'psl', 0.05, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'psl', 0.1, False, log_file)
piaac, log_file = lm.sm.pf(piaac, 'psl', 0.025, True, log_file)
piaac, log_file = lm.sm.pf(piaac, 'psl', 0.05, True, log_file)
piaac, log_file = lm.sm.pf(piaac, 'psl', 0.1, True, log_file)

# 2.5 Allen-Levels-van-der-Velden Literacy
current_section = '2.5 Allen-Levels-van-der-Velden Literacy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.alv(piaac, 'lit', 1, log_file)
piaac, log_file = lm.sm.alv(piaac, 'lit', 1.5, log_file)
piaac, log_file = lm.sm.alv(piaac, 'lit', 2, log_file)

# 2.6 Allen-Levels-van-der-Velden Numeracy
current_section = '2.6 Allen-Levels-van-der-Velden Numeracy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.alv(piaac, 'num', 1, log_file)
piaac, log_file = lm.sm.alv(piaac, 'num', 1.5, log_file)
piaac, log_file = lm.sm.alv(piaac, 'num', 2, log_file)

# 2.7 Allen-Levels-van-der-Velden Problem-Solving
current_section = '2.7 Allen-Levels-van-der-Velden Problem-Solving'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.sm.alv(piaac, 'psl', 1, log_file)
piaac, log_file = lm.sm.alv(piaac, 'psl', 1.5, log_file)
piaac, log_file = lm.sm.alv(piaac, 'psl', 2, log_file)

os.chdir("/Users/seva/Desktop/projects/labour_mismatch/code/python/processed_data")
log_record = 'directory is set to /Users/seva/Desktop/projects/labour_mismatch/code/python/processed_data'
log_file = lm.utility.log(log_file, log_record)

log_record = 'exporting the dataset to lm_python_v1.csv, please wait'
log_file = lm.utility.log(log_file, log_record)
piaac.to_csv('lm_python_v1.csv', index=False)
log_record = ('n=' + str(piaac.shape[0]))
log_file = lm.utility.log(log_file, log_record)

print()
print('LOG FILE')
lm.utility.print_tab(log_file)
log_file.to_csv('lm_main_log_file.csv', index=False)

