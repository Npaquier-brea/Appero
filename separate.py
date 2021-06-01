import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

def adjlist(G):
    adj = []
    nodes = list(G.nodes)
    for src, dst in G.adjacency():
        succ = []
        for key in dst.keys():
            succ.append(nodes.index(key))
        adj.append(succ)
    return adj

def edge_to_remove(G):
    dict1 = nx.edge_betweenness_centrality(G)
    list_of_tuples = sorted(dict1.items(), key = lambda x:x[1], reverse = True)
    return list_of_tuples[0][0]

def girvan(G):
    c = list(G.subgraph(c) for c in nx.strongly_connected_components(G))
    l = len(c)
    print('The number of connected components are ', l)

    while l <= 1:
        G.remove_edge(*edge_to_remove(G))
        c = list(G.subgraph(c) for c in nx.strongly_connected_components(G))
        l = len(c)
        print('The number of connected components are ', l)

    return c

place = 'Sus, France'
city = ox.graph_from_place(place)
city = ox.utils_graph.remove_isolated_nodes(city)
#city = city.to_undirected()
c = girvan(city.copy())

ox.plot_graph(city)
print(city.edges)
sum_len = 0

for i in c:
    print(adjlist(i))
    sum_len += len(i.edges)

    ox.plot_graph(i)
    print('..........')

print(len(city.edges), sum_len)