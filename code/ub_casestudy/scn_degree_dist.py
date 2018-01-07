import os
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import powerlaw

def plotfigures(scn,figures_basedir):
    species_k = scn.degree(scn.listSpeciesNodes())
    collectors_k = scn.degree(scn.listCollectorsNodes())
    
    myfig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(10,10)) # This figure will store all figures
    
    
    #############
    #### Plot (c)
    #------------
    
    # scatter plot data
    x,y = zip(*sorted( [(k,n) for k,n in Counter( k for n,k in list(species_k) ).items()], key=lambda x: x[0] ))
    
    # histogram data
    degree_counts = Counter( k for n,k in list(species_k) )
    highest_degree=max(degree_counts.keys())
    lowest_degree=min(degree_counts.keys())
    l=[ (i, degree_counts.get(i,0)) for i in range(lowest_degree,highest_degree+1)]
    x_hist=[ i for l in [ [k for i in range(cnt)] for k,cnt in l ] for i in l ]
    
    
    ax3.plot(x,y,'o',markerfacecolor='none',markeredgewidth=.6,ms=7,color='r')
    ax3.set_yscale('log')
    
    # plot histogram
    binsize=10
    lowest=0
    highest=highest_degree
    binseq = range(lowest,highest+1,binsize) if (highest-lowest)%binsize==0 else range(lowest,highest+binsize,binsize)
    
    ax3.hist(x_hist,bins=binseq,log=True,color='.9',ec='.6',lw=0.5)
    
    ax3.set_ylim((7e-1,1.5e4))
    ax3.set_xlabel('degree ($k$)')
    ax3.set_ylabel('species $N_k$')
    ax3.grid(which='both',linewidth=0.5, ls='--',color='.7')
    ax3.text(360,6e3,'(c)')
    
    
    #############
    #### Plot (a)
    # -----------
    degree_counts = Counter( k for n,k in list(species_k) )
    # scatter plot data
    # linear binning
    k,n = zip(*sorted( [(k,n) for k,n in degree_counts.items()], key=lambda x: x[0] ))
    pk = [ i/sum(n) for i in n ]
    
    # Fitting a powerlaw
    data_expanded = [ k for k,cnt in list(zip(k,n)) for i in range(cnt) ]
    fit = powerlaw.Fit(data_expanded,discrete=True,xmin=6)
    
    dist=fit.truncated_power_law
    alpha=dist.alpha
    lbda=dist.Lambda
    
    f=lambda x, alpha,lbda,a1: a1*pow(x,-alpha)*np.exp(-lbda*x) # powerlaw with cutoff function
    
    # Plotting results
    ax1.plot(k, pk, 'o',markerfacecolor='none',markeredgewidth=.6,ms=7,alpha=0.8,color='r')
    ax1.plot(k, f(np.array(k),alpha,lbda,0.55), ls='--',color='k')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('degree ($k$)')
    ax1.set_ylabel('species $p_k$')
    ax1.set_xlim((8e-1,6e3))
    ax1.set_ylim((1.5e-5,1))
    ax1.grid(which='both',linewidth=0.5, ls='--',color='.8')
    ax1.text(2e3,4e-1, '(a)')
    
    print("\n  >>> SCN Degree Distribution Plot (a)")
    print("  |--- Fit function: "+str(dist.name))
    print("  |--- Fit alpha: "+str(alpha))
    print("  |--- Fit lambda: "+str(lbda))
    
    
    #############
    #### Plot (d)
    # -----------
    
    # scatter plot data
    x,y = zip(*sorted( [(k,n) for k,n in Counter( k for n,k in list(collectors_k) ).items()], key=lambda x: x[0] ))
    
    # histogram data
    degree_counts = Counter( k for n,k in list(collectors_k) )
    highest_degree=max(degree_counts.keys())
    lowest_degree=min(degree_counts.keys())
    l=[ (i, degree_counts.get(i,0)) for i in range(lowest_degree,highest_degree+1)]
    x_hist=[ i for l in [ [k for i in range(cnt)] for k,cnt in l ] for i in l ]
    
    # plot scatter
    ax4.plot(x,y,'o',markerfacecolor='none', markeredgewidth=.6,ms=7,color='b')
    ax4.set_yscale('log')
    
    # plot histogram
    binsize=100
    lowest=0
    highest=highest_degree
    binseq = range(lowest,highest+1,binsize) if (highest-lowest)%binsize==0 else range(lowest,highest+binsize,binsize)
    
    ax4.hist(x_hist,bins=binseq,log=True,color='.9',ec='.6',lw=0.5)
    
    ax4.set_ylim((7e-1,1.5e4))
    ax4.set_xlabel('degree ($k$)')
    ax4.set_ylabel('collectors $N_k$')
    ax4.grid(which='both',linewidth=0.5, ls='--',color='.7')
    ax4.text(4200,6e3,'(d)')
    
    #############
    #### Plot (c)
    # ----------
    
    degree_counts = Counter( k for n,k in list(collectors_k) )
    # scatter plot data
    # linear binning
    k,n = zip(*sorted( [(k,n) for k,n in degree_counts.items()], key=lambda x: x[0] ))
    pk = [ i/sum(n) for i in n ]
    
    # Fitting a powerlaw
    data_expanded = [ k for k,cnt in zip(k,n) for i in range(cnt) ]
    fit = powerlaw.Fit(data_expanded,discrete=True,xmin=1)
    
    dist=fit.power_law
    alpha=dist.alpha
    #lbda=dist.Lambda
    
    #f=lambda x, alpha,lbda,a1: a1*pow(x,-alpha)*np.exp(-lbda*x) # powerlaw with cutoff function
    f=lambda x, alpha,a1: a1*pow(x,-alpha) # powerlaw
    
    
    # Plotting results
    fig,ax=plt.subplots(figsize=(6,6))
    
    ax2.plot(k, pk, 'o',markerfacecolor='none',markeredgewidth=.6,ms=7,alpha=0.8,color='b')
    ax2.plot(k, f(np.array(k),alpha,0.5), ls='--',color='k')
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('degree ($k$)')
    ax2.set_ylabel('collectors $p_k$')
    ax2.set_xlim((8e-1,6e3))
    ax2.set_ylim((1.5e-5,1))
    ax2.grid(which='both',linewidth=0.5, ls='--',color='.8')
    ax2.text(2e3,4e-1, '(b)')
    
    print("\n  >>> SCN Degree Distribution Plot (b)")
    print("  |--- Fit function: "+str(dist.name))
    print("  |--- Fit alpha: "+str(alpha))
    
    
    ###################
    # Save final figure
    # -----------------
    figPath=os.path.join(figures_basedir,'casestudy_ub/scn_degree_dist.pdf')
    print("\n  >>> Saving figure {} ...".format(figPath))
    myfig.savefig(figPath,dpi=192,format='pdf',bbox_inches='tight')
    print("  Figure saved successfully")
   
    

