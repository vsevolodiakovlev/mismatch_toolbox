import pandas as pd
import numpy as np
import os
import sys
import importlib
import math
# for importlib.reload(lm)

sys.path.insert(0, '/Users/seva/Desktop/projects/labour_mismatch/code/python')
import labour_mismatch as lm


# 0 PRELIMINARIES
current_section = ""
log_file = pd.DataFrame(columns=['index', 'section', 'record'])

# 0.1 PIAAC Data
current_section = '0.1 Load PIAAC Data'
log_file = lm.utility.section(current_section, log_file)

# set the directory
os.chdir("/Users/seva/Desktop/projects/labour_mismatch/code/python")
log_record = 'directory is set to Users/seva/labour_mismatch/code/python'
log_file = lm.utility.log(log_file, log_record)

# load PIAAC dataset
log_record = 'loading piaac dataset, please wait'
log_file = lm.utility.log(log_file, log_record)
piaac = pd.read_csv("/Users/seva/Desktop/projects/labour_mismatch/code/python/processed_data/lm_python_v1.csv", low_memory=False)

# converting gender_r to float
log_record = 'converting [gender_r] to float'
log_file = lm.utility.log(log_file, log_record)
piaac['gender_r'] = pd.to_numeric(piaac['gender_r'], errors='coerce')

# converting age_r to float
log_record = 'converting [age_r] to float'
log_file = lm.utility.log(log_file, log_record)
piaac['age_r'] = pd.to_numeric(piaac['age_r'], errors='coerce')


# 1 Summary Statistic

current_section = '1 Summary Statistic'
log_file = lm.utility.section(current_section, log_file)

os.chdir("/Users/seva/Desktop/projects/labour_mismatch/latex/ch1_exploration/tables/sum_stats")
log_record = '/Users/seva/Desktop/projects/labour_mismatch/latex/ch1_exploration/tables/sum_stats'
log_file = lm.utility.log(log_file, log_record)

# Earnings and education

sumstat_earn_ed = piaac[['earn', 'b_q01a', 'isco08_sl_o', 'isco08_sl_r', 'yrsqual', 'yrsget']].describe(include='all').round(2).to_latex()
sumstat_earn_ed = sumstat_earn_ed.replace('{} &      earn &    b\_q01a &  isco08\_sl\_o &  isco08\_sl\_r &   yrsqual &    yrsget \\',
                                          '{} & Earnings     & Highest     & Obtained  & Required  & Obtained   & Required \\\  &    & qual.     & ISCO SL   & ISCO SL   & years of ed      & year of ed.    \\')
sumstat_earn_ed = sumstat_earn_ed.replace('.00', '')
with open('sumstat_earn_ed.tex','w') as file:
    file.write(sumstat_earn_ed)
log_record = 'table is saved as ' + 'sumstat_earn_ed' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# Skills

sumstat_skills = piaac[['notchal', 'needtrain', 'lit', 'num', 'psl']].describe(include='all').round(2).to_latex()
sumstat_skills = sumstat_skills.replace('{} &   notchal &  needtrain &       lit &       num &       psl \\', 
                                        '{} &   Not challenged &  Need training &       Literacy &       Numeracy &       Problem-solving \\')
sumstat_skills = sumstat_skills.replace('.00', '')
with open('sumstat_skills.tex','w') as file:
    file.write(sumstat_skills)
log_record = 'table is saved as ' + 'sumstat_skills' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# Occupations

occ_count = pd.concat([piaac.isco_lbl.value_counts(),
                    piaac.isco_lbl.value_counts(normalize=True).round(2),
                    piaac[['isco_lbl', 'earn']].groupby(by='isco_lbl').median().round(2),
                    piaac[['isco_lbl', 'b_q01a']].groupby(by='isco_lbl').median().round(2),
                    piaac[['isco_lbl', 'lit']].groupby(by='isco_lbl').mean().round(2),
                    piaac[['isco_lbl', 'num']].groupby(by='isco_lbl').mean().round(2),
                    piaac[['isco_lbl', 'psl']].groupby(by='isco_lbl').mean().round(2),
                    piaac[['isco_lbl', 'gender_r']].groupby(by='isco_lbl').mean().round(2)-1,
                    piaac[['isco_lbl', 'age_r']].groupby(by='isco_lbl').mean().round(2)],
                    axis=1)
