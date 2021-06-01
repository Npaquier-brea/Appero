import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

def read():
    L = []
    f = open("quartier.txt", "r")
    for line in f:
        #tmp = line.split(" ")
        #for quart in tmp:
            #L.append(quart)
        L.append(line[:-1])
    return L

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
    G = G.to_undirected()
    c = list(G.subgraph(c) for c in nx.connected_components(G))
    l = len(c)
    print('The number of connected components are ', l)
    l1 = l
    while l1 == l:
        G.remove_edge(*edge_to_remove(G))
        c = list(G.subgraph(c) for c in nx.connected_components(G))
        l1 = len(c)
        print('The number of connected components are ', l)

    return c
#L = read()
#print(L)

place = 'Snowdon    Cote-des-Neiges–Notre-Dame-de-Grace, Montreal'
tmpcity = ox.graph_from_place(place,network_type="drive")
tmpcity = ox.utils_graph.remove_isolated_nodes(tmpcity)
city = tmpcity.to_undirected()
print(city.order())
print(7/3)
print(7//3)
ox.plot_graph(city)
"""
c = girvan(city)
sum_len = 0
left = c[0].copy()
right = c[1].copy()
print("edges: " + str(len(city.edges)))
c = 0
print("city :",city.order())
print("left :",left.order())
print("right:",right.order())

for edge in city.edges:
    c += 1
    if c % 100 == 0:
        print(c)
    if not edge in left.edges and not edge in right.edges:
        node1, node2, _ = edge
        if node1 in left.nodes:
            dic = dict(city.nodes(data = True))
            data = dic[node2]
            left.add_node(node2, x = data['x'], y = data['y'])
        else:
            dic = dict(city.nodes(data = True))
            data = dic[node1]
            left.add_node(node1, x = data['x'], y = data['y'])
        left.add_edge(*edge)

for i in [left, right]:
    print(1)
    sum_len += len(i.edges)

    ox.plot_graph(i)
    print('..........')

print(len(city.edges), sum_len)"""