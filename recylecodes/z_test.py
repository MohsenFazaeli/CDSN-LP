from spla.parser import parameter_parser
from spla.graph_io import graph_reader

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

args = parameter_parser()
G = graph_reader(args.input)

val_map = {1: 1.0,
           2: 0.5714285714285714,
           3: 0.0}
#print type(val_map)
#print G.nodes()

values = [val_map.get(node, 0.25) for node in G.nodes()]
print values
nx.draw_networkx(G, cmap=plt.get_cmap('jet'), node_color=values)
plt.show()

print len(G.edges)
print G.edges

wt_p=0
for (u, v, c) in G.edges.data('weight', default=0):
  wt_p+= 1 if c==1 else 0
print wt_p

wt_n=0
for (u, v, c) in G.edges.data('weight', default=0):
  wt_n+= 1 if c==-1 else 0
print wt_n

print [n for n in G.neighbors(1)]
print [n for n in G.neighbors(2)]

w_p={ n:0 for n in G.nodes}
w_n={ n:0 for n in G.nodes}

for wi in G.nodes():
    for wj in G.neighbors(wi):
        if G.edges[wi,wj]['weight'] > 0:
            w_p[wi]+=G.edges[wi,wj]['weight']
        else:
            w_n[wi] += G.edges[wi, wj]['weight']


sum=0

for wi in G.nodes():
    for wj in G.neighbors(wi):
        if (G.nodes[wi]['poslabel']==G.nodes[wj]['poslabel']):
            sum+= G.edges[wi,wj]['weight']-\
            ( (w_p[wi]*1.0*w_p[wj])/(2.0*wt_p) - (w_p[wi]*1.0*w_p[wj])/(2.0*wt_n))



for source,dist in G.edges:
    #print sourse,dist
    print G[source][dist]['weight']

    """
    if (G.nodes[source]['poslabel']==G.nodes[dist]['poslabel']):
        w
        G[source][dist]['weight']-\
        (  )+\
        (  )
        """