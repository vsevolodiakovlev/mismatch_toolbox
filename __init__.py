"""
Labout Mismatch Toolbox for PIAAC

This package provides a set of functions designed to compute education 
and skill mismatch using data from the 1st Cycle of the Survey of Adult 
Skills (PIAAC). The currently available measures include job analysis, 
realised matches, indirect self-assessment, direct self-assessment, 
Pellizzari-Fichen, and Allen-Levels-Van-der-Velden.For the description 
of the measures, please refer to Section 3: Labour Mismatch Measurement 
Frameworks in [1].

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
    last update: 24/01/2025

References
----------

[1] Iakovlev, V. (2024). Skill vs. education types of labour mismatch and 
    their association with earnings (No. 2024-12). Accountancy, Economics, 
    and Finance Working Papers.

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