def getReport(scn):
    collectors_k = scn.degree(scn.listCollectorsNodes())
    species_k = scn.degree(scn.listSpeciesNodes())
    
    colnodes_k_avg = np.average([ v for u,v in collectors_k ])
    spnodes_k_avg = np.average([ v for u,v in species_k ])
    num_col_nodes = len(scn.listCollectorsNodes())
    num_spp_nodes = len(scn.listSpeciesNodes())
    
    
    data = {
            'num_col_nodes': num_col_nodes,
            'num_sp_nodes': num_spp_nodes,
            'top10_collectors': sorted( list(collectors_k), key=lambda x: x[1],reverse=True )[:10] ,
            'top10_species': sorted( list(species_k), key=lambda x: x[1],reverse=True )[:10],
            'colnodes_k_avg': colnodes_k_avg,
            'spnodes_k_avg': spnodes_k_avg,
            'perc_cols_k_leq_avg': sum( 1 for n,k in collectors_k if k<=colnodes_k_avg )/num_col_nodes,
            'perc_sp_k_leq_avg':  sum( 1 for n,k in species_k if k<=spnodes_k_avg )/num_spp_nodes,
            'num_cols_k_leq_10': sum(1 for u,v in collectors_k if v<=10),
            'perc_cols_k_leq_10': sum( 1 for u,v in collectors_k if v<=10)/num_col_nodes,
            'num_sp_k_leq_10': sum(1 for u,v in species_k if v<=10),
            'perc_sp_k_leq_10': sum( 1 for u,v in species_k if v<=10)/num_spp_nodes
     }
    
    return data



def createLatexTables(scn):
    report_data = getReport(scn)
    num_col_nodes = report_data['num_col_nodes']
    num_spp_nodes = report_data['num_sp_nodes']
    colnodes_k_avg = report_data['colnodes_k_avg']
    spnodes_k_avg = report_data['spnodes_k_avg']
    collectors_top10 = report_data['top10_collectors']
    species_top10 = report_data['top10_species']
    
    table_data= {
     'collectors': (num_col_nodes,
                    colnodes_k_avg,
                    [ col for col,k in collectors_top10 ],
                    [ k for col,k in collectors_top10],
                    [ k/num_spp_nodes for col,k in collectors_top10 ]) ,
     'species': (num_spp_nodes, 
                 spnodes_k_avg,
                    [ sp for sp,k in species_top10],
                    [ k for sp,k in species_top10],
                    [ k/num_col_nodes for sp,k in species_top10]) }
     
    # Create latex tables
    tables = []
    
    # Table 1
    table_label="table:ub_scn_degrees"
    table_caption=r"Some degree metrics for the UB SCN model. For each nodes set the total number of nodes, average degree $\langle k \rangle$, top-10 highest-degree nodes and their respective degrees $k$ are listed. We define $k^*$ as the maximum possible degree of a nodes set, a metric that represents the degree of a hypothetical node which is connected to every single node from the complementary set. Therefore $k/k^*$ is the proportion of nodes from the complementary set a given node is linked to."
    table = r"""
  \caption{"""+table_caption+r"""}
  \begin{center}
  \begin{tabular}{l c c c c c}
    & num of nodes & $\langle k \rangle$ & top-10 & $k$ & $k/k^*$ \\
   \hline"""

    for nset,d in table_data.items():
        table += r"    {} & {} & {:.2f} &".format(nset, d[0], d[1])
        table +="\n"
        for i,col in enumerate(d[2:]):
            table += r"   \begin{tabular}[t]{{@{}c@{}@{}}}"
            for el in col:
                if i==2: table +="{:.2f}\\\\".format(float(el)) # formatting percentages
                elif nset=='species' and i==0: table +="\\textit{{{}}}\\\\".format(el) # species name to italics
                else: table += "{}\\\\".format(el) # other columns
            
            table = table[:-2]
            table += "\\end{{tabular}} &\n".format(col[-1])
        
        table = table[:-2]
        table += r"\\ \\"+"\n"
    
    table = table[:-3]+"\n"
    table+=r"""  \hline
  \end{tabular}
  \end{center}
  \label{"""+table_label+r"""}
"""

    tables.append( (table_label.replace(':','_'), table) )
    # end of Table 1

    return tables