#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paths, sys, os, datetime
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def run():
    # Configure plots
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('seaborn-paper')
    
    sns.set_color_codes('deep')
    
    customPlotParams = {
        'marker_emptyCircle':{
                'markerfacecolor':'none',
                'markeredgewidth':.6,
                'ms':7,
                'marker':'o'
                }
    }
    
    # Configure project assets and directories paths
    rootpath=os.path.normpath(r'/home/pedro/tese_lncc')
    figures_basedir = os.path.join(rootpath,r'figures/casestudy_ub/')
    tables_basedir = os.path.join(rootpath,r'tables/casestudy_ub/')
    
    occurrencesDsetPath=os.path.normpath(r'/home/pedro/datasets/ub_herbarium/occurrence.txt')
    
    ub_names_replaces_file = os.path.normpath(r'/home/pedro/caryocar/caryocar/cleaning/data/ub_collectors_replaces.json')
    ub_namesMap_file = os.path.normpath(r'/home/pedro/caryocar/caryocar/cleaning/data/ub_namesmap.json')
    
    #sys.exit()
    print( "############################################" )
    print( "############################################" )
    print( "* UB Herbarium case study")
    print( "* Author: Pedro C. de Siracusa")
    print( "* This report was generated on", str(datetime.datetime.now()) )
    print( "############################################\n\n" )
    
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
    
    print(">>> Reading data from file {} ...".format(occurrencesDsetPath))
    cols=['recordedBy','scientificName','taxonRank','kingdom','phylum','class','order','family','genus','species']
    print(">>> Removing null collector names...")
    ub_occs = pd.read_table(occurrencesDsetPath,usecols=cols,low_memory=False)
    ub_occs = ub_occs[ub_occs['recordedBy'].notnull()]
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
    print(">>> Using names replaces from file {} ...".format(ub_names_replaces_file))
    na.read_replaces(ub_names_replaces_file)
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
    print(">>> Creating names map from file {} ...".format(ub_namesMap_file))
    nm = read_NamesMap_fromJson(ub_namesMap_file,normalizationFunc=normalize)
    print(">>> Updating names map with new names...")
    nm.addNames( names=list(set(n for n,st,num in na.getCachedNames())) )
    print("""
Done creating names map 
------------------
""")
    
    
    # Create SCN
    import create_scn
    scn = create_scn.run(ub_occs,nm)

    # Create CWN
    import create_cwn
    cwn = create_cwn.run(ub_occs,nm)
    
    ######
    ######
    ## SCN 
    # Subgraphs of SCN connected components
    import scn_connected_components
    #scn_connected_components.run(scn,ub_occs)
    # Degree dist figure and table
    import scn_degree_dist
    #scn_degree_dist.run(scn,figures_basedir,tables_basedir)
    
    
    ######
    ######
    ## CWN
    # Degree dist figure
    import cwn_degree_dist
    cwn_degree_dist.run(cwn, figures_basedir=figures_basedir, customPlotParams=customPlotParams)
    
    
    


if __name__=='__main__':
    orig_stdout = sys.stdout
    f=open('report.txt','w')
    #sys.stdout=f
    
    run()
    
    #sys.stdout=orig_stdout
    f.close()
