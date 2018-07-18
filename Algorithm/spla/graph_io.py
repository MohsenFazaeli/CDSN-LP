import pandas as pd
import networkx as nx
import json

def graph_reader(input_path):
    edges = pd.read_csv(input_path,sep=',',header=None)
    #edges = pd.read_csv(input_path,sep=',')
    #print edges.values.tolist()


    #graph = nx.from_edgelist(edges.values.tolist())
    edges_list=[ (d[0],d[1],{'weight':d[2], 'color':'g' if d[2]>0 else 'r' }) for d in edges.values.tolist()]
    #edges_list=[ (d[0],d[1],{'weight':1 if d[2]>0 else -1, 'color':'g' if d[2]>0 else 'r' }) for d in edges.values.tolist()]
    #print edges_list
    graph = nx.from_edgelist(edges_list)

    #print graph[2]

    return graph

def json_dumper(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)