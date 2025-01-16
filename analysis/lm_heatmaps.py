import pandas as pd
import numpy as np
import os
import sys
import importlib
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


# 1 Mismatch shares

current_section = '1.1 Shares: Job Assessment'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'ja', 'cntrycode', log_file)

current_section = '1.2 Shares: Realised Matches'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'rm_mean_05', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'rm_mean_1', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'rm_mean_15', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'rm_mode_01', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'rm_mode_1', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'rm_mode_2', 'cntrycode', log_file)

current_section = '1.3 Shares: Indirect Self Assessment'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'isa_1', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'isa_2', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'isa_3', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'isa_4', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'isa_5', 'cntrycode', log_file)

current_section = '1.4 Shares: Pellizzari-Fichen Literacy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_lit_0025', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_lit_005', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_lit_01', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_lit_0025_relaxed', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_lit_005_relaxed', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_lit_01_relaxed', 'cntrycode', log_file)

current_section = '1.5 Shares: Pellizzari-Fichen Numeracy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_num_0025', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_num_005', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_num_01', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_num_0025_relaxed', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_num_005_relaxed', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_num_01_relaxed', 'cntrycode', log_file)

current_section = '1.6 Shares: Pellizzari-Fichen Problem-Solving'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_psl_0025', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_psl_005', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_psl_01', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_psl_0025_relaxed', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_psl_005_relaxed', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'pf_psl_01_relaxed', 'cntrycode', log_file)

current_section = '1.7 Shares: Allen-Levels-van-der-Velden Literacy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_lit_1', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_lit_15', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_lit_2', 'cntrycode', log_file)

current_section = '1.8 Shares: Allen-Levels-van-der-Velden Numeracy'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_num_1', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_num_15', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_num_2', 'cntrycode', log_file)

current_section = '1.9 Shares: Allen-Levels-van-der-Velden Problem-Solving'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_psl_1', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_psl_15', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'alv_psl_2', 'cntrycode', log_file)

current_section = '1.7 Shares: Direct Self Assessment'
log_file = lm.utility.section(current_section, log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'dsa', 'cntrycode', log_file)
piaac, log_file = lm.utility.mismatch_shares(piaac, 'dsa_relaxed', 'cntrycode', log_file)

# 2 Heatmaps

current_section = '2.1 Heatmaps: Realised Matches'
log_file = lm.utility.section(current_section, log_file)

os.chdir("/Users/seva/Desktop/projects/labour_mismatch/latex/ch1_exploration/heat_maps")
log_record = 'directory is set to /Users/seva/Desktop/projects/labour_mismatch/latex/ch1_exploration/heat_maps'
log_file = lm.utility.log(log_file, log_record)

titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, True]
colorbars = [True, False, False]
numbers = True
shifts = [0.1, 0.25, 0.25]
for i in [0, 1, 2]:
    measures = ['rm_mean_05_' + sharename[i] + '_by_cntrycode',
                'rm_mean_1_' + sharename[i] + '_by_cntrycode',
                'rm_mean_15_' + sharename[i] + '_by_cntrycode',
                'rm_mode_01_' + sharename[i] + '_by_cntrycode',
                'rm_mode_1_' + sharename[i] + '_by_cntrycode',
                'rm_mode_2_' + sharename[i] + '_by_cntrycode']
    labels = ['RM, mean ± 0.5 SD',
              'RM, mean ± 1 SD',
              'RM, mean ± 1.5 SD',
              'RM, mode ± 0.1 SD',
              'RM, mode ± 1 SD',
              'RM, mode ± 2 SD']
    lm.graphs.shares_heatmap(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (10, 18), 'rm_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, True)
    log_record = 'file is saved as ' + 'rm_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)


current_section = '2.2 Heatmaps: Indirect Self Assessment'
log_file = lm.utility.section(current_section, log_file)

titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, True]
colorbars = [True, False, False]
numbers = True
shifts = [0.1, 0.25, 0.25]
for i in [0, 1, 2]:
    measures = ['isa_1_' + sharename[i] + '_by_cntrycode',
                'isa_2_' + sharename[i] + '_by_cntrycode',
                'isa_3_' + sharename[i] + '_by_cntrycode',
                'isa_4_' + sharename[i] + '_by_cntrycode',
                'isa_5_' + sharename[i] + '_by_cntrycode']
    labels = ['ISA, 1 year',
              'ISA, 2 year',
              'ISA, 3 year',
              'ISA, 4 year',
              'ISA, 5 year']
    lm.graphs.shares_heatmap(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (10, 18), 'isa_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, False)
    log_record = 'file is saved as ' + 'isa_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)


current_section = '2.4 Heatmaps: Pellizzari-Fichen'
titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, False]
colorbars = [True, True, True]
numbers = True
for i in [0, 1, 2]:
    measures = ['pf_lit_0025_' + sharename[i] + '_by_cntrycode',
                'pf_lit_005_' + sharename[i] + '_by_cntrycode',
                'pf_lit_01_' + sharename[i] + '_by_cntrycode',
                'pf_num_0025_' + sharename[i] + '_by_cntrycode',
                'pf_num_005_' + sharename[i] + '_by_cntrycode',
                'pf_num_01_' + sharename[i] + '_by_cntrycode',
                'pf_psl_0025_' + sharename[i] + '_by_cntrycode',
                'pf_psl_005_' + sharename[i] + '_by_cntrycode',
                'pf_psl_01_' + sharename[i] + '_by_cntrycode',
                'pf_lit_0025_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_lit_005_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_lit_01_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_num_0025_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_num_005_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_num_01_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_psl_0025_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_psl_005_relaxed_' + sharename[i] + '_by_cntrycode',
                'pf_psl_01_relaxed_' + sharename[i] + '_by_cntrycode',
                'alv_lit_1_' + sharename[i] + '_by_cntrycode',
                'alv_lit_15_' + sharename[i] + '_by_cntrycode',
                'alv_lit_2_' + sharename[i] + '_by_cntrycode',
                'alv_num_1_' + sharename[i] + '_by_cntrycode',
                'alv_num_15_' + sharename[i] + '_by_cntrycode',
                'alv_num_2_' + sharename[i] + '_by_cntrycode',
                'alv_psl_1_' + sharename[i] + '_by_cntrycode',
                'alv_psl_15_' + sharename[i] + '_by_cntrycode',
                'alv_psl_2_' + sharename[i] + '_by_cntrycode']
    labels = ['PF, ' + 'Literacy' + ' 5%',
              'PF, ' + 'Literacy' + ' 10%',
              'PF, ' + 'Literacy' + ' 20%',
              'PF, ' + 'Numeracy' + ' 5%',
              'PF, ' + 'Numeracy' + ' 10%',
              'PF, ' + 'Numeracy' + ' 20%',
              'PF, ' + 'Prb-Solv' + ' 5%',
              'PF, ' + 'Prb-Solv' + ' 10%',
              'PF, ' + 'Prb-Solv' + ' 20%',
              'Relaxed PF, ' + 'Literacy' + ' 5%',
              'Relaxed PF, ' + 'Literacy' + ' 10%',
              'Relaxed PF, ' + 'Literacy' + ' 20%',
              'Relaxed PF, ' + 'Numeracy' + ' 5%',
              'Relaxed PF, ' + 'Numeracy' + ' 10%',
              'Relaxed PF, ' + 'Numeracy' + ' 20%',
              'Relaxed PF, ' + 'Prb-Solv' + ' 5%',
              'Relaxed PF, ' + 'Prb-Solv' + ' 10%',
              'Relaxed PF, ' + 'Prb-Solv' + ' 20%',
              'ALV, ' + 'Literacy' + ' 1 point',
              'ALV, ' + 'Literacy' + ' 1.5 points',
              'ALV, ' + 'Literacy' + ' 2 points',
              'ALV, ' + 'Numeracy' + ' 1 point',
              'ALV, ' + 'Numeracy' + ' 1.5 points',
              'ALV, ' + 'Numeracy' + ' 2 points',
              'ALV, ' + 'Prb-Solv' + ' 1 point',
              'ALV, ' + 'Prb-Solv' + ' 1.5 points',
              'ALV, ' + 'Prb-Solv' + ' 2 points']
    lm.graphs.shares_heatmap(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (17, 16), 'pf_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, True)
    log_record = 'file is saved as ' + 'pf_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)
    
current_section = '2.6 Heatmaps: Direct Self Assessment'
log_file = lm.utility.section(current_section, log_file)

titles = ['Under', 'Well', 'DP Error', 'Over']
sharename = ['undershare', 'wellshare', 'errorshare', 'overshare']
x_labels = [True, True, True, True]
y_labels = [False, False, False, True]
colorbars = [True, False, False, False]
numbers = True
for i in [0, 1, 2, 3]:
    measures = ['dsa_' + sharename[i] + '_by_cntrycode']
    labels = ['DSA']
    lm.graphs.shares_heatmap(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (10, 18), 'dsa_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, False)
    log_record = 'file is saved as ' + 'dsa_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)
    
titles = ['Under', 'Well', 'Over']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, True]
colorbars = [True, False, False]
numbers = True
for i in [0, 1, 2]:
    measures = ['dsa_relaxed_' + sharename[i] + '_by_cntrycode']
    labels = ['Relaxed DSA']
    lm.graphs.shares_heatmap(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (10, 19.1), 'dsar_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, False)
    log_record = 'file is saved as ' + 'dsar_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)


current_section = '2.7 Heatmaps: main measures'
log_file = lm.utility.section(current_section, log_file)

titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, True]
colorbars = [True, False, False]
numbers = True
for i in [0, 1, 2]:
    measures = ['ja_' + sharename[i] + '_by_cntrycode',
                'rm_mode_1_' + sharename[i] + '_by_cntrycode',
                'isa_1_' + sharename[i] + '_by_cntrycode',
                'pf_lit_005_' + sharename[i] + '_by_cntrycode',
                'pf_num_005_' + sharename[i] + '_by_cntrycode',
                'pf_psl_005_' + sharename[i] + '_by_cntrycode',
                'alv_lit_15_' + sharename[i] + '_by_cntrycode',
                'alv_num_15_' + sharename[i] + '_by_cntrycode',
                'alv_psl_15_' + sharename[i] + '_by_cntrycode'
                ]
    labels = ['Job Analysis',
              'Realized Matches',
              'Indirect Self-Assessment',
              'PF Literacy',
              'PF Numeracy',
              'PF Problem-Solving',
              'ALV Literacy',
              'ALV Numeracy',
              'ALV Problem-Solving'
              ]
    lm.graphs.shares_heatmap(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (8, 15), 'all_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, True)
    log_record = 'file is saved as ' + 'all_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)

current_section = '2.7.2 Heatmaps: main measures (for slides)'
log_file = lm.utility.section(current_section, log_file)

titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, True]
colorbars = [True, False, False]
numbers = True
for i in [0, 1, 2]:
    measures = ['ja_' + sharename[i] + '_by_cntrycode',
                'rm_mode_1_' + sharename[i] + '_by_cntrycode',
                'isa_1_' + sharename[i] + '_by_cntrycode',
                'pf_lit_005_' + sharename[i] + '_by_cntrycode',
                'pf_num_005_' + sharename[i] + '_by_cntrycode',
                'pf_psl_005_' + sharename[i] + '_by_cntrycode',
                'alv_lit_15_' + sharename[i] + '_by_cntrycode',
                'alv_num_15_' + sharename[i] + '_by_cntrycode',
                'alv_psl_15_' + sharename[i] + '_by_cntrycode'
                ]
    labels = ['Job Analysis',
              'Realized Matches',
              'Indirect Self-Assessment',
              'PF Literacy',
              'PF Numeracy',
              'PF Problem-Solving',
              'ALV Literacy',
              'ALV Numeracy',
              'ALV Problem-Solving'
              ]
    lm.graphs.shares_heatmap_slides(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (8, 15), 'all_' + sharename[i] + '_by_cntrycode_slides', y_labels[i], x_labels[i], colorbars[i], numbers, True)
    log_record = 'file is saved as ' + 'all_' + sharename[i] + '_by_cntrycode_slides' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)

