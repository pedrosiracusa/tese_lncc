

def getReport(scn,occs,datadict):
    sgs = sorted(scn.connectedComponentsSubgraphs(), key=lambda g: len(g.nodes()), reverse=True)
    datadict['subgraphs_count']=len(sgs) 
    datadict['subgraphs_nodes']=[ (sg.listCollectorsNodes(data=True), sg.listSpeciesNodes(data=True)) for sg in sgs ] # t[0] is collectors, t[1] is species
    datadict['subgraphs_connected_comp']=sgs[0]
    datadict['subgraphs_biggest_isolated']=sgs[1]
    
    # Get counts for biggest isolated component aggregated by phylum
    grouping=dict( (f,set(spp)) for f,spp in occs[['species','phylum']].groupby('phylum')['species'] )
    scn_comp1_phylum = datadict['subgraphs_biggest_isolated'].taxonomicAggregation(grouping)
    scn_comp1_phylum_counts = scn_comp1_phylum.listSpeciesNodes(data='count')
    datadict['subgraphs_biggest_isolated_phylum_counts']=scn_comp1_phylum_counts

def run(scn,occs):
    print(\
"""
===================
Connected Subgraphs
-------------------
""")
    data=dict()
    
    print(">>> Analyzing connected subgraphs from SCN...")
    getReport(scn,occs,datadict=data)
    print(">>> Num of subgraphs:",data['subgraphs_count'])
    print(">>> Top-10 subgraphs in nodes size:")
    lines = [ "    Graph {}: {} cols and {} spp;".format(i,len(cols),len(spp)) for i,(cols,spp) in enumerate(data['subgraphs_nodes'])][:10]
    for l in lines:
        print(l)
        
    print("")        
    print(">>> Taxons counts of the biggest isolated component. Aggregated by rank phylum :")
    lines = [ "    Phylum: {} | count: {};".format( *tpl) for tpl in data['subgraphs_biggest_isolated_phylum_counts'] ]
    for l in lines:
        print(l)
        
    print("""
Done with connected subgraphs 
-------------------

""")
    return data

def __main__(scn,occs):
    run(scn,occs)