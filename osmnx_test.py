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

def di_dijkstra(i,j, adjlist):
    queue = []
    queue.append(([(i,0)],0))
    smallestweight = MAX
    path = []
    visited = [False] * len(adjlist)
    while queue:
        (current, currentweight) = queue.pop()
        visited[current[-1][0]] = True
        for (voisin, poids) in adjlist[current[-1][0]][1]:
            if visited[voisin] == True:
                continue
            if voisin == j:
                if (currentweight + poids) < smallestweight:
                    smallestweight = currentweight + poids
                    path = current + [(voisin,poids)]
            elif (currentweight + poids) < smallestweight:
                queue.append((current + [(voisin,poids)], currentweight + poids))
    return (smallestweight, path)

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

def change_degre(i, new_degree, adjlist):
    adjlist[i] = new_degree
    return adjlist

def di_addpath(path, adjlist):
    precedent = None
    for (node,poids) in path:
        if precedent == None:
            precedent = node
            continue
        print("precedent = ", end="")
        print(precedent)
        print("node = ", end="")
        print(node)
        print("Degre = ", end="")
        print(adjlist[precedent][0])
        print(adjlist[precedent])
        print(type(adjlist[precedent][0]))
        adjlist[precedent] = (adjlist[precedent][0] -1, adjlist[precedent][1])
        adjlist[node] = (adjlist[node][0] + 1, adjlist[node][1])
        adjlist[precedent][1].append((node, poids))
        precedent = node
    return adjlist

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

def di_optirepair(oddslist_neg, oddslist_pos, adjlist):
    while oddslist_pos:
        smallestpath = (None, None)
        currentdist = MAX
        path = []
        for i in range(0, len(oddslist_pos)):
            for j in range(0, len(oddslist_neg)):
                (tmp, pathtmp) = di_dijkstra(oddslist_pos[i], oddslist_neg[j], adjlist)
                if tmp < currentdist:
                    smallestpath = (oddslist_pos[i], oddslist_neg[j])
                    path = pathtmp
        adjlist = di_addpath(path, adjlist)
        if adjlist[smallestpath[0]][0] == 0:
            oddslist_pos.remove(smallestpath[0])
        if adjlist[smallestpath[1]][0] == 0:
            oddslist_pos.remove(smallestpath[1])
    return adjlist

def optirepair(oddslist, adjlist):
    while oddslist:
        smallestpath = (None, None)
        currentdist = MAX
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

#Fonction to Eulerian

def to_Eulerian(adjlist):
    # [[(n1,p1),(n2, p2)], ...]
    oddslist = []
    for i in range(0,len(adjlist)):
        if len(adjlist[i]) % 2 != 0:
            oddslist.append(i)
    adjlist = optirepair(oddslist, adjlist)
    return adjlist

def Di_to_Eulerian(adjlist):
    # [(D,[(neigbhournode, weight)]), ...]
    oddslist_neg = [] #moins d'arrete entrante que sortante
    oddlist_positif = [] #plus d'arretes entrante que sortante
    for i in range(0,len(adjlist)):
        if adjlist[i][0] < 0:
            oddslist_neg.append(i)
        if adjlist[i][0] > 0:
            oddlist_positif.append(i)
    adjlist = di_optirepair(oddlist_positif, oddslist_neg, adjlist)
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
"""
def DiGraph_to_Di_adjlist(G):
    nodes = list(G.nodes())
    Trad = []
    for node in nodes:
        Trad.append(node)
     
    for (i,j,p) in list(G.edges(data="length", default=1)):
        res(Trad.index(i)][1].append((Trad.index(j),p))
    return (Trad,res)"""

def main():
    #adjlist = [[(1,1),(6,8),(2,3)],[(0,1),(2,1),(4,1)],[(1,1),(3,1),(0,3)],[(2,1),(4,1)],[(3,1),(5,1),(1,1)],[(4,1),(6,1)],[(5,1),(0,8)]]
    #path = dijkstra(0,6, adjlist)
    #print("path found with dijkstra:")
    #print(path)
    """
    path = dijkstra(0,4,adjlist)
    print(path)
    
    adjlist = to_Eulerian(adjlist)
    print("adjlist after repair:")
    print(adjlist) """

    """
    di_adjlist = [(1,[(4,1)]), 
    (-1,[(0,1),(2,1)]),
    (0, [(3,1),(0,1)]),
    (0, [(4,1)]),
    (0, [(1,1),(2,1)])]
    print(di_adjlist)
    (weight, path) = di_dijkstra(0,1, di_adjlist)
    print(path)
    di_adjlist = di_addpath(path, di_adjlist)
    print(di_adjlist)

    #di_adjlist = Di_to_Eulerian(di_adjlist)
    #print(di_adjlist)"""
    place = 'poil'
    city = load(place)

    if city == None:
        city = ox.graph_from_place(place)
        save(city, place)

    city = ox.utils_graph.remove_isolated_nodes(city)
#    (Trad, di_adjlist) =  DiGraph_to_Di_adjlist(city)
#    print(di_adjlist)
    #print(list(city.edges(data=True)))
if __name__ == '__main__':
    main()