from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import powerlaw

def plotfigure(scn):
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
    
    print("CWN Degree Distribution Plot (a)")
    print("--- Fit function: "+str(dist.name))
    print("--- Fit alpha: "+str(alpha))
    print("--- Fit lambda: "+str(lbda))
    
    
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
    
    dist=fit.truncated_power_law
    alpha=dist.alpha
    #lbda=dist.Lambda
    
    #f=lambda x, alpha,lbda,a1: a1*pow(x,-alpha)*np.exp(-lbda*x) # powerlaw with cutoff function
    f=lambda x, alpha,a1: a1*pow(x,-alpha) # powerlaw
    
    
    # Plotting results
    fig,ax=plt.subplots(figsize=(6,6))
    
    ax2.plot(k, pk, 'o',markerfacecolor='none',markeredgewidth=.6,ms=7,alpha=0.8,color='b')
    ax2.plot(k, f(np.array(k),alpha,0.4), ls='--',color='k')
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('degree ($k$)')
    ax2.set_ylabel('collectors $p_k$')
    ax2.set_xlim((8e-1,6e3))
    ax2.set_ylim((1.5e-5,1))
    ax2.grid(which='both',linewidth=0.5, ls='--',color='.8')
    ax2.text(2e3,4e-1, '(b)')
    
    print("CWN Degree Distribution Plot (b)")
    print("--- Fit function: "+str(dist.name))
    print("--- Fit alpha: "+str(alpha))
    
    
    ###################
    # Save final figure
    # -----------------
    
    myfig.savefig('./figures/cwn_degree_dist.pdf',dpi=192,format='pdf',bbox_inches='tight')