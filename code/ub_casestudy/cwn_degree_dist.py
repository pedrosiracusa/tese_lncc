
import os
import powerlaw
import networkx as nx
import matplotlib.pyplot as plt

def plotFigures(cwn, **kwargs):
    
    ###############
    ## CWN degree dist
    print(">>> Plotting CWN degree distribution")
    
    # Get histogram
    k_hist = nx.degree_histogram(cwn)
    sum_degrees = sum(k_hist)
    h = list(zip( range(len(k_hist)), k_hist ))
    h_pct = [ (k,cnt/sum_degrees) for k,cnt in h ]
    
    # Fit powerlaw
    data_expanded=[ k for k,cnt in h for i in range(cnt) if k>0 ] 
    fit = powerlaw.Fit(data_expanded,discrete=True,xmin=3)
    
    dist=fit.power_law
    alpha=dist.alpha

    # Create figure

    powerlaw_func=lambda x, alpha,a1: a1*pow(x,-alpha) # powerlaw
    x,y = zip(*h_pct[1:])
    
    fig,ax = plt.subplots(figsize=(5,5))
    ax.plot(x,y,ls='none', **kwargs.get('customPlotParams').get('marker_emptyCircle'))
    ax.plot(x,powerlaw_func(x,alpha,1.3),ls='--',color='k')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which='both',linewidth=0.5, ls='--',color='.7')
    ax.set_xlabel('degree ($k$)')
    ax.set_ylabel('$p_k$')
    ax.set_xlim((8e-1,6e3))
    ax.set_ylim((1.5e-5,1))
    
    print(">>> CWN Degree Distribution Plot")
    print("  |--- Fit function: "+str(dist.name))
    print("  |--- Fit alpha: "+str(alpha))
    
    # Save figure
    figures_basedir = kwargs.get('figures_basedir')
    figPath=os.path.join(figures_basedir,'cwn_degree_dist.pdf')
    print("\n  >>> Saving figure {} ...".format(figPath))
    fig.savefig(figPath,dpi=192,format='pdf',bbox_inches='tight')
    print("  Figure saved successfully")
    return
    

def run(cwn, **kwargs):
    print(\
"""
=======================
CWN Degree distribution
-----------------------
""")
    plotFigures(cwn, **kwargs)

    return