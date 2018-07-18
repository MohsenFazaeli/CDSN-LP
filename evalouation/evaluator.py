import networkx as nx








def compute_Modularity(G,comunityMap,weights='weight',isSigned=True):
    w_p = {int(n): 0.0 for n in G.nodes}
    w_n = {int(n): 0.0 for n in G.nodes}

    for wi in G.nodes():
        for wj in G.neighbors(wi):
            if G.edges[wi, wj]['weight'] > 0:
                w_p[wi] += G.edges[wi, wj]['weight']
                #w_p[wi] += 1
            else:
                if G.edges[wi, wj]['weight'] < 0 :
                    w_n[wi] -= G.edges[wi, wj]['weight']
                    #w_n[wi] += 1
    wt_n=sum(w_n.values())
    wt_p=sum(w_p.values())

    sum_ = 0.0
    min_= 0.0
    min_2= 0.0

    for i in G.nodes():
        for j in G.nodes():
            negative_noise=((w_n[i] * 1.0 * w_n[j]) / ( wt_n))
            if G.has_edge(i,j):
                if  (comunityMap[i] == comunityMap[j]):
                    sum_ += G.edges[i, j]['weight'] - (  ((w_p[i] * 1.0 * w_p[j]) / ( wt_p))- negative_noise )
            else:
                #min_+= - (  ((w_p[i] * 1.0 * w_p[j]) / ( wt_p))- ((w_n[i] * 1.0 * w_n[j]) / ( wt_n)) )
                if  (comunityMap[i] == comunityMap[j]):
                    min_2 += - (((w_p[i] * 1.0 * w_p[j]) / (wt_p)) -negative_noise)
                    #min_2 += - (((w_p[i] * 1.0 * w_p[j]) / (wt_p)) - ((w_n[i] * 1.0 * w_n[j]) / (wt_n)))

    normfacto=1.0/((wt_p+wt_n))

    """
    print "parameters",
    print "wn",sum(w_n.values())
    print "wt_n",wt_n,w_n
    print "w_p",sum(w_p.values())
    print "wt_p",wt_p,w_p
    print normfacto
    print wt_n
    print wt_p
    """
    #print "final Q singed is:" + str (normfacto*sum_)
    #print normfacto*(sum_+min_)
    #print normfacto*(sum_-min_)
    #print
    #print normfacto*(sum_-min_2)
    print "Evaluatin moulde final Q singed is:" + str(normfacto*(sum_+min_2))
    return str(normfacto*(sum_+min_2))