# -*- coding: utf-8 -*-
"""
This module implements community detection.
"""
from __future__ import print_function
import matplotlib.pyplot as plt

import array
import random

import networkx as nx

from community_status import Status
import config as cfg
import  Algorithm.spla.graph_io as gio
import evalouation.evaluator as eval


__author__ = """Thomas Aynaud (thomas.aynaud@lip6.fr)"""
#    Copyright (C) 2009 by
#    Thomas Aynaud <thomas.aynaud@lip6.fr>
#    All rights reserved.
#    BSD license.

__PASS_MAX = -1
__MIN = 0.0000001


def partition_at_level(dendrogram, level):
    """Return the partition of the nodes at the given level

    A dendrogram is a tree and each level is a partition of the graph nodes.
    Level 0 is the first partition, which contains the smallest communities,
    and the best is len(dendrogram) - 1.
    The higher the level is, the bigger are the communities

    Parameters
    ----------
    dendrogram : list of dict
       a list of partitions, ie dictionnaries where keys of the i+1 are the
       values of the i.
    level : int
       the level which belongs to [0..len(dendrogram)-1]

    Returns
    -------
    partition : dictionnary
       A dictionary where keys are the nodes and the values are the set it
       belongs to

    Raises
    ------
    KeyError
       If the dendrogram is not well formed or the level is too high

    See Also
    --------
    best_partition which directly combines partition_at_level and
    generate_dendrogram to obtain the partition of highest modularity

    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> dendrogram = generate_dendrogram(G)
    >>> for level in range(len(dendrogram) - 1) :
    >>>     print("partition at level", level, "is", partition_at_level(dendrogram, level))  # NOQA
    """
    partition = dendrogram[0].copy()
    for index in range(1, level + 1):
        for node, community in partition.items():
            partition[node] = dendrogram[index][community]
    return partition


def modularity(partition, graph, weight='weight'):
    """Compute the modularity of a partition of a graph

    Parameters
    ----------
    partition : dict
       the partition of the nodes, i.e a dictionary where keys are their nodes
       and values the communities
    graph : networkx.Graph
       the networkx graph which is decomposed
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'


    Returns
    -------
    modularity : float
       The modularity

    Raises
    ------
    KeyError
       If the partition is not a partition of all graph nodes
    ValueError
        If the graph has no link
    TypeError
        If graph is not a networkx.Graph

    References
    ----------
    .. 1. Newman, M.E.J. & Girvan, M. Finding and evaluating community
    structure in networks. Physical Review E 69, 26113(2004).

    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> part = best_partition(G)
    >>> modularity(part, G)
    """
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = graph.size(weight=weight)
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        com = partition[node]
        deg[com] = deg.get(com, 0.) + graph.degree(node, weight=weight)
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor == node:
                    inc[com] = inc.get(com, 0.) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.

    res = 0.
    for com in set(partition.values()):
        res += (inc.get(com, 0.) / links) - \
               (deg.get(com, 0.) / (2. * links)) ** 2
    return res