occ_count = occ_count.sort_values('earn', ascending=False).to_latex()
occ_count = occ_count.replace('{} &  isco\_lbl &  isco\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')
occ_count = occ_count.replace('.00', '')
occ_count = occ_count.replace('High skilled managers', 'HS managers')
occ_count = occ_count.replace('Professionals', 'Professionals')
occ_count = occ_count.replace('Technicians and associate professionals', 'Techc-s \& assoc.')
occ_count = occ_count.replace('Low skilled managers', 'LS managers ')
occ_count = occ_count.replace('Clerical support workers', 'Clerical support')
occ_count = occ_count.replace('Craft and related trades workers', 'Craft \& related')
occ_count = occ_count.replace('Plant and machine operators, and assemblers', 'Operat. \& assem.')
occ_count = occ_count.replace('Service and sales workers', 'Service and sales')
occ_count = occ_count.replace('Elementary occupations', 'Element. occup.')
occ_count = occ_count.replace('Skilled agricultural, forestry and fishery workers', 'Agric. \& fishery')
with open('occ_count.tex','w') as file:
    file.write(occ_count)
log_record = 'table is saved as ' + 'occ_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# Countries

cntry_count = pd.concat([piaac.cntryname.value_counts(),
                    piaac.cntryname.value_counts(normalize=True).round(2),
                    piaac[['cntryname', 'earn']].groupby(by='cntryname').median().round(2),
                    piaac[['cntryname', 'b_q01a']].groupby(by='cntryname').median().round(2),
                    piaac[['cntryname', 'lit']].groupby(by='cntryname').mean().round(2),
                    piaac[['cntryname', 'num']].groupby(by='cntryname').mean().round(2),
                    piaac[['cntryname', 'psl']].groupby(by='cntryname').mean().round(2),
                    piaac[['cntryname', 'gender_r']].groupby(by='cntryname').mean().round(2)-1,
                    piaac[['cntryname', 'age_r']].groupby(by='cntryname').mean().round(2)],
                    axis=1)
cntry_count = cntry_count.sort_values('earn', ascending=False).to_latex()
cntry_count = cntry_count.replace('{} &  cntryname &  cntryname &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')
cntry_count = cntry_count.replace('.00', '')
with open('cntry_count.tex','w') as file:
    file.write(cntry_count)
log_record = 'table is saved as ' + 'cntry_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# JA

