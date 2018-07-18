import networkx as nx
from tqdm import tqdm

def normalized_overlap(g, node_1, node_2):
    inter = len(set(nx.neighbors(g, node_1)).intersection(set(nx.neighbors(g, node_2))))
    unio = len(set(nx.neighbors(g, node_1)).union(set(nx.neighbors(g, node_2))))
    return float(inter)/float(unio)

def overlap(G, node_1, node_2):
    list1=[]
    for wj in G.neighbors(node_1):
        if G.edges[node_1, wj]['weight'] > 0:
            list1.append(wj)
    list2 = []
    for wj in G.neighbors(node_2):
        if G.edges[node_2, wj]['weight'] > 0:
            list2.append(wj)

    inter1 = len(set(list1).intersection(set(list2)))

    list1 = []
    for wj in G.neighbors(node_1):
        if G.edges[node_1, wj]['weight'] < 0:
            list1.append(wj)
    list2 = []
    for wj in G.neighbors(node_2):
        if G.edges[node_2, wj]['weight'] < 0:
            list2.append(wj)

    inter2 = len(set(list1).intersection(set(list2)))

    list1 = []
    for wj in G.neighbors(node_1):
        if G.edges[node_1, wj]['weight'] > 0 and G.has_edge(node_2,wj) and G.edges[node_2, wj]['weight'] < 0:
            list1.append(wj)
    list2 = []
    for wj in G.neighbors(node_2):
        if G.edges[node_2, wj]['weight'] > 0 and G.has_edge(node_1, wj) and G.edges[node_1, wj]['weight'] < 0:
            list2.append(wj)

    inter3 = len(set(list1).union(set(list2)))
    return float(inter1+inter2)

def unit(g, node_1, node_2):
    return 1

def min_norm(g, node_1, node_2):
    inter = len(set(nx.neighbors(g, node_1)).intersection(set(nx.neighbors(g, node_2))))
    min_norm = min(len(set(nx.neighbors(g, node_1))), len(set(nx.neighbors(g, node_2))))
    return float(inter)/float(min_norm)

def mea_sim(G, node_1, node_2):
    xl= set(G.neighbors(node_1))
    #print xl
    xl=set(xl).union(set(G.neighbors(node_2)))
    xl=set(xl).union(set([node_1, node_2]))
    sai=0.0
    for x in xl:
        if(G.has_edge(node_1,x) and G.has_edge(node_2,x)):
            if not(G.edges[node_1,x]['weight']<0 and G.edges[node_2,x]['weight']<0 ):
                sai+= G.edges[node_1,x]['weight'] * G.edges[node_2,x]['weight']
    usquare=0.0
    for i in G.neighbors(node_1):
        usquare+=G.edges[node_1,i]['weight'] * G.edges[node_1,i]['weight']
    vsquare=0.0
    for i in G.neighbors(node_2):
        vsquare+=G.edges[node_2,i]['weight'] * G.edges[node_2,i]['weight']

    return float( sai/(usquare*vsquare))

def overlap_generator(metric, graph):
    edges = nx.edges(graph)
    #print list(edges)
    #print list(map(lambda x: (x[1], x[0]), edges))
    edges = list(edges) + list(map(lambda x: (x[1], x[0]), edges))
    return {edge: metric(graph, edge[0], edge[1]) for edge in tqdm(edges)}
