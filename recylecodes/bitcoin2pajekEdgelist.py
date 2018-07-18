import pandas as pd
import networkx as nx
import json


def graph_reader(input_path):
    edges = pd.read_csv(input_path, sep=',', header=None, )
    #edges = pd.read_csv(input_path,sep=',')
    #print edges.values.tolist()


    #graph = nx.from_edgelist(edges.values.tolist())
    edges_list=[ (d[0],d[1],{'weight':d[2], 'color':'g' if d[2]>0 else 'r' }) for d in edges.values.tolist()]
    #print edges_list
    graph = nx.from_edgelist(edges_list)
    #print graph[2]
    return graph


def json_dumper(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def save_file(filename,G):
    f= open("data/paj/"+filename+".paj", "w+")
    nx.write_pajek(G, f)
    fh = open("./data/adj/"+filename+".adj", 'wb')
    nx.write_adjlist(G, fh)
    nx.write_weighted_edgelist(G, "./data/edg/"+filename+".edg")

if __name__ == "__main__":
    G = graph_reader('data/compress/soc-sign-bitcoinotc.csv')
    save_file('soc-sign-bitcoinotc', G)
    #do_a_series_of_propagations()