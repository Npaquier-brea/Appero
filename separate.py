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

    while l < 2:
        G.remove_edge(*edge_to_remove(G))
        c = list(G.subgraph(c) for c in nx.strongly_connected_components(G))
        l = len(c)
        print('The number of connected components are ', l)

    return c

place = 'Saint-Nazaire, France'
city = ox.graph_from_place(place)
city = ox.utils_graph.remove_isolated_nodes(city)
#city = city.to_undirected()
c = girvan(city.copy())

ox.plot_graph(city)
print(city.edges)
sum_len = 0

left = c[0].copy()
right = c[1].copy()

print("edges: " + str(len(city.edges)))

c = 0
for edge in city.edges:
    c += 1
    if c % 100 == 0:
        print(c)
    if not edge in left.edges and not edge in right.edges:
        node1, node2, _ = edge
        if node1 in left.nodes:
            dic = dict(city.nodes(data = True))
            data = dic[node1]
            left.add_node(node1, x = data['x'], y = data['y'])
        else:
            dic = dict(city.nodes(data = True))
            data = dic[node2]
            left.add_node(node2, x = data['x'], y = data['y'])
        left.add_edge(*edge)

for i in [left, right]:
    print(adjlist(i))
    sum_len += len(i.edges)

    ox.plot_graph(i)
    print('..........')

print(len(city.edges), sum_len)