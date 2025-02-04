# Labout Mismatch Toolbox for PIAAC

[Usage](#usage) | [Codebook](#codebook) | [Example](#example) | [Meet Bruce!](#meet-bruce-labour-mismatch-measures-101) | [References](#references)

![figure](./figures/toolbox_logo.png)

This package provides a set of functions designed to compute education 
and skill mismatch using data from the 1st Cycle of the Survey of Adult 
Skills (PIAAC). The currently available measures include job analysis, 
realised matches, indirect self-assessment, direct self-assessment, 
Pellizzari-Fichen, and Allen-Levels-Van-der-Velden. For the desription 
of the measures, please refer to Section 3: Labour Mismatch Measurement 
Frameworks in [1].

## Usage

1. Create a new directory with the input data make it your working directory
2. Clone the repository to that directory
3. Make sure the following packages are installed: ``matplotlib``, `numpy` ``pandas``, ``scikit-learn``, ``seaborn``, ``statistics``, ``tabulate``:
```python
pip install matplotlib numpy pandas scikit-learn seaborn statistics tabulate
```
4. Import the package:
```python
import mismatch_toolbox as mt
```
5. Type ``help(mt)`` to view the packages's description and available modules.

## Codebook

[International](https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/piaac/data-materials/International-Codebook-PIAAC-Public-use-File-Variables-and-Values_Feb2023.xlsx) and [derived variables](https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/piaac/data-materials/Codebook-for-derived-Variables-16March2015.docx) [cedobooks](https://www.oecd.org/en/data/datasets/piaac-1st-cycle-database.html#codebooks) are available at the PIAAC [website](https://www.oecd.org/en/about/programmes/piaac/piaac-data.html).

## Example

1. Import the packages:

```python
import pandas as pd
import os
import sys

sys.path.insert(0, '/Users/bruce/example_directory_with_the_package')
import mismatch_toolbox as mt
```

2. Load and preprocess the data:

```python
# Preliminaries
sec_name = ""
log_file = pd.DataFrame(columns=['index', 'section', 'record'])

# PIAAC Data
sec_name = 'Load PIAAC Data'
log_file = mt.utilities.section(sec_name, log_file)

# set the directory
os.chdir('/Users/bruce/example_directory_with_the_package')
log_record = 'directory is set to /Users/bruce/example_directory_with_the_package'
log_file = mt.utilities.log(log_file, log_record)

# load PIAAC dataset
log_record = 'loading piaac dataset, please wait'
log_file = mt.utilities.log(log_file, log_record)
piaac = pd.read_csv('/Users/bruce/example_directory_with_piaac_data/piaac.csv', low_memory=False)

# Preparation
sec_name = 'Preparations'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.clean.preparation(piaac, log_file)

# ISCO-08 skill level
sec_name = 'ISCO-08 skill level'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.isco.education(piaac, log_file)

# ISCO-08 occupation groups
sec_name = 'ISCO-08 occupation groups'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.isco.occupations(piaac, log_file)

```

Output:

```
Load PIAAC Data
---------------------------------------------

log[1] directory is set to /Users/seva/Desktop/projects/labour_mismatch/code/python/test
log[2] loading piaac dataset, please wait

Preparations
---------------------------------------------

log[4] converting cntryid to float
log[5] creating [cntryname]: variable for country names
log[6] creating [cntrycode]: variable for country codes
log[7] check and drop for missing values in country ID
log[8] no observations have the value of nan for [cntryid]
log[9] n=227031
log[10] converting [c_d05] (employment status) to float
log[11] drop all respondents who are unemployed or out of the labour force
log[12] n=227031
log[13] dropping observations with [c_d05]!=[1]
log[14] n=150650; 76381 observations have been removed
log[15] creating [earn]: variable earn as a float of an earnings variable of choice
log[16] check and drop for missing values in earnings
log[17] 73937 observations have the value of nan for [earn]
log[18] n=150650
log[19] removing the observations...
log[20] no observations have the value of nan for [earn]
log[21] n=76713; 73937 observations have been removed
log[22] trim earningns at the 1st and 99th percentiles
log[23] n=75188

ISCO-08 skill level
---------------------------------------------

log[25] converting ISCED level to a float
log[26] missing values cleaning skipped for b_q01a
log[27] 4038 observations have the value of nan for b_q01a
log[28] creating a variable for obtained ISCO-08 skill level
log[29] print table of ISCED - skill level mapping

+----------+-------+-------+-------+-------+-------+
| b_q01a   |   1.0 |   2.0 |   3.0 |   4.0 |   All |
|----------+-------+-------+-------+-------+-------|
| 1.0      |  1011 |     0 |     0 |     0 |  1011 |
| 2.0      |     0 |  2101 |     0 |     0 |  2101 |
| 3.0      |     0 |  7418 |     0 |     0 |  7418 |
| 4.0      |     0 |  1681 |     0 |     0 |  1681 |
| 5.0      |     0 |  8974 |     0 |     0 |  8974 |
| 6.0      |     0 | 14414 |     0 |     0 | 14414 |
| 7.0      |     0 |  3607 |     0 |     0 |  3607 |
| 8.0      |     0 |  1306 |     0 |     0 |  1306 |
| 9.0      |     0 |  1266 |     0 |     0 |  1266 |
| 10.0     |     0 |   842 |     0 |     0 |   842 |
| 11.0     |     0 |     0 |  8493 |     0 |  8493 |
| 12.0     |     0 |     0 |     0 | 10351 | 10351 |
| 13.0     |     0 |     0 |     0 |  6950 |  6950 |
| 14.0     |     0 |     0 |     0 |   629 |   629 |
| 15.0     |     0 |     0 |     0 |   565 |   565 |
| 16.0     |     0 |     0 |     0 |  1542 |  1542 |
| All      |  1011 | 41609 |  8493 | 20037 | 71150 |
+----------+-------+-------+-------+-------+-------+
log[30] converting isco08_sl_o to float
log[31] missing values cleaning skipped for isco08_sl_o
log[32] 4038 observations have the value of nan for isco08_sl_o
log[33] convert b_q01c2 (year of finish) to float
log[34] creating a variable for the year when higher education decision was supposedly made
log[35] creating a variable for country specific decision year bins

ISCO-08 occupation groups
---------------------------------------------

log[37] converting isco1c, isco2c, isco1l and isco2l to float
log[38] check and drop for 1-digit occupation groups
log[39] 18 observations have the value of nan for [isco1c]
log[40] n=75188
log[41] removing the observations...
log[42] no observations have the value of nan for [isco1c]
log[43] n=75170; 18 observations have been removed
log[44] check and drop for 2-digit occupation groups
log[45] no observations have the value of nan for [isco2c]
log[46] n=75170
log[47] dropping observations for which isco1c is encoded as missing (9995, 9996, 9997, 9998, 9999)
log[48] n=75170
log[49] dropping observations with [isco1c]==[9995, 9996, 9997, 9998, 9999]
log[50] n=74445; 725 observations have been removed
log[51] creating occupation group label variable for 1-digit groups
log[52] creating occupation group label variable for 2-digit groups
log[53] creating major custom occupation groups based on ISCO-08 required skill level
log[54] check and drop for custom occupation groups
log[55] 493 observations have the value of nan for [isco_lbl]
log[56] n=74445
log[57] removing the observations...
log[58] dropping armed orces due to small sample
log[59] n=73952
log[60] dropping observations with [isco2c]==[1, 2, 3]
log[61] n=73675; 277 observations have been removed
log[62] creating variables for country-specific occupation groups
log[63] dropping occupations groups with n<30
log[64] n=73675
log[65] dropping observations with [cntry_isco_lbl]==['RUS Low skilled managers', 'RUS Skilled agricultural, forestry and fishery workers', 'JPN Low skilled managers', 'JPN Skilled agricultural, forestry and fishery workers', 'CHL Low skilled managers', 'GRC High skilled managers', 'GRC Low skilled managers', 'GRC Skilled agricultural, forestry and fishery workers', 'KAZ Skilled agricultural, forestry and fishery workers', 'ESP Low skilled managers', 'IRL Skilled agricultural, forestry and fishery workers', 'ECU High skilled managers', 'ECU Low skilled managers', 'NLD Skilled agricultural, forestry and fishery workers', 'NOR Low skilled managers', 'NOR Skilled agricultural, forestry and fishery workers', 'POL Skilled agricultural, forestry and fishery workers', 'ISR Skilled agricultural, forestry and fishery workers', 'ITA High skilled managers', 'ITA Skilled agricultural, forestry and fishery workers', 'ITA Low skilled managers', 'KOR Low skilled managers', 'KOR Skilled agricultural, forestry and fishery workers', 'SVN Skilled agricultural, forestry and fishery workers', 'SVN Low skilled managers', 'BEL Low skilled managers', 'BEL Skilled agricultural, forestry and fishery workers', 'MEX Low skilled managers', 'SVK Low skilled managers', 'SVK Skilled agricultural, forestry and fishery workers', 'LTU Low skilled managers', 'LTU Skilled agricultural, forestry and fishery workers', 'CZE Skilled agricultural, forestry and fishery workers', 'GBR Skilled agricultural, forestry and fishery workers']
log[66] n=73135; 540 observations have been removed
```

3. Compute 3 mismatch measures:

```python
# Realised Matches - mode
sec_name = 'Realised Matches - mode'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.em.rm_mode(piaac_df = piaac, 
                                SDs = 1, 
                                log_df = log_file)

# Indirect Self-Assessment
sec_name = 'Indirect Self-Assessment'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.em.isa(piaac_df = piaac, 
                            gap = 1, 
                            log_df = log_file)

# Pellizzari-Fichen Numeracy
sec_name = 'Pellizzari-Fichen Numeracy'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.sm.dsa(piaac_df = piaac,
                            log_df = log_file)

piaac, log_file = mt.sm.pf(piaac_df = piaac, 
                           skill_var = 'num', 
                           precision = 0.05, 
                           dsa_relaxed = False, 
                           log_df = log_file)
```

Output:

```
Realised Matches - mode
---------------------------------------------

log[68] defining function calculating skill level mode and standard deviation
log[69] calculating country-specific skill level mode and standard deviation
log[70] creating [rm_mode_1]: variable for country-spec mode-based RM mismatch with 1 SDs threshold
log[71] missing values cleaning skipped for [rm_mode_1]
log[72] 3698 observations have the value of nan for rm_mode_1

Indirect Self-Assessment
---------------------------------------------

log[74] converting self-reported requirement to float
log[75] converting years of education to float
log[76] creating [isa_1]: variable for ISA mismatch
log[77] missing values cleaning skipped for [isa_1]
log[78] 2089 observations have the value of nan for isa_1

Pellizzari-Fichen Numeracy
---------------------------------------------

log[80] converting [f_q07a] to float
log[81] check and drop for missing values in [f_q07a]
log[82] 519 observations have the value of nan for [f_q07a]
log[83] n=73135
log[84] removing the observations...
log[85] no observations have the value of nan for [f_q07a]
log[86] n=72616; 519 observations have been removed
log[87] creating variable for being not challenged enough
log[88] converting [f_q07b] to float
log[89] check and drop for missing values in [f_q07b]
log[90] 53 observations have the value of nan for [f_q07b]
log[91] n=72616
log[92] removing the observations...
log[93] no observations have the value of nan for [f_q07b]
log[94] n=72563; 53 observations have been removed
log[95] creating variable for feeling need in training
log[96] creating [dsa]: variable for DSA skill mismatch
log[97] creating [dsa_relaxed]: variable for "relaxed" DSA skill mismatch
log[98] missing values cleaning skipped for [dsa]
log[99] 0 observations have the value of nan for dsa
log[100] missing values cleaning skipped for [dsa_relaxed]
log[101] 0 observations have the value of nan for dsa_relaxed
log[102] creating [num]: variable for the average of literacy plausible values
log[103] converting [num] to float
log[104] missing values cleaning skipped for [num]
log[105] 2 observations have the value of nan for [num]
log[106] creating [num] skill mismatch thresholds, [dsa_relaxed] = False
log[107] creating [dsa_num_min]: cntry_isco_lbl-specific thresholds at 0.05 and 0.95 percentiles
log[108] missing values cleaning skipped for [dsa_num_max]
log[109] 40 observations have the value of nan for dsa_num_max
log[110] missing values cleaning skipped for [dsa_num_min]
log[111] 40 observations have the value of nan for dsa_num_min
log[112] creating [pf_num_005]: variable for literacy skill mismatch
log[113] missing values cleaning skipped for [pf_num_005]
log[114] 42 observations have the value of nan for [pf_num_005]
```

4. Calculate mismatch shares across countries:

```python
# Shares: Realised Matches
sec_name = 'Shares: Realised Matches'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.utilities.mismatch_shares(piaac_df = piaac, 
                                               mismatch_variable = 'rm_mode_1', 
                                               feature = 'cntrycode', 
                                               log_df = log_file)

# Shares: Indirect Self-Assessment
sec_name = 'Shares: Indirect Self-Assessment'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.utilities.mismatch_shares(piaac_df = piaac, 
                                               mismatch_variable = 'isa_1', 
                                               feature = 'cntrycode', 
                                               log_df = log_file)

# Shares: Pellizzari-Fichen Numeracy
sec_name = 'Shares: Pellizzari-Fichen Numeracy'
log_file = mt.utilities.section(sec_name, log_file)
piaac, log_file = mt.utilities.mismatch_shares(piaac_df = piaac, 
                                               mismatch_variable = 'pf_num_005', 
                                               feature = 'cntrycode', 
                                               log_df = log_file)
```

Output:

```
Shares: Realised Matches
---------------------------------------------

log[116] creating mismatch shares for [rm_mode_1] across [cntrycode]
log[117] [rm_mode_1_wellshare_by_cntrycode] created
log[118] [rm_mode_1_overshare_by_cntrycode] created
log[119] [rm_mode_1_undershare_by_cntrycode] created

Shares: Indirect Self-Assessment
---------------------------------------------

log[121] creating mismatch shares for [isa_1] across [cntrycode]
log[122] [isa_1_wellshare_by_cntrycode] created
log[123] [isa_1_overshare_by_cntrycode] created
log[124] [isa_1_undershare_by_cntrycode] created

Shares: Pellizzari-Fichen Numeracy
---------------------------------------------

log[126] creating mismatch shares for [pf_num_005] across [cntrycode]
log[127] [pf_num_005_wellshare_by_cntrycode] created
log[128] [pf_num_005_overshare_by_cntrycode] created
log[129] [pf_num_005_undershare_by_cntrycode] created
```

5. Plot shares heatmap:

```python
# Mismatch Shares Heatmap
sec_name = 'Mismatch Shares Heatmap'
log_file = mt.utilities.section(sec_name, log_file)

titles = ['Under-Matched', 'Well-Matched', 'Over-Matched']
sharename = ['undershare', 'wellshare', 'overshare']
x_labels = [True, True, True]
y_labels = [False, False, True]

for i in [0, 1, 2]:
    
    measures = ['rm_mode_1_' + sharename[i] + '_by_cntrycode',
                'isa_1_' + sharename[i] + '_by_cntrycode',
                'pf_num_005_' + sharename[i] + '_by_cntrycode']
    
    labels = ['Realized Matches',
              'Indirect Self-Assessment',
              'Pellizzari-Fichen Numeracy']
    
    mt.graphs.shares_heatmap(piaac_df = piaac, 
                             measures_list = measures, 
                             measures_labels = labels, 
                             cluster = 'cntrycode', 
                             feature = 'earn', 
                             title = titles[i],                             
                             y_labels = y_labels[i], 
                             x_labels = x_labels[i], 
                             colorbar = True, 
                             numbers = True, 
                             nan_present = True,
                             size = (3, 15),
                             vertical = True, 
                             filename = 'test_' + sharename[i] + '_by_cntrycode', 
                             display = True,
                             save = True)
    
    log_record = 'file is saved as ' + 'test_' + sharename[i] + '_by_cntrycode' + '.pdf'
    log_file = mt.utilities.log(log_file, log_record)
```

Output:

```
Mismatch Shares Heatmap
---------------------------------------------
log[131] file is saved as test_undershare_by_cntrycode.pdf
log[132] file is saved as test_wellshare_by_cntrycode.pdf
log[133] file is saved as test_overshare_by_cntrycode.pdf
```

<img src="./figures/test_undershare_by_cntrycode.png"> <img src="./figures/test_wellshare_by_cntrycode.png"> <img src="./figures/test_overshare_by_cntrycode.png">

6. Plot correlation heatmap:

```python
# Correlation Heatmap
sec_name = 'Correlation Heatmap'
log_file = mt.utilities.section(sec_name, log_file)

measures = ['rm_mode_1',
            'isa_1',
            'pf_num_005']

mt.graphs.corr_heat_map(piaac_df = piaac, 
                        corr_type = 'matthews', 
                        measures_list = measures, 
                        measures_labels = labels, 
                        country = 'all', 
                        title = "Well-Matched",                     
                        x_labels = True, 
                        y_labels = True,
                        size = (5, 5), 
                        filename = 'mcc_test_w',
                        display = True,
                        save = True)
                        
log_record = 'file is saved as ' + 'mcc_test_w' + '.pdf'
log_file = mt.utilities.log(log_file, log_record)
```

Output:

```
Correlation Heatmap
---------------------------------------------
log_file = mt.utilities.section(sec_name, log_file)
```

<img src="./figures/mcc_test_w.png">

## Meet Bruce: labour mismatch measures 101 

The following graphs are designed to communicate the intuition behind some of the mismatch measures that are supported by the package.

<img src="./bruce/bruce_ja.png" width="700">
 
<img src="./bruce/bruce_rm.png" width="700">

<img src="./bruce/bruce_isa.png" width="700">

<img src="./bruce/bruce_pf.png" width="700">

<img src="./bruce/bruce_alv.png" width="700">

## References