# creating variable for ja labels
log_record = 'creating [js_lbl]: ja labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['ja'] == 1,
    piaac['ja'] == 0,
    piaac['ja'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['ja_lbl'] = np.select(conditions, values, default=math.nan)

ja_count = pd.concat([piaac['ja_lbl'].value_counts(),
                    piaac['ja_lbl'].value_counts(normalize=True).round(2),
                    piaac[['ja_lbl', 'earn']].groupby(by='ja_lbl').median().round(2),
                    piaac[['ja_lbl', 'b_q01a']].groupby(by='ja_lbl').median().round(2),
                    piaac[['ja_lbl', 'lit']].groupby(by='ja_lbl').mean().round(2),
                    piaac[['ja_lbl', 'num']].groupby(by='ja_lbl').mean().round(2),
                    piaac[['ja_lbl', 'psl']].groupby(by='ja_lbl').mean().round(2),
                    piaac[['ja_lbl', 'gender_r']].groupby(by='ja_lbl').mean().round(2)-1,
                    piaac[['ja_lbl', 'age_r']].groupby(by='ja_lbl').mean().round(2)],
                    axis=1)
ja_count = ja_count.sort_index().to_latex()
ja_count = ja_count.replace('.00', '')
ja_count = ja_count.replace('{} &  ja\_lbl &  ja\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('ja_count.tex','w') as file:
    file.write(ja_count)
log_record = 'table is saved as ' + 'ja_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# RM

# creating variable for rm_mode_1 labels
log_record = 'creating [rm_mode_1_lbl]: rm_mode_1 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['rm_mode_1'] == 1,
    piaac['rm_mode_1'] == 0,
    piaac['rm_mode_1'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['rm_mode_1_lbl'] = np.select(conditions, values, default=math.nan)

rm_mode_1_count = pd.concat([piaac['rm_mode_1_lbl'].value_counts(),
                    piaac['rm_mode_1_lbl'].value_counts(normalize=True).round(2),
                    piaac[['rm_mode_1_lbl', 'earn']].groupby(by='rm_mode_1_lbl').median().round(2),
                    piaac[['rm_mode_1_lbl', 'b_q01a']].groupby(by='rm_mode_1_lbl').median().round(2),
                    piaac[['rm_mode_1_lbl', 'lit']].groupby(by='rm_mode_1_lbl').mean().round(2),
                    piaac[['rm_mode_1_lbl', 'num']].groupby(by='rm_mode_1_lbl').mean().round(2),
                    piaac[['rm_mode_1_lbl', 'psl']].groupby(by='rm_mode_1_lbl').mean().round(2),
                    piaac[['rm_mode_1_lbl', 'gender_r']].groupby(by='rm_mode_1_lbl').mean().round(2)-1,
                    piaac[['rm_mode_1_lbl', 'age_r']].groupby(by='rm_mode_1_lbl').mean().round(2)],
                    axis=1)
rm_mode_1_count = rm_mode_1_count.sort_index().to_latex()
rm_mode_1_count = rm_mode_1_count.replace('.00', '')
rm_mode_1_count = rm_mode_1_count.replace('{} &  rm\_mode\_1\_lbl &  rm\_mode\_1\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('rm_mode_1_count.tex','w') as file:
    file.write(rm_mode_1_count)
log_record = 'table is saved as ' + 'rm_mode_1_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# ISA

# creating variable for isa_1 labels
log_record = 'creating [isa_1_lbl]: isa_1 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['isa_1'] == 1,
    piaac['isa_1'] == 0,
    piaac['isa_1'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['isa_1_lbl'] = np.select(conditions, values, default=math.nan)

isa_1_count = pd.concat([piaac['isa_1_lbl'].value_counts(),
                    piaac['isa_1_lbl'].value_counts(normalize=True).round(2),
                    piaac[['isa_1_lbl', 'earn']].groupby(by='isa_1_lbl').median().round(2),
                    piaac[['isa_1_lbl', 'b_q01a']].groupby(by='isa_1_lbl').median().round(2),
                    piaac[['isa_1_lbl', 'lit']].groupby(by='isa_1_lbl').mean().round(2),
                    piaac[['isa_1_lbl', 'num']].groupby(by='isa_1_lbl').mean().round(2),
                    piaac[['isa_1_lbl', 'psl']].groupby(by='isa_1_lbl').mean().round(2),
                    piaac[['isa_1_lbl', 'gender_r']].groupby(by='isa_1_lbl').mean().round(2)-1,
                    piaac[['isa_1_lbl', 'age_r']].groupby(by='isa_1_lbl').mean().round(2)],
                    axis=1)
isa_1_count = isa_1_count.sort_index().to_latex()
isa_1_count = isa_1_count.replace('.00', '')
isa_1_count = isa_1_count.replace('{} &  isa\_1\_lbl &  isa\_1\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('isa_1_count.tex','w') as file:
    file.write(isa_1_count)
log_record = 'table is saved as ' + 'isa_1_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# DSA

# creating variable for dsa labels
log_record = 'creating [dsa_lbl]: dsa labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['dsa'] == 1,
    piaac['dsa'] == 0,
    piaac['dsa'] == 9999,
    piaac['dsa'] == -1]
values = [
    'Over',
    'Well',
    'DP Error',
    'Under']
piaac['dsa_lbl'] = np.select(conditions, values, default=math.nan)

dsa_count = pd.concat([piaac['dsa_lbl'].value_counts(),
                    piaac['dsa_lbl'].value_counts(normalize=True).round(2),
                    piaac[['dsa_lbl', 'earn']].groupby(by='dsa_lbl').median().round(2),
                    piaac[['dsa_lbl', 'b_q01a']].groupby(by='dsa_lbl').median().round(2),
                    piaac[['dsa_lbl', 'lit']].groupby(by='dsa_lbl').mean().round(2),
                    piaac[['dsa_lbl', 'num']].groupby(by='dsa_lbl').mean().round(2),
                    piaac[['dsa_lbl', 'psl']].groupby(by='dsa_lbl').mean().round(2),
                    piaac[['dsa_lbl', 'gender_r']].groupby(by='dsa_lbl').mean().round(2)-1,
                    piaac[['dsa_lbl', 'age_r']].groupby(by='dsa_lbl').mean().round(2)],
                    axis=1)
dsa_count = dsa_count.sort_index().to_latex()
dsa_count = dsa_count.replace('.00', '')
dsa_count = dsa_count.replace('{} &  dsa\_lbl &  dsa\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('dsa_count.tex','w') as file:
    file.write(dsa_count)
log_record = 'table is saved as ' + 'dsa_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)


# PFL

# creating variable for pf_lit_005 labels
log_record = 'creating [pf_lit_005_lbl]: pf_lit_005 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['pf_lit_005'] == 1,
    piaac['pf_lit_005'] == 0,
    piaac['pf_lit_005'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['pf_lit_005_lbl'] = np.select(conditions, values, default=math.nan)

pf_lit_005_count = pd.concat([piaac['pf_lit_005_lbl'].value_counts(),
                    piaac['pf_lit_005_lbl'].value_counts(normalize=True).round(2),
                    piaac[['pf_lit_005_lbl', 'earn']].groupby(by='pf_lit_005_lbl').median().round(2),
                    piaac[['pf_lit_005_lbl', 'b_q01a']].groupby(by='pf_lit_005_lbl').median().round(2),
                    piaac[['pf_lit_005_lbl', 'lit']].groupby(by='pf_lit_005_lbl').mean().round(2),
                    piaac[['pf_lit_005_lbl', 'num']].groupby(by='pf_lit_005_lbl').mean().round(2),
                    piaac[['pf_lit_005_lbl', 'psl']].groupby(by='pf_lit_005_lbl').mean().round(2),
                    piaac[['pf_lit_005_lbl', 'gender_r']].groupby(by='pf_lit_005_lbl').mean().round(2)-1,
                    piaac[['pf_lit_005_lbl', 'age_r']].groupby(by='pf_lit_005_lbl').mean().round(2)],
                    axis=1)
pf_lit_005_count = pf_lit_005_count.sort_index().to_latex()
pf_lit_005_count = pf_lit_005_count.replace('.00', '')
pf_lit_005_count = pf_lit_005_count.replace('{} &  pf\_lit\_005\_lbl &  pf\_lit\_005\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('pf_lit_005_count.tex','w') as file:
    file.write(pf_lit_005_count)
log_record = 'table is saved as ' + 'pf_lit_005_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)


# PFN

# creating variable for pf_num_005 labels
log_record = 'creating [pf_num_005_lbl]: pf_num_005 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['pf_num_005'] == 1,
    piaac['pf_num_005'] == 0,
    piaac['pf_num_005'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['pf_num_005_lbl'] = np.select(conditions, values, default=math.nan)

pf_num_005_count = pd.concat([piaac['pf_num_005_lbl'].value_counts(),
                    piaac['pf_num_005_lbl'].value_counts(normalize=True).round(2),
                    piaac[['pf_num_005_lbl', 'earn']].groupby(by='pf_num_005_lbl').median().round(2),
                    piaac[['pf_num_005_lbl', 'b_q01a']].groupby(by='pf_num_005_lbl').median().round(2),
                    piaac[['pf_num_005_lbl', 'lit']].groupby(by='pf_num_005_lbl').mean().round(2),
                    piaac[['pf_num_005_lbl', 'num']].groupby(by='pf_num_005_lbl').mean().round(2),
                    piaac[['pf_num_005_lbl', 'psl']].groupby(by='pf_num_005_lbl').mean().round(2),
                    piaac[['pf_num_005_lbl', 'gender_r']].groupby(by='pf_num_005_lbl').mean().round(2)-1,
                    piaac[['pf_num_005_lbl', 'age_r']].groupby(by='pf_num_005_lbl').mean().round(2)],
                    axis=1)
pf_num_005_count = pf_num_005_count.sort_index().to_latex()
pf_num_005_count = pf_num_005_count.replace('.00', '')
pf_num_005_count = pf_num_005_count.replace('{} &  pf\_num\_005\_lbl &  pf\_num\_005\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('pf_num_005_count.tex','w') as file:
    file.write(pf_num_005_count)
log_record = 'table is saved as ' + 'pf_num_005_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)


# PFP

# creating variable for pf_psl_005 labels
log_record = 'creating [pf_psl_005_lbl]: pf_psl_005 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['pf_psl_005'] == 1,
    piaac['pf_psl_005'] == 0,
    piaac['pf_psl_005'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['pf_psl_005_lbl'] = np.select(conditions, values, default=math.nan)

pf_psl_005_count = pd.concat([piaac['pf_psl_005_lbl'].value_counts(),
                    piaac['pf_psl_005_lbl'].value_counts(normalize=True).round(2),
                    piaac[['pf_psl_005_lbl', 'earn']].groupby(by='pf_psl_005_lbl').median().round(2),
                    piaac[['pf_psl_005_lbl', 'b_q01a']].groupby(by='pf_psl_005_lbl').median().round(2),
                    piaac[['pf_psl_005_lbl', 'lit']].groupby(by='pf_psl_005_lbl').mean().round(2),
                    piaac[['pf_psl_005_lbl', 'num']].groupby(by='pf_psl_005_lbl').mean().round(2),
                    piaac[['pf_psl_005_lbl', 'psl']].groupby(by='pf_psl_005_lbl').mean().round(2),
                    piaac[['pf_psl_005_lbl', 'gender_r']].groupby(by='pf_psl_005_lbl').mean().round(2)-1,
                    piaac[['pf_psl_005_lbl', 'age_r']].groupby(by='pf_psl_005_lbl').mean().round(2)],
                    axis=1)
pf_psl_005_count = pf_psl_005_count.sort_index().to_latex()
pf_psl_005_count = pf_psl_005_count.replace('.00', '')
pf_psl_005_count = pf_psl_005_count.replace('{} &  pf\_psl\_005\_lbl &  pf\_psl\_005\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('pf_psl_005_count.tex','w') as file:
    file.write(pf_psl_005_count)
log_record = 'table is saved as ' + 'pf_psl_005_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)

# ALVL

# creating variable for alv_lit_15 labels
log_record = 'creating [alv_lit_15_lbl]: alv_lit_15 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['alv_lit_15'] == 1,
    piaac['alv_lit_15'] == 0,
    piaac['alv_lit_15'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['alv_lit_15_lbl'] = np.select(conditions, values, default=math.nan)

alv_lit_15_count = pd.concat([piaac['alv_lit_15_lbl'].value_counts(),
                    piaac['alv_lit_15_lbl'].value_counts(normalize=True).round(2),
                    piaac[['alv_lit_15_lbl', 'earn']].groupby(by='alv_lit_15_lbl').median().round(2),
                    piaac[['alv_lit_15_lbl', 'b_q01a']].groupby(by='alv_lit_15_lbl').median().round(2),
                    piaac[['alv_lit_15_lbl', 'lit']].groupby(by='alv_lit_15_lbl').mean().round(2),
                    piaac[['alv_lit_15_lbl', 'num']].groupby(by='alv_lit_15_lbl').mean().round(2),
                    piaac[['alv_lit_15_lbl', 'psl']].groupby(by='alv_lit_15_lbl').mean().round(2),
                    piaac[['alv_lit_15_lbl', 'gender_r']].groupby(by='alv_lit_15_lbl').mean().round(2)-1,
                    piaac[['alv_lit_15_lbl', 'age_r']].groupby(by='alv_lit_15_lbl').mean().round(2)],
                    axis=1)
alv_lit_15_count = alv_lit_15_count.sort_index().to_latex()
alv_lit_15_count = alv_lit_15_count.replace('.00', '')
alv_lit_15_count = alv_lit_15_count.replace('{} &  alv\_lit\_15\_lbl &  alv\_lit\_15\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('alv_lit_15_count.tex','w') as file:
    file.write(alv_lit_15_count)
log_record = 'table is saved as ' + 'alv_lit_15_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)


# ALVN

# creating variable for alv_num_15 labels
log_record = 'creating [alv_num_15_lbl]: alv_num_15 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['alv_num_15'] == 1,
    piaac['alv_num_15'] == 0,
    piaac['alv_num_15'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['alv_num_15_lbl'] = np.select(conditions, values, default=math.nan)

alv_num_15_count = pd.concat([piaac['alv_num_15_lbl'].value_counts(),
                    piaac['alv_num_15_lbl'].value_counts(normalize=True).round(2),
                    piaac[['alv_num_15_lbl', 'earn']].groupby(by='alv_num_15_lbl').median().round(2),
                    piaac[['alv_num_15_lbl', 'b_q01a']].groupby(by='alv_num_15_lbl').median().round(2),
                    piaac[['alv_num_15_lbl', 'lit']].groupby(by='alv_num_15_lbl').mean().round(2),
                    piaac[['alv_num_15_lbl', 'num']].groupby(by='alv_num_15_lbl').mean().round(2),
                    piaac[['alv_num_15_lbl', 'psl']].groupby(by='alv_num_15_lbl').mean().round(2),
                    piaac[['alv_num_15_lbl', 'gender_r']].groupby(by='alv_num_15_lbl').mean().round(2)-1,
                    piaac[['alv_num_15_lbl', 'age_r']].groupby(by='alv_num_15_lbl').mean().round(2)],
                    axis=1)
alv_num_15_count = alv_num_15_count.sort_index().to_latex()
alv_num_15_count = alv_num_15_count.replace('.00', '')
alv_num_15_count = alv_num_15_count.replace('{} &  alv\_num\_15\_lbl &  alv\_num\_15\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('alv_num_15_count.tex','w') as file:
    file.write(alv_num_15_count)
log_record = 'table is saved as ' + 'alv_num_15_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)


# ALVP

# creating variable for alv_psl_15 labels
log_record = 'creating [alv_psl_15_lbl]: alv_psl_15 labels'
log_file = lm.utility.log(log_file, log_record)
conditions = [
    piaac['alv_psl_15'] == 1,
    piaac['alv_psl_15'] == 0,
    piaac['alv_psl_15'] == -1]
values = [
    'Over',
    'Well',
    'Under']
piaac['alv_psl_15_lbl'] = np.select(conditions, values, default=math.nan)

alv_psl_15_count = pd.concat([piaac['alv_psl_15_lbl'].value_counts(),
                    piaac['alv_psl_15_lbl'].value_counts(normalize=True).round(2),
                    piaac[['alv_psl_15_lbl', 'earn']].groupby(by='alv_psl_15_lbl').median().round(2),
                    piaac[['alv_psl_15_lbl', 'b_q01a']].groupby(by='alv_psl_15_lbl').median().round(2),
                    piaac[['alv_psl_15_lbl', 'lit']].groupby(by='alv_psl_15_lbl').mean().round(2),
                    piaac[['alv_psl_15_lbl', 'num']].groupby(by='alv_psl_15_lbl').mean().round(2),
                    piaac[['alv_psl_15_lbl', 'psl']].groupby(by='alv_psl_15_lbl').mean().round(2),
                    piaac[['alv_psl_15_lbl', 'gender_r']].groupby(by='alv_psl_15_lbl').mean().round(2)-1,
                    piaac[['alv_psl_15_lbl', 'age_r']].groupby(by='alv_psl_15_lbl').mean().round(2)],
                    axis=1)
alv_psl_15_count = alv_psl_15_count.sort_index().to_latex()
alv_psl_15_count = alv_psl_15_count.replace('.00', '')
alv_psl_15_count = alv_psl_15_count.replace('{} &  alv\_psl\_15\_lbl &  alv\_psl\_15\_lbl &   earn &  b\_q01a &     lit &     num &     psl &  gender\_r &  age\_r \\',
                              '{} &  N &  Frac. &  Median   & Median    & Mean &     Mean &     Mean & Mean & Mean \\\ &   &           & earnings  & qual.     & literacy  & num-y  & pr. slv. & gender & age \\')

with open('alv_psl_15_count.tex','w') as file:
    file.write(alv_psl_15_count)
log_record = 'table is saved as ' + 'pf_psl_005_count' + '.tex'
log_file = lm.utility.log(log_file, log_record)