def best_partition(graph, partition=None,
                   weight='weight', resolution=1., randomize=False):
    """Compute the partition of the graph nodes which maximises the modularity
    (or try..) using the Louvain heuristices

    This is the partition of highest modularity, i.e. the highest partition
    of the dendrogram generated by the Louvain algorithm.

    Parameters
    ----------
    graph : networkx.Graph
       the networkx graph which is decomposed
    partition : dict, optional
       the algorithm will start using this partition of the nodes.
       It's a dictionary where keys are their nodes and values the communities
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'
    resolution :  double, optional
        Will change the size of the communities, default to 1.
        represents the time described in
        "Laplacian Dynamics and Multiscale Modular Structure in Networks",
        R. Lambiotte, J.-C. Delvenne, M. Barahona
    randomize :  boolean, optional
        Will randomize the node evaluation order and the community evaluation
        order to get different partitions at each call

    Returns
    -------
    partition : dictionnary
       The partition, with communities numbered from 0 to number of communities

    Raises
    ------
    NetworkXError
       If the graph is not Eulerian.

    See Also
    --------
    generate_dendrogram to obtain all the decompositions levels

    Notes
    -----
    Uses Louvain algorithm

    References
    ----------
    .. 1. Blondel, V.D. et al. Fast unfolding of communities in
    large networks. J. Stat. Mech 10008, 1-12(2008).

    Examples
    --------
    >>>  #Basic usage
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> part = best_partition(G)

    >>> #other example to display a graph with its community :
    >>> #better with karate_graph() as defined in networkx examples
    >>> #erdos renyi don't have true community structure
    >>> G = nx.erdos_renyi_graph(30, 0.05)
    >>> #first compute the best partition
    >>> partition = community.best_partition(G)
    >>>  #drawing
    >>> size = float(len(set(partition.values())))
    >>> pos = nx.spring_layout(G)
    >>> count = 0.
    >>> for com in set(partition.values()) :
    >>>     count += 1.
    >>>     list_nodes = [nodes for nodes in partition.keys()
    >>>                                 if partition[nodes] == com]
    >>>     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))
    >>> nx.draw_networkx_edges(G, pos, alpha=0.5)
    >>> plt.show()
    """
    dendo = generate_dendrogram(graph,
                                partition,
                                weight,
                                resolution,
                                randomize)
    print(dendo)
    return partition_at_level(dendo, len(dendo) - 1)


def generate_dendrogram(graph,
                        part_init=None,
                        weight='weight',
                        resolution=1.,
                        randomize=False):
    """Find communities in the graph and return the associated dendrogram

    A dendrogram is a tree and each level is a partition of the graph nodes.
    Level 0 is the first partition, which contains the smallest communities,
    and the best is len(dendrogram) - 1. The higher the level is, the bigger
    are the communities


    Parameters
    ----------
    graph : networkx.Graph
        the networkx graph which will be decomposed
    part_init : dict, optional
        the algorithm will start using this partition of the nodes. It's a
        dictionary where keys are their nodes and values the communities
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'
    resolution :  double, optional
        Will change the size of the communities, default to 1.
        represents the time described in
        "Laplacian Dynamics and Multiscale Modular Structure in Networks",
        R. Lambiotte, J.-C. Delvenne, M. Barahona

    Returns
    -------
    dendrogram : list of dictionaries
        a list of partitions, ie dictionnaries where keys of the i+1 are the
        values of the i. and where keys of the first are the nodes of graph

    Raises
    ------
    TypeError
        If the graph is not a networkx.Graph

    See Also
    --------
    best_partition

    Notes
    -----
    Uses Louvain algorithm

    References
    ----------
    .. 1. Blondel, V.D. et al. Fast unfolding of communities in large
    networks. J. Stat. Mech 10008, 1-12(2008).

    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> dendo = generate_dendrogram(G)
    >>> for level in range(len(dendo) - 1) :
    >>>     print("partition at level", level,
    >>>           "is", partition_at_level(dendo, level))
    :param weight:
    :type weight:
    """
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    # special case, when there is no link
    # the best partition is everyone in its community
    if graph.number_of_edges() == 0:
        part = dict([])
        for node in graph.nodes():
            part[node] = node
        return [part]

    current_graph = graph.copy()
    #status = Status()
    #status.init(current_graph, weight, part_init)

    status_list = list()

    posStatus = Status()
    posGraph=nx.Graph();
    posGraph.add_nodes_from(current_graph.nodes)
    posGraph.add_edges_from([(a,b,{'weight':c }) for (a,b,c) in current_graph.edges.data('weight', default=1) if c>0])
    posStatus.init(posGraph, weight, part_init)
    #posStatus.list=list()

    negStatus = Status()
    negGraph = nx.Graph();
    negGraph.add_nodes_from(current_graph.nodes)
    negGraph.add_edges_from([(a, b, {'weight': -c}) for (a, b, c) in current_graph.edges.data('weight', default=-1) if c < 0])
    negStatus.init(negGraph, weight, part_init)
    #negStatus.list = list()
    print(posStatus.total_weight )
    print(negStatus.total_weight )
    print(len(negGraph.nodes()),len(posGraph.nodes()))
    print(len(negGraph.edges()),len(posGraph.edges()))
    #print(negGraph.nodes(),negGraph.edges())
    #print(current_graph.edges.data('weight', default=-1))
    #print(current_graph.edges.data('weight', default=0))


    __one_level(posGraph ,negGraph, posStatus ,negStatus , weight, resolution, randomize)
    #TODO  Edit one_levl function
    posMul= float(posStatus.total_weight /(posStatus.total_weight + negStatus.total_weight)) #Multip by 2 is impactless
    negMul= float(negStatus.total_weight /(posStatus.total_weight + negStatus.total_weight)) #Multip by 2 is impactless
    new_mod = posMul*__modularity(posStatus)- negMul*__modularity(negStatus)
    #TODO check modularity works correct

    partition = __renumber(posStatus.node2com)
    status_list.append(partition)
    mod = new_mod
    #current_graph = induced_graph(partition, current_graph, weight)
    #status.init(current_graph, weight)
    posGraph = induced_graph(partition, posGraph, weight);
    posStatus.init(posGraph, weight, part_init)

    negGraph = induced_graph(partition, negGraph, weight);
    negStatus.init(negGraph, weight, part_init)
    print(" WHile ")

    while True:
        print(" WHile ")

        __one_level(posGraph, negGraph, posStatus, negStatus, weight, resolution, randomize)
        #__one_level(current_graph, status, weight, resolution, randomize)
        #new_mod = __modularity(status)
        pos_mod = __modularity(posStatus)
        neg_mod = __modularity(negStatus)
        new_mod = posMul * pos_mod - negMul * neg_mod

         #TODO Sth is not double
        if new_mod - mod < __MIN:
            break
        partition = __renumber(posStatus.node2com)
        status_list.append(partition)
        mod = new_mod
        posGraph = induced_graph(partition, posGraph, weight)
        negGraph = induced_graph(partition, negGraph, weight)
        posStatus.init(posGraph, weight)
        negStatus.init(negGraph, weight)
        print("\n\n\n our modularity: ",mod)
    print("eow WHile ")

    return status_list[:]


