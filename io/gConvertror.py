from itertools import islice

import pandas as pd
import networkx as nx
import json
import numpy as np


dataDirecoty="/home/mf/PycharmProjects/DataSet"

def graph_reader(input_path,format,header=None, sep=',', comment='#', skiprows=0,isWeighted=True,normalizerFacor=1.0):
    print "graph_reader"
    if(format=='bitcoin'):
        #print "bitcoin"
        edges = pd.read_csv(input_path, sep=sep , header=None,comment=comment, skiprows=skiprows)
       #edges = pd.read_csv(input_path,sep=',')
        #print edges.values.tolist()
        #graph = nx.from_edgelist(edges.values.tolist())
        if(isWeighted):
            edges_list = [
                (int(d[0]), int(d[1]), {'weight': float(d[2])/normalizerFacor,  'color': 'g' if d[2] > 0 else 'r'}) for
                d in edges.values.tolist()] #'timestamp': d[3],
        else:
            edges_list = [
                (int(d[0]), int(d[1]), {'weight': 1 if int(d[2])>0 else -1, 'color': 'g' if d[2] > 0 else 'r'}) for
                d in edges.values.tolist()] #'timestamp': d[3],
        #print edges_list
        graph = nx.DiGraph(edges_list)
        #print graph[2]
        #return graph.to_undirected()
        return graph
    elif(format=='epinions' or format=='sladshot' or format=='konect'):
        print "sladshot"
        edges = pd.read_csv(input_path, sep=sep , header=None,comment=comment, skiprows=skiprows)
        #print edges
        #count=0
        #for d in edges:
        #    count+=1
        #    print d
        if(isWeighted):
            try:
                edges_list=[ (int(d[0]),int(d[1]),{'weight':float(d[2])/normalizerFacor, 'color':'g' if d[2]>0 else 'r' }) for d in edges.values.tolist()]
            except ValueError:
                print d
        else:
            edges_list = [(int(d[0]), int(d[1]), {'weight': 1 if int(d[2])>0 else -1, 'color': 'g' if d[2] > 0 else 'r'}) for d in
                          edges.values.tolist()]

        #print edges_list
        graph = nx.DiGraph(edges_list)
        return graph

    elif (format == 'wikiElec'):
        return
    elif (format == 'wikiRFA'):
        return
    else:
        return

