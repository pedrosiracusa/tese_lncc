#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:10:11 2018

@author: pedro
"""

# This script creates thesis figures

import paths, sys, os
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plots
mpl.rcParams.update(mpl.rcParamsDefault)
plt.style.use('seaborn-paper')

sns.set_color_codes('deep')

# Configure project dirs
figures_basedir = os.path.abspath('../figures/')
tables_basedir = os.path.abspath('../tables/')

#sys.exit()

################
## UB Case Study
## -------------

# Load UB dataset
print(\
"""
======================
Loading the UB dataset
----------------------
""")
dsetPath = '/home/pedro/datasets/ub_herbarium/occurrence.txt'
print(">>> Reading data from file {} ...".format(dsetPath))
cols=['recordedBy','scientificName','taxonRank','kingdom','phylum','class','order','family','genus','species']
print(">>> Removing null values...")
ub_occs = pd.read_table(dsetPath,usecols=cols,low_memory=False)
ub_occs = ub_occs[ub_occs['recordedBy'].notnull()]
ub_occs = ub_occs[ub_occs['scientificName'].notnull()]
ub_occs = ub_occs[ub_occs['species'].notnull()]
print("""
Done loading the ub dataset 
----------------------

""")


# Create names atomizer
print(\
"""
=======================
Creating Names Atomizer
-----------------------
""")
from caryocar.cleaning import NamesAtomizer,namesFromString
na = NamesAtomizer(atomizeOp=namesFromString)
names_replaces_file = '/home/pedro/caryocar/caryocar/cleaning/data/ub_collectors_replaces.json'
print(">>> Using names replaces from file {} ...".format(names_replaces_file))
na.read_replaces(names_replaces_file)
print(">>> Creating an atomized collectors column...")
ub_occs['recordedBy_atomized']=na.atomize(ub_occs['recordedBy'])
print("""
Done creating names atomizer 
-----------------------
""")


# Get names map
print(\
"""
==================
Creating Names Map
------------------
""")
from caryocar.cleaning import normalize, read_NamesMap_fromJson
ub_namesMap_file = '/home/pedro/caryocar/caryocar/cleaning/data/ub_namesmap.json'
print(">>> Creating names map from file {} ...".format(ub_namesMap_file))
nm = read_NamesMap_fromJson(ub_namesMap_file,normalizationFunc=normalize)
print(">>> Updating names map with new names...")
nm.addNames( names=list(set(n for n,st,num in na.getCachedNames())) )
print("""
Done creating names map 
------------------
""")


# Create SCN
print(\
"""
======================================
Creating the SCN model from UB dataset
--------------------------------------
""")
from caryocar.models import SpeciesCollectorsNetwork
print(">>> Initializing SpeciesCollectorsNetwork instance...")
scn = SpeciesCollectorsNetwork(species=ub_occs['species'],collectors=ub_occs['recordedBy_atomized'], namesMap=nm)
nodes_to_filter = ['','ignorado','ilegivel','incognito','etal']
print(">>> Filtering out nodes from {}".format(nodes_to_filter))
scn.remove_nodes_from(nodes_to_filter)
print(">>> The SCN model was created. Here's some info:")
print("    * Number of S_col nodes:",len(scn.listCollectorsNodes()) )
print("    * Number of S_sp nodes:", len(scn.listSpeciesNodes()) )
print("    * Number of edges:",len(scn.edges) )
print("""
Done creating the SCN model
--------------------------------------
""")

# Plot figures
print(\
"""
=================================
Plotting SCN degree distributions
---------------------------------
""")
import ub_casestudy.scn_degree_dist
print(">>> using module {}".format(ub_casestudy.scn_degree_dist.__name__))
ub_casestudy.scn_degree_dist.plotfigures(scn,figures_basedir)
print("""
Done plotting SCN degree distributions
---------------------------------
""")


# Data
print(\
"""
======================
Outputting data report
----------------------
""")
data = ub_casestudy.scn_degree_dist.getReport(scn)

for k,v in data.items():
    print('{}: {}'.format(k,v))
print("""
Done outputting data report
----------------------
""")


# Latex tables
print(\
"""
=================================
Outputting LaTeX-formatted tables
---------------------------------
""")
tables = ub_casestudy.scn_degree_dist.createLatexTables(scn)
for tname,table in tables:
    print(">>> Printing table {}:\n".format(tname))
    print(table+'\n')
    
print(">>> Saving LaTeX tables...")
for i,(tname,table) in enumerate(tables):
    fpath = os.path.join(tables_basedir,"casestudy_ub/"+tname+".tex")
    with open(fpath,'w+') as f:
        f.write(table)
        print(">>> Saved table: {}\n".format(tname))


print("""
Done outputting LaTeX tables
---------------------------------
""")


