"""
import networkx as nx
from  matplotlib import pyplot as plt

G = nx.erdos_renyi_graph(8,0.4)
p = nx.shortest_path(G,0,3)
# Set all edge color attribute to black
for e in G.edges():
    G[e[0]][e[1]]['color'] = 'black'
# Set color of edges of the shortest path to green
for i in xrange(len(p)-1):
    G[p[i]][p[i+1]]['color'] = 'blue'
# Store in a list to use for drawing
edge_color_list = [ G[e[0]][e[1]]['color'] for e in G.edges() ]
nx.draw(G,edge_color = edge_color_list, with_labels = True)
plt.show()
"""
"""
G=nx.Graph()
G.add_edges_from([(1,3),(2,4),(3,5),(4,6)], weight = 1)dfsfsfafa
G.add_edges_from([(1,2),(2,3),(3,4),(4,5)], weight = -1)

pos_edges = [(u,v,w) for (u,v,w) in G.edges(data=True) if w['weight']>0]
neg_edges = [(u,v,w) for (u,v,w) in G.edges(data=True) if w['weight']<0]

Hpos = nx.Graph()
Hneg = nx.Graph()

Hpos.add_edges_from(pos_edges)
Hneg.add_edges_from(neg_edges)

print Hneg.edges(data=True)
print Hneg.neighbors(1)

[(1, 2, {'weight': -1}),
 (2, 3, {'weight': -1}),
 (3, 4, {'weight': -1}),
 (4, 5, {'weight': -1})]
Hpos.edges(data=True)
 [(1, 3, {'weight': 1}),
 (2, 4, {'weight': 1}),
 (3, 5, {'weight': 1}),
 (4, 6, {'weight': 1})]
"""


"""

import community

import networkx as nx
import matplotlib.pyplot as plt

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
G = nx.erdos_renyi_graph(30, 0.05)

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()
"""




"""

sorted_by_second = sorted(data, key=lambda tup: tup[1])

or:

data.sort(key=lambda tup: tup[1])  # sorts in place

"""