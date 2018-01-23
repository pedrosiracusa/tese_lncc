#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 23:46:52 2018

@author: pedro
"""
from caryocar.models import SpeciesCollectorsNetwork

def run(dset,namesMap=None):
    print(\
"""
======================================
Creating the SCN model from UB dataset
--------------------------------------
""")
    dset=dset.copy()
    print(">>> Removing null entries for scientificName field...")
    dset = dset[dset['scientificName'].notnull()]
    print(">>> Removing null entries for species field...")
    dset = dset[dset['species'].notnull()]

    print(">>> Initializing SpeciesCollectorsNetwork instance...")
    scn = SpeciesCollectorsNetwork(species=dset['species'],collectors=dset['recordedBy_atomized'], namesMap=namesMap)
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
    return scn