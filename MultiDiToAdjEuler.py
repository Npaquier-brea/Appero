from networkx.algorithms.components import connected
from networkx.readwrite import adjlist
from numpy import integer
import osmnx as ox
import matplotlib.pyplot as plt
import pickle
import os
import time
MAX = 9223372036854775807
def isEulerian(adjList):
    count = 0
    for e in adjList:
        if len(e) % 2 != 0:
            count += 1
        if count > 2:
            return False
    return True

def is_DiEulerian(adjList):
    D1 = None
    D2 = None
    for e in adjList:
        if e[1] != 0:
            if D1 == None:
                D1 = e[1]
            elif D2 == None:
                D2 = e[1]
            else:
                return False
    return True if (D1 == -1 and D2 == 1) or (D2 == 1 and D2 == -1) else False

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
    #print("DIJKSTRA")
    queue = []
    queue.append(([(i,0)],0))
    smallestweight = 2000 #remettre MAX une fois que ça marche
    path = []
    visited = [False] * len(adjlist)
    while queue:
        #print("Boucle:")
        #print("\tqueue = ",queue)
        (current, currentweight) = queue.pop()
        print(current)
        visited[current[-1][0]] = True
        #print("\tcurrent = ",current)
        #print("\t CurrentAdj = ",adjlist[current[-1][0]])
        print("Adj[Current] = ",adjlist[current[-1][0]])
        for (voisin, poids) in adjlist[current[-1][0]][1]:
            if visited[voisin] == True:
                continue
            if voisin == j:
                if (currentweight + poids) < smallestweight:
                    smallestweight = currentweight + poids
                    path = current + [(voisin,poids)]
            elif (currentweight + poids) < smallestweight:
                queue.append((current + [(voisin,poids)], currentweight + poids))
        time.sleep(4)
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
    print("path :", path)
    precedent = None
    for (node,poids) in path:
        if precedent == None:
            precedent = node
            continue
        print("\tprecedent = ",precedent)
        print("\tnode = ",node)
        print("\tDegre = ", adjlist[precedent][0])
        print(type(adjlist[precedent][0]))
        adjlist[precedent] = (adjlist[precedent][0] +1, adjlist[precedent][1])
        adjlist[node] = (adjlist[node][0] - 1, adjlist[node][1])
        adjlist[node][1].append((precedent, poids))
        precedent = node

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
    print("Starting Repair")
    print(oddslist_neg)
    print(oddslist_pos)
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
        di_addpath(path, adjlist)
        if adjlist[smallestpath[0]][0] == 0:
            oddslist_pos.remove(smallestpath[0])
        if adjlist[smallestpath[1]][0] == 0:
            oddslist_neg.remove(smallestpath[1])
    print("Repair Ending")

def optirepair(oddslist, adjlist):
    print("Starting Repair")
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
        oddslist.remove(smallestpath[0])
        oddslist.remove(smallestpath[1])
    print("Repair Ending")
    return adjlist

def fasterrepair(oddslist, adjlist):
    #Amelioration de temps mais perte d'opti de trajet:
    #Chercher le chemin le plus cours pour oddlist[0] jusqu'à [1] while oddlist
    while oddslist:
        path =[]
        (tmp, pathtmp) = dijkstra(oddslist[0],oddslist[1], adjlist)
        smallestpath = (oddslist[0],oddslist[1])
        currentdist = tmp
        path = pathtmp
        addjlist = addpath(path, adjlist)
        oddslist.remove(smallestpath[0])
        oddslist.remove(smallestpath[1])
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
    di_optirepair(oddlist_positif, oddslist_neg, adjlist)

def NodesToList(G):
    resList = []
    nodes = list(G.nodes())
    for (count, node) in enumerate(nodes):
        resList.append((count, node))
    return resList


def DiGraph_to_adjlist(G):
    nodes = list(G.nodes())
    Trad = []
    res = []
    for node in nodes:
        Trad.append(node)
        res.append([])
    for (i,j,p) in list(G.edges(data="length", default=1)):
        res[Trad.index(i)].append((Trad.index(j),p))
    return (Trad,res)

def DiGraph_to_Diadjlist(G):
    nodes = list(G.nodes())
    Trad = []
    res = []
    for node in nodes:
        Trad.append(node)
        res.append((G.degree(node),[]))
    for (i,j,p) in list(G.edges(data="length", default=1)):
        res[Trad.index(i)][1].append((Trad.index(j),p))
    return (Trad,res)