current_section = '2.8 Heatmaps: correlation analysis'
log_file = lm.utility.section(current_section, log_file)

measures = ['ja',
            'rm_mode_1',
            'isa_1',
            'pf_lit_005',
            'pf_lit_005_relaxed',
            'alv_lit_15',
            'pf_num_005',
            'pf_num_005_relaxed',
            'alv_num_15',
            'pf_psl_005',
            'pf_psl_005_relaxed',
            'alv_psl_15',
            'dsa',
            'dsa_relaxed']
piaac, log_file = lm.utility.mismatch_split(piaac, measures, log_file)

labels = ['Job Analysis',
          'Realized Matches',
          'Indirect Self-Assessment',
          'PF Literacy',
          'PF Numeracy',
          'PF Problem-Solving',
          'Rel. PF Literacy',
          'Rel. PF Numeracy',
          'Rel. PF Problem-Solving',
          'ALV Literacy',
          'ALV Numeracy',
          'ALV Problem-Solving',
          'Direct Self-Assessment',
          'Rel. Direct Self-Assessment']

measures = ['ja_o',
            'rm_mode_1_o',
            'isa_1_o',
            'pf_lit_005_o',
            'pf_num_005_o',
            'pf_psl_005_o',
            'pf_lit_005_relaxed_o',
            'pf_num_005_relaxed_o',
            'pf_psl_005_relaxed_o',
            'alv_lit_15_o',
            'alv_num_15_o',
            'alv_psl_15_o',
            'dsa_o',
            'dsa_relaxed_o']