def json_dumper(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def save_file(G,filename,post):
    f= open(dataDirecoty+"/paj/"+filename+".paj"+post, "w+")
    #f= open("data/paj/"+filename+"/"+filename+".paj"+post, "w+")
    nx.write_pajek(G, f)
    f = open(dataDirecoty + "/paj/" + post+"_" + filename + ".paj" + post, "w+")
    nx.write_pajek(G, f)

    fh = open(dataDirecoty+"/adj/"+filename+".adj"+post, 'wb')
    #fh = open("./data/adj/"+filename+"/"+filename+".adj"+post, 'wb')
    nx.write_adjlist(G, fh)

    fh = open(dataDirecoty+"/adj/"+post+"_"+filename+".adj"+post, 'wb')
    #fh = open("./data/adj/"+filename+"/"+filename+".adj"+post, 'wb')
    nx.write_adjlist(G, fh)
    #nx.write_weighted_edgelist(G, "./data/edg/"+filename+"/"+filename+".edg"+post)
    nx.write_weighted_edgelist(G, dataDirecoty+"/edg/"+filename+".edg"+post)
    nx.write_weighted_edgelist(G, dataDirecoty+"/edg/"+post+"_"+filename+".edg"+post)
    """
    f = open(dataDirecoty + "/matrix/" + filename + ".gra" + post, "w+")
    m=nx.to_numpy_matrix(G)
    f.write(";\n".join(", ".join(map(str, x)) for x in m.tolist()))
    f = open(dataDirecoty + "/matrix/" + post+"_"+filename + ".gra" + post, "w+")
    m=nx.to_numpy_matrix(G)
    f.write(";\n".join(", ".join(map(str, x)) for x in m.tolist()))
    """
if __name__ == "__main__":

    datasets={
        1:{'name':'bitcoin_otc' ,'file':'soc-sign-bitcoinotc.csv' ,'format': 'bitcoin', 'sep':',', 'comment':'#', 'skiprows':0,'normalizerFacor':10.0},
        2:{'name':'bitcoin_alpha' ,'file':'soc-sign-bitcoinalpha.csv' ,'format': 'bitcoin', 'sep':',', 'comment':'#', 'skiprows':0,'normalizerFacor':10.0},
        3:{'name':'slodshot_zoo' ,'file':'slodshotzoo.konect' ,'format': 'konect', 'sep':' ', 'comment':'%', 'skiprows':2,'normalizerFacor':1.0},
        4:{'name':'epinions' ,'file':'soc-sign-epinions.txt' ,'format': 'epinions', 'sep':'	', 'comment':'#', 'skiprows':4,'normalizerFacor':1.0},
        5:{'name':'wiki_elec' ,'file':'wikipediaElection.konect' ,'format': 'konect', 'sep':' ', 'comment':'%', 'skiprows':2,'normalizerFacor':1.0},
        6:{'name':'wiki_signed' ,'file':'wikisigned.konect' ,'format': 'konect', 'sep':' ', 'comment':'%', 'skiprows':1,'normalizerFacor':1.0},
        7:{'name':'highland_tribes' ,'file':'Highland-tribes.csv' ,'format': 'konect', 'sep':',', 'comment':'%', 'skiprows':1,'normalizerFacor':1.0},
        8:{'name':'SNM_AFF4' ,'file':'SNM_AFF4.csv' ,'format': 'konect', 'sep':',', 'comment':'%', 'skiprows':0,'normalizerFacor':1.0},
        9:{'name':'SNM_INFL' ,'file':'SNM_INFL.csv' ,'format': 'konect', 'sep':',', 'comment':'%', 'skiprows':0,'normalizerFacor':1.0},
        10:{'name':'stranke94' ,'file':'stranke94.csv' ,'format': 'konect', 'sep':',', 'comment':'%', 'skiprows':0 ,'normalizerFacor':215.0},
        11:{'name':'usSuprime' ,'file':'usSuprimeEdg.csv' ,'format': 'konect', 'sep':',', 'comment':'%', 'skiprows':0,'normalizerFacor':37.0},
    }

    for key in datasets:
        print key, 'corresponds to', datasets[key]
        G = graph_reader(dataDirecoty+"/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=True)
        save_file(G,datasets[key]['name'],"_WD")
        G = graph_reader(dataDirecoty+"/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=False)
        save_file(G,datasets[key]['name'],"_uWD")

        G = graph_reader(dataDirecoty+"/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=True)
        save_file(G.to_undirected(),datasets[key]['name'],"_WuD")
        G = graph_reader(dataDirecoty+"/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=False)
        save_file(G.to_undirected(),datasets[key]['name'],"_uWuD")

        G = graph_reader(dataDirecoty+"/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=True,normalizerFacor=datasets[key]['normalizerFacor'])
        save_file(G,datasets[key]['name'],"_nWD")
        #G = graph_reader("./data/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=False,normalizerFacor=datasets[key]['normalizerFacor'])
        #save_file(G,datasets[key]['name'],"uWD")

        G = graph_reader(dataDirecoty+"/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=True,normalizerFacor=datasets[key]['normalizerFacor'])
        save_file(G.to_undirected(),datasets[key]['name'],"_nWuD")
        #G = graph_reader("./data/compress/"+datasets[key]['file'], header=None,format=datasets[key]['format'], sep=datasets[key]['sep'], comment=datasets[key]['comment'], skiprows=datasets[key]['skiprows'],isWeighted=False,normalizerFacor=datasets[key]['normalizerFacor'])
        #save_file(G.to_directed(),datasets[key]['name'],"uWuD")

