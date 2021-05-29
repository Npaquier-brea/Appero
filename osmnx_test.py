from networkx.algorithms.components import connected
from networkx.readwrite import adjlist
from numpy import integer
import osmnx as ox
import matplotlib.pyplot as plt
import pickle
import os

DIR = 'data'
MAX = 9223372036854775807

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
    #print("adjlist in dijkstra:")
    #print(adjlist)
    queue = []
    queue.append(([(i,0)],0))
    smallestweight = MAX
    path = []
    visited = [False] * len(adjlist)
    while queue:
        (current, currentweight) = queue.pop()
        visited[current[-1][0]] = True
        for (voisin, poids) in adjlist[current[-1][0]]:
            if visited[voisin] == True:
                continue
            if voisin == j:
                if (currentweight + poids) < smallestweight:
                    smallestweight = currentweight + poids
                    path = current + [(voisin,poids)]
            elif (currentweight + poids) < smallestweight:
                queue.append((current + [(voisin,poids)], currentweight + poids))
    return (smallestweight, path)

def addpath(path, adjlist):
    precedent = None
    for (node,poids) in path:
        if precedent == None:
            precedent = node
            continue
        adjlist[precedent].append((node, poids))
        adjlist[node].append((precedent, poids))
        precedent = node
    return adjlist

def optirepair(oddslist, adjlist):
    #Amelioration de temps mais perte d'opti de trajet:
    #Chercher le chemin le plus cours pour oddlist[0] jusqu'à [1] while oddlist
    while oddslist:
        print(oddslist)
        smallestpath = (None, None)
        currentdist = 20000 #tester avec MAX une fois que ça marche
        path =[]
        for i in range(0,len(oddslist)-1):
            for j in range (i+1, len(oddslist)):       
                (tmp, pathtmp) = dijkstra(oddslist[i],oddslist[j], adjlist)
                if tmp < currentdist:
                    smallestpath = (oddslist[i],oddslist[j])
                    currentdist = tmp
                    path = pathtmp
        addjlist = addpath(path, adjlist)
        print(smallestpath)
        oddslist.remove(smallestpath[0])
        oddslist.remove(smallestpath[1])
    return adjlist

def fasterrepair(oddslist, adjlist):
    #Amelioration de temps mais perte d'opti de trajet:
    #Chercher le chemin le plus cours pour oddlist[0] jusqu'à [1] while oddlist
    print("start repair")
    while oddslist:
        path =[]
        (tmp, pathtmp) = dijkstra(oddslist[0],oddslist[1], adjlist)
        smallestpath = (oddslist[0],oddslist[1])
        currentdist = tmp
        path = pathtmp
        addjlist = addpath(path, adjlist)
        oddslist.remove(smallestpath[0])
        oddslist.remove(smallestpath[1])
    print("repair ending")
    return adjlist

def to_Eulerian(adjlist):
    oddslist = []
    for i in range(0,len(adjlist)):
        if len(adjlist[i]) % 2 != 0:
            oddslist.append(i)
    #print("oddslist:")
    #print(oddslist)
    adjlist = optirepair(oddslist, adjlist)
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
    adjlist = [[(1,1),(6,8),(2,3)],[(0,1),(2,1),(4,1)],[(1,1),(3,1),(0,3)],[(2,1),(4,1)],[(3,1),(5,1),(1,1)],[(4,1),(6,1)],[(5,1),(0,8)]]
    #path = dijkstra(0,6, adjlist)
    #print("path found with dijkstra:")
    #print(path)
    """
    path = dijkstra(0,4,adjlist)
    print(path)
    """
    adjlist = to_Eulerian(adjlist)
    print("adjlist after repair:")
    print(adjlist)

if __name__ == '__main__':
    main()