#temporary

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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


def shares_heatmap_slides(piaac_df, measures_list, measures_labels, cluster, feature, title, size, filename, y_labels,
                    x_labels, colorbar, numbers, nan_present):

    # close all open graphs
    plt.close('all')

    # define the x-axis by the labels of specified measures
    x = measures_labels

    # define the y-axis by the median of specified feature for specified cluster level
    y = piaac_df[[cluster, feature]].groupby(by=[cluster]).median().round(decimals=2).sort_values(feature, ascending=False).reset_index(level=0).to_numpy().tolist()
    y_new = []
    for i in y:
        y_new += [i[0]]
    y = y_new

    heatmap_data = np.empty((len(piaac_df[cluster].value_counts()), 1))
    for measure in measures_list:
        heatmap_data = np.append(heatmap_data, np.delete(np.array(
            piaac_df[[cluster, feature, measure]].groupby(by=[cluster]).median().sort_values(feature, ascending=False)),
                                                         0, 1), axis=1)
    heatmap_data = np.delete(heatmap_data, 0, 1)
    heatmap_data = np.around(heatmap_data, decimals=2)
    
    #heatmap_data = heatmap_data.T
    #x_old = x
    #y_old = y
    #x = y_old
    #y = x_old
    

    fig = plt.figure(figsize=size)
    ax = fig.subplots()
    
    if nan_present == True:
        unique_values = np.unique(heatmap_data).tolist()
        unique_values.sort()
        min_value = unique_values[1]
        im = ax.imshow(heatmap_data, cmap='Greys', vmin=min_value)
    else:
        im = ax.imshow(heatmap_data, cmap='Greys')

    # colour schemes can be found at
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html

    if colorbar == True:
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, location="left", aspect=60, pad=0.005)
        cbar.ax.tick_params(axis='y', labelsize=14, labelrotation = 90)
        cbar.ax.set_ylabel("Share", fontsize=18, rotation=90)
    else:
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, location="left", aspect=60, pad=0.005)
        cbar.ax.tick_params(axis='y', labelsize=14, labelrotation = 90)

    # Show all ticks and label them with the respective list entries
    if x_labels == True:
        ax.set_xticks(np.arange(len(x)), labels=x)
    else:
        ax.set_xticks(np.arange(len(x)), labels=[])
    
    if y_labels == True:
        ax.set_ylabel('Countries by median earnings (ascending)', fontsize=18, rotation=90)
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.set_yticks(np.arange(len(y)), labels=y)
    else:
        ax.set_yticks(np.arange(len(y)), labels=[])

    ax.tick_params(axis='y', labelsize=14, rotation=60)
    ax.tick_params(axis='x', labelsize=18)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(heatmap_data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(heatmap_data.shape[0] + 1) - .5, minor=True)
    #ax.grid(which="minor", color="w", linestyle='-')
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.yaxis.tick_right()

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", va="center", rotation_mode="anchor")
    #plt.setp(ax.get_yticklabels(), rotation=0, ha="left", va="center", rotation_mode="anchor")

    threshold = im.norm(heatmap_data.max()) / 2.
    textcolors = ("black", "white")

    # Loop over data dimensions and create text annotations.
    if numbers == True:
        for i in range(len(y)):
            for j in range(len(x)):
                text = ax.text(j, i, formatFloat("%.2f", heatmap_data[i, j]), ha="center", va="center",
                               color=textcolors[int(im.norm(heatmap_data[i, j]) > threshold)],
                               fontsize=14, rotation=0)

    ax.set_title(title, fontsize=22, rotation='horizontal', ha='center')
    fig.tight_layout()
    
    plt.savefig(filename + '.pdf', bbox_inches="tight")
    plt.show()


current_section = '2.7.2 Heatmaps: main measures (for slides)'
log_file = lm.utility.section(current_section, log_file)


titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [True, False, False]
colorbars = [False, False, True]
numbers = False
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
    shares_heatmap_slides(piaac, measures, labels, 'cntrycode', 'earn', titles[i], (8, 15), 'all_' + sharename[i] + '_by_cntrycode', y_labels[i], x_labels[i], colorbars[i], numbers, True)
    log_record = 'file is saved as ' + 'all_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = lm.utility.log(log_file, log_record)