def induced_graph(partition, graph, weight="weight"):
    """Produce the graph where nodes are the communities

    there is a link of weight w between communities if the sum of the weights
    of the links between their elements is w

    Parameters
    ----------
    partition : dict
       a dictionary where keys are graph nodes and  values the part the node
       belongs to
    graph : networkx.Graph
        the initial graph
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'


    Returns
    -------
    g : networkx.Graph
       a networkx graph where nodes are the parts

    Examples
    --------
    >>> n = 5
    >>> g = nx.complete_graph(2*n)
    >>> part = dict([])
    >>> for node in g.nodes() :
    >>>     part[node] = node % 2
    >>> ind = induced_graph(part, g)
    >>> goal = nx.Graph()
    >>> goal.add_weighted_edges_from([(0,1,n*n),(0,0,n*(n-1)/2), (1, 1, n*(n-1)/2)])  # NOQA
    >>> nx.is_isomorphic(int, goal)
    True
    """
    ret = nx.Graph()
    ret.add_nodes_from(partition.values())

    for node1, node2, datas in graph.edges(data=True):
        edge_weight = datas.get(weight, 1)
        com1 = partition[node1]
        com2 = partition[node2]
        w_prec = ret.get_edge_data(com1, com2, {weight: 0}).get(weight, 1)
        ret.add_edge(com1, com2, **{weight: w_prec + edge_weight})

    return ret