lm.graphs.corr_heat_map(piaac, 'matthews', measures, labels, 'all', "Over-Matched", (11, 10), 'mcc_all_o', False, True)
log_record = 'file is saved as ' + 'mcc_all_o' + '.pdf'
log_file = lm.utility.log(log_file, log_record)

"""
lm.graphs.corr_heat_map(piaac, 'pearson', measures, labels, 'all', "Over-Matched", (11, 11), 'corr_all_o', True)
log_record = 'file is saved as ' + 'corr_all_o' + '.pdf'
log_file = lm.utility.log(log_file, log_record)
"""

measures = ['ja_w',
            'rm_mode_1_w',
            'isa_1_w',
            'pf_lit_005_w',
            'pf_num_005_w',
            'pf_psl_005_w',
            'pf_lit_005_relaxed_w',
            'pf_num_005_relaxed_w',
            'pf_psl_005_relaxed_w',
            'alv_lit_15_w',
            'alv_num_15_w',
            'alv_psl_15_w',
            'dsa_w',
            'dsa_relaxed_w']

lm.graphs.corr_heat_map(piaac, 'matthews', measures, labels, 'all', "Well-Matched", (11, 10), 'mcc_all_w', False, True)
log_record = 'file is saved as ' + 'mcc_all_w' + '.pdf'
log_file = lm.utility.log(log_file, log_record)

"""
lm.graphs.corr_heat_map(piaac, 'pearson', measures, labels, 'all', "Well-Matched", (11, 11), 'corr_all_w', True, True)
log_record = 'file is saved as ' + 'corr_all_w' + '.pdf'
log_file = lm.utility.log(log_file, log_record)
"""

measures = ['ja_u',
            'rm_mode_1_u',
            'isa_1_u',
            'pf_lit_005_u',
            'pf_num_005_u',
            'pf_psl_005_u',
            'pf_lit_005_relaxed_u',
            'pf_num_005_relaxed_u',
            'pf_psl_005_relaxed_u',
            'alv_lit_15_u',
            'alv_num_15_u',
            'alv_psl_15_u',
            'dsa_u',
            'dsa_relaxed_u']


lm.graphs.corr_heat_map(piaac, 'matthews', measures, labels, 'all', "Under-Matched", (11, 11), 'mcc_all_u', True, True)
log_record = 'file is saved as ' + 'mcc_all_u' + '.pdf'
log_file = lm.utility.log(log_file, log_record)

"""
lm.graphs.corr_heat_map(piaac, 'pearson', measures, labels, 'all', "Under-Matched", (11, 11), 'corr_all_u', True, True)
log_record = 'file is saved as ' + 'corr_all_u' + '.pdf'
log_file = lm.utility.log(log_file, log_record)
""" 


"""
under_est = {'ja': [0.193, 0.083, 1.717],
             'rm': [0.184, 0.100, 1.106],
             'isa': [0, 0, 0],
             'pfl': [-0.139, -0.035, -2.983],
             'pfn': [-0.138, -0.059, -2.469],
             'pfp': [-0.271, -0.053, -2.030]}
under_est = pd.DataFrame(data=under_est)

over_est = {'ja': [-0.086, -0.073, 0],
             'rm': [0.151, 0.020, 1.707],
             'isa': [-0.186, -0.116, -0.908],
             'pfl': [-0.066, 0.084, -1.140],
             'pfn': [-0.073, 0.106, -1.226],
             'pfp': [-0.165, 0, -0.798]}
over_est = pd.DataFrame(data=over_est)

lm.graphs.estimates_heat_map(under_est, ['ja', 'rm', 'isa', 'pfl', 'pfn', 'pfp'], ['pols', 'fe', 'be'], "", (10,10), 'estimates_u_hm')
lm.graphs.estimates_heat_map(over_est, ['ja', 'rm', 'isa', 'pfl', 'pfn', 'pfp'], ['pols', 'fe', 'be'], "", (10,10), 'estimates_u_hm')
"""

    
    