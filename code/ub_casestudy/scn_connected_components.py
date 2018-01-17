

def getReport(scn,datadict):
    sgs = scn.connectedComponentsSubgraphs()
    datadict['subgraphs_count']=len(sgs) 
    datadict['subgraphs_nodes']=sorted( [ (sg.listCollectorsNodes(data=True), sg.listSpeciesNodes(data=True)) for sg in sgs ],
                                        key=lambda x: len(x[0])+len(x[1]), reverse=True) # t[0] is collectors, t[1] is species
    

def run(scn):
    print(\
"""
===================
Connected Subgraphs
-------------------
""")
    data=dict()
    
    print(">>> Analyzing connected subgraphs from SCN...")
    getReport(scn,data)
    print(">>> Num of subgraphs:",data['subgraphs_count'])
    
    print(">>> Top-10 subgraphs in nodes size:")
    lines = [ "    Graph {}: {} cols and {} spp;".format(i,len(cols),len(spp)) for i,(cols,spp) in enumerate(data['subgraphs_nodes'])][:10]
    for l in lines:
        print(l)
        
    print("""
Done with connected subgraphs 
-------------------

""")
    return data

def __main__(scn):
    run(scn)