def __renumber(dictionary):
    """Renumber the values of the dictionary from 0 to n
    """
    count = 0
    ret = dictionary.copy()
    new_values = dict([])

    for key in dictionary.keys():
        value = dictionary[key]
        new_value = new_values.get(value, -1)
        if new_value == -1:
            new_values[value] = count
            new_value = count
            count += 1
        ret[key] = new_value

    return ret


def load_binary(data):
    """Load binary graph as used by the cpp implementation of this algorithm
    """
    data = open(data, "rb")

    reader = array.array("I")
    reader.fromfile(data, 1)
    num_nodes = reader.pop()
    reader = array.array("I")
    reader.fromfile(data, num_nodes)
    cum_deg = reader.tolist()
    num_links = reader.pop()
    reader = array.array("I")
    reader.fromfile(data, num_links)
    links = reader.tolist()
    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))
    prec_deg = 0

    for index in range(num_nodes):
        last_deg = cum_deg[index]
        neighbors = links[prec_deg:last_deg]
        graph.add_edges_from([(index, int(neigh)) for neigh in neighbors])
        prec_deg = last_deg

    return graph


def __randomly(seq, randomize):
    """ Convert sequence or iterable to an iterable in random order if
    randomize """
    if randomize:
        shuffled = list(seq)
        random.shuffle(shuffled)
        return iter(shuffled)
    return seq


def __one_level(posGraph,negGraph, posStatus,negStatus, weight_key, resolution, randomize):
    """Compute one level of communities
    """

    modified = True
    nb_pass_done = 0
    posMul= float(posStatus.total_weight /(posStatus.total_weight + negStatus.total_weight)) #Multip by 2 is impactless
    negMul= float(negStatus.total_weight /(posStatus.total_weight + negStatus.total_weight)) #Multip by 2 is impactless
    new_mod = posMul*__modularity(posStatus)- negMul*__modularity(negStatus)

    #cur_mod = __modularity(status)
    cur_mod = new_mod

    #new_mod = cur_mod

    while modified and nb_pass_done != __PASS_MAX:
        cur_mod = new_mod
        modified = False
        nb_pass_done += 1

        for node in __randomly(posGraph.nodes(), randomize):
            com_node = posStatus.node2com[node]
            print("___________________________")
            print("for node: ",node," in com: ",com_node)

            pos_degc_totw = posStatus.gdegrees.get(node, 0.) / (posStatus.total_weight * 2.)  # NOQA # ki/2m
            print(pos_degc_totw)
            neg_degc_totw = negStatus.gdegrees.get(node, 0.) / (negStatus.total_weight * 2.)  # NOQA # ki/2m
            print(neg_degc_totw)

            pos_neigh_communities = __neighcom(node, posGraph, posStatus, weight_key)

            neg_neigh_communities = __neighcom(node, negGraph, negStatus, weight_key)


            #remove_cost = - resolution * neigh_communities.get(com_node,0) + \               - ki,c + (kc-ki)/2m
            #    (status.degrees.get(com_node, 0.) - status.gdegrees.get(node, 0.)) * degc_totw

            pos_remove_cost = - resolution * pos_neigh_communities.get(com_node,0) + \
               (posStatus.degrees.get(com_node, 0.) - posStatus.gdegrees.get(node, 0.)) * pos_degc_totw

            neg_remove_cost = - resolution * neg_neigh_communities.get(com_node,0) + \
               (negStatus.degrees.get(com_node, 0.) - negStatus.gdegrees.get(node, 0.)) * neg_degc_totw

            remove_cost=posMul*pos_remove_cost-negMul*neg_remove_cost

            __remove(node, com_node,
                     pos_neigh_communities.get(com_node, 0.), posStatus)
            __remove(node, com_node,
                     neg_neigh_communities.get(com_node, 0.), negStatus)
            #Todo _remove check

            best_com = com_node
            best_increase = 0
            #TODO upto here refined check for dnc
            #print(type(pos_neigh_communities.keys()))
            for com in __randomly(pos_neigh_communities.keys()+neg_neigh_communities.keys(),  # only joining posetive commuinty has bounous
                                       randomize):

                print("\n Itration \n")
                print( neg_neigh_communities)
                print( pos_neigh_communities)

                #pos_incr =  resolution * pos_neigh_communities[com] - \
                #       posStatus.degrees.get(com, 0.) * pos_degc_totw

                pos_incr =  resolution * pos_neigh_communities.get(com, 0.) - \
                       posStatus.degrees.get(com, 0.) * pos_degc_totw

                neg_incr =  resolution * neg_neigh_communities.get(com, 0.) - \
                       negStatus.degrees.get(com, 0.) * neg_degc_totw
                        #remove_cost +
                       #(status.degrees.get(com_node, 0.) * status.gdegrees.get(node, 0.)) * degc_totw
                       #status.degrees.get(com, 0.) * degc_totw

                incr = remove_cost + posMul * pos_incr - negMul * neg_incr


                if incr > best_increase:
                    best_increase = incr
                    best_com = com
            __insert(node, best_com,
                     pos_neigh_communities.get(best_com, 0.), posStatus)
            __insert(node, best_com,
                     neg_neigh_communities.get(best_com, 0.), negStatus)

            if best_com != com_node:
                modified = True

        pos_mod = __modularity(posStatus)
        neg_mod = __modularity(negStatus)

        new_mod = posMul * pos_mod - negMul * neg_mod

        if new_mod - cur_mod < __MIN:
            break


