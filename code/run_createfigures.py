#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:10:11 2018

@author: pedro
"""

# This script creates thesis figures

import paths, sys, os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plots
mpl.rcParams.update(mpl.rcParamsDefault)
plt.style.use('seaborn-paper')

sns.set_color_codes('deep')



#sys.exit()

################
## UB Case Study
## -------------

# Load UB dataset
print("Loading the UB dataset")
dsetPath = '/home/pedro/datasets/ub_herbarium/occurrence.txt'
cols=['recordedBy','scientificName','taxonRank','kingdom','phylum','class','order','family','genus','species']
ub_occs = pd.read_table(dsetPath,usecols=cols,low_memory=False)
ub_occs = ub_occs[ub_occs['recordedBy'].notnull()]
ub_occs = ub_occs[ub_occs['scientificName'].notnull()]
ub_occs = ub_occs[ub_occs['species'].notnull()]

# Get names map
print("Creating names map")
from caryocar.cleaning import read_NamesMap_fromJson
ub_namesMap_file = '/home/pedro/caryocar/caryocar/cleaning_data/ub_namesmap.json'
nm = read_NamesMap_fromJson(ub_namesMap_file,normalizationFunc=None)

# Get names atomizer
print("Creating names atomizer")
from caryocar.cleaning import NamesAtomizer,namesFromString
na = NamesAtomizer(atomizeOp=namesFromString)
names_replaces_file = '/home/pedro/caryocar/caryocar/cleaning_data/ub_collectors_replaces.json'
na.read_replaces(names_replaces_file)

# Create SCN
print("Creating a SCN")
from caryocar.models import SpeciesCollectorsNetwork
ub_occs['recordedBy_atomized']=na.atomize(ub_occs['recordedBy'])
scn = SpeciesCollectorsNetwork(species=ub_occs['species'],collectors=ub_occs['recordedBy_atomized'])
# Create SCN


import ub_casestudy.cwn_degree_dist
print("Plotting CWN degree distributions")
ub_casestudy.cwn_degree_dist.plotfigure(scn)