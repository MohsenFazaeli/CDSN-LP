from spla.parser import parameter_parser
from spla.graph_io import graph_reader
import networkx as nx


#from pygraphviz import graphviz_layout

def create_and_run_model(args):
    G = graph_reader(args.input)
    #jtplot.style()

    print G.nodes


    print nx.betweenness_centrality(G)

    labels= { i:{'poslabel':1,'negLabels':-15 } for i in G.nodes}
    print labels
    nx.set_node_attributes(G, labels)





    for n in G.nodes():
        print n

    print G.nodes[1]['poslabel']
    print G.nodes[1]['poslabel']
    print G.nodes[1]['poslabel']

    edges, weights = zip(*nx.get_edge_attributes(G, 'color').items())
    print weights

    #nodes, weights = zip(*nx.nodes(G).items())
    #pos = nx.spring_layout(G)
    #pos = nx.graphviz_layout(G)
    #pos = nx.pygraphviz_layout(G)
    #nx.draw_networkx_labels(G, pos, weights, font_size=16, font_color='r')
    #nx.draw(G, pos, node_color='b', edgelist=edges, edge_color=weights, width=2.0, edge_cmap=plt.cm.Blues)
    #plt.savefig('edges.png')
    #nx.draw(G)
    #plt.show()



    #model = LabelPropagator(graph, args)
    #model.do_a_series_of_propagations()


if __name__ == "__main__":
    args = parameter_parser()
    create_and_run_model(args)



