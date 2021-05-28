from networkx.readwrite import adjlist
from numpy import integer
import osmnx as ox
import matplotlib.pyplot as plt
import pickle
import os

DIR = 'data'

def save(graph, place):
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    with open('data/' + place + '.obj', 'wb') as file:
        pickle.dump(graph, file)

    print('saved')


def load(place):
    try:
        with open('data/' + place + '.obj', 'rb') as file:
           graph = pickle.load(file)

        print('loaded')
        return graph

    except:
        return None

def isEulerian(adjList):
    count = 0
    for e in adjList:
        if len(e) % 2 != 0:
            count += 1
        if count > 2:
            return False
    return True

def is_connected(G):
    node = G[0][0]
    verif = [len(G.__len__())] * False
    queue = []
    queue.append(node)
    while queue:
        tmp = queue.pop()
        for a in tmp.adjacency():
            if verif[a]:
              continue
            verif[a] = True
            queue.append(a)
    return not False in verif

def dijkstra(i,j, adjlist):
    queue = []
    queue.append(([i],0))
    smallestweight = 20000
    path = []
    while queue:
        (current, currentweight) = queue.pop()
        for (voisin, poids) in  adjlist[current[-1]]:
            if voisin == j:
                if (currentweight + poids) < smallestweight:
                    smallestweight = currentweight + poids
                    path = current
            elif (currentweight + poids) < smallestweight:
                queue.append((current + [voisin] ,currentweight + poids))
    return path

def addpath(path, adjlist):
    for i in path:
        adjlist[i[1]].append((i[0], i[2]))
        adjlist[i[0]].append((i[1], i[2]))
    return adjlist

def repair(oddslist, adjlist):
    while oddslist:
        smallestpath = (0, 1)
        currentdist = integer.max
        path =[]
        for i in range(len(oddslist)-1):
            for j in range (i+1, len(oddslist)):
                (tmp, pathtmp) = dijkstra(i,j, adjlist)
                if tmp < currentdist:
                    smallestpath = (i,j)
                    currentdist = tmp
                    path = pathtmp
        addjlist = addpath(path, adjlist)
        oddslist.remove(smallestpath[0])
        oddslist.remove(smallestpath[1])

def to_Eulerian(adjlist):
    oddslist = []
    for i in len(adjlist):
        if len(adjlist[i]) % 2 != 1:
            oddslist.append(i)
    repair(oddslist, adjlist)
    return adjlist

def NodesToList(G):
    resList = []
    nodes = list(G.nodes())
    for (count, node) in enumerate(nodes):
        resList.append((count, node))
    return resList

def main1():
    #city = ox.geocode_to_gdf("Montreal",  network_type = "drive")
    place = 'Rochefourchat'
    city = load(place)

    if city == None:
        city = ox.graph_from_place(place)
        save(city, place)

    city = ox.utils_graph.remove_isolated_nodes(city)
    adj = []
    nodes = list(city.nodes)
    for src, dst in city.adjacency():
        succ = []
        for key in dst.keys():
            succ.append(nodes.index(key))
        adj.append(succ)

    print(adj)
    number_of_nodes = len(adj)
    print("'" + place + "'", "has", number_of_nodes, "of nodes and",  len(city.edges()), "edges")
    print("isEulerian :", isEulerian(adj))

def main():
    adjlist = [[(1,1),(6,8)],[(0,1),(2,1)],[(1,1),(3,1)],[(2,1),(4,1)],[(3,1),(5,1)],[(4,1),(6,1)],[(5,1),(0,8)]]
    path = dijkstra(0,6, adjlist)
    print(path)

if __name__ == '__main__':
    main()