def __neighcom(node, graph, status, weight_key):
    """
    Compute the communities in the neighborhood of node in the graph given
    with the decomposition node2com  K_{i,in}
    """
    weights = {}
    for neighbor, datas in graph[node].items():
        if neighbor != node:
            edge_weight = datas.get(weight_key, 1)
            neighborcom = status.node2com[neighbor]
            weights[neighborcom] = weights.get(neighborcom, 0) + edge_weight

    return weights


def __remove(node, com, weight, status):
    """ Remove node from community com and modify status"""
    status.degrees[com] = (status.degrees.get(com, 0.)
                           - status.gdegrees.get(node, 0.))
    status.internals[com] = float(status.internals.get(com, 0.) -
                                  weight - status.loops.get(node, 0.))
    status.node2com[node] = -1


def __insert(node, com, weight, status):
    """ Insert node into community and modify status"""
    status.node2com[node] = com
    status.degrees[com] = (status.degrees.get(com, 0.) +
                           status.gdegrees.get(node, 0.))
    status.internals[com] = float(status.internals.get(com, 0.) +
                                  weight + status.loops.get(node, 0.))


def __modularity(status):
    """
    Fast compute the modularity of the partition of the graph using
    status precomputed
    """
    links = float(status.total_weight)
    result = 0.
    for community in set(status.node2com.values()):
        in_degree = status.internals.get(community, 0.)
        degree = status.degrees.get(community, 0.)
        if links > 0:
            result += in_degree / links - ((degree / (2. * links)) ** 2)
    return result

if __name__  == "__main__":
    #Basic usage
    #G=nx.erdos_renyi_graph(100, 0.01)
    #part = best_partition(G)

    #other example to display a graph with its community :
    #better with karate_graph() as defined in networkx examples
    #erdos renyi don't have true community structure
    #G = nx.erdos_renyi_graph(30, 0.05)
    #G = nx.karate_club_graph()
    G = gio.graph_reader(cfg.dataDirecoty+'/compress/soc-sign-bitcoinotc.csv')
    #G = gio.graph_reader(cfg.dataDirecoty+'/compress/Highland-tribes.csv')
    #G = gio.graph_reader(cfg.dataDirecoty+'/basic/usSuprimeADJunw.csv')

    print(G.__len__())
    print(len(G.edges()))
    #print(G[1][62])
    #first compute the best partition
    partition = best_partition(G)
    #drawing
    """
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
        count += 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()
    """
    #print (modularity(partition,G))
    print(partition)
    eval.compute_Modularity(G, partition)
