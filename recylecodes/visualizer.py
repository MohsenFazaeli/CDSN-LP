import networkx as nx
import community
import matplotlib.pyplot as plt
from spla.graph_io import graph_reader
from spla.parser import parameter_parser
"""
G = nx.karate_club_graph()  # load a default graph

partition = community.best_partition(G)  # compute communities
print partition

pos = nx.spring_layout(G)  # compute graph layout
plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
plt.axis('off')
nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.3)
plt.show()
"""
args = parameter_parser()
G = graph_reader(args.input)
mlist =[ (s,d) for s, d in G.edges()  ]
for s, d in mlist:
    if G.edges[s, d]['weight'] < 0:
        G.remove_edge(s, d)

partition = community.best_partition(G)  # compute communities
print partition

pos = nx.spring_layout(G)  # compute graph layout
plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
plt.axis('off')
nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.3)
plt.show()
