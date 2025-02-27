"""
Labour Mismatch Toolbox for PIAAC

This package provides a set of functions designed to compute education 
and skill mismatch using data from the 1st Cycle of the Survey of Adult 
Skills (PIAAC). The currently available measures include job analysis, 
realised matches, indirect self-assessment, direct self-assessment, 
Pellizzari-Fichen [3], and Allen-Levels-Van-der-Velden [1].For the description 
of the measures, please refer to Section 3: Labour Mismatch Measurement 
Frameworks in [2].

Modules
--------

utilities
    A set of functions for data processing and analysis.
    last update: 22/01/2025

clean
    A set of functions for data cleaning.
    last update: 23/01/2025

isco
    Clean existing and create additional occupation and education variables based on ISCO-08.
    last update: 23/01/2025

 em
    Functions computing education mismatch measures.
    last update: 24/01/2025   

sm
    Functions computing skill mismatch measures.
    last update: 27/02/2025

graphs
    Labour mismatch data visualisation functions.
    last update: 27/02/2025

References
----------

[1] Allen, J. P., Levels, M., & Van der Velden, R. K. W. (2013). 
    Skill mismatch and skill use in developed countries: Evidence from the PIAAC study.

[2] Iakovlev, V. (2024). Skill vs. education types of labour mismatch and their association 
    with earnings (No. 2024-12). Accountancy, Economics, and Finance Working Papers.

[3] Pellizzari, M., & Fichen, A. (2017). A new measure of skill mismatch: theory and 
    evidence from PIAAC. IZA Journal of Labor Economics, 6, 1-30.

author: Vsevolod Iakovlev
email: vsevolod.v.iakovlev@gmail.com
"""

from .src import (
    clean,
    em,
    isco,
    sm,
    utilities,
    graphs
)
