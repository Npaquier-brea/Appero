from networkx.algorithms import *
from networkx.readwrite import adjlist
from numpy import integer
import osmnx as ox
import matplotlib.pyplot as plt
import pickle
import os
import MultiDiToAdjEuler as elr
import findpath as find
import Difindpath as Difind

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
    print("isEulerian :", elr.isEulerian(adj))

def This_Is_Reality(city):
    new_city = city.to_undirected()
    if not(ox.is_eulerian(new_city)):
        new_city = ox.eulerize(new_city)  
    L = list(ox.eulerian_circuit(new_city))# On peut ajouter le noeud de départ
    return L
#Stratégie:
# - Diviser notre graphe en plusieurs graph (multiple du nbr de thread) ---HARD---???
# - Compter l'importance total de chaque graph et attribué en fonction un nbr de machine ---EASY---
# - rediviser en fonction du nbr de machine qu'on attribue ---HARD---???
# - puis calculer le chemin eulerien sur chaque graph  ---DONE---

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

    place = 'poil'
    city = load(place)
    if city == None:
        city = ox.graph_from_place(place)
        save(city, place)
    #city = ox.utils_graph.remove_isolated_nodes(city)
    L = This_Is_Reality(city)
    print(L)
    #(Trad, di_adjlist) =  DiGraph_to_Di_adjlist(city)
    #print(di_adjlist)
    #print(list(city.edges(data=True)))
    #adjlist = [[(1,1),(3,1)],[(0,1),(2,1),(3,1),(4,1)],[(1,1),(3,1)],[(2,1),(0,1),(1,1),(4,1)],[(1,1),(3,1)]]
    #to adjlist = [[(1,1,0),(3,1,2)],[(0,1,4),(2,1,0),(3,1,0),(4,1,5)],[(1,1,10),(3,1,7)],[(2,1,8),(0,1,7),(1,1,6),(4,1,1)],[(1,1,2),(3,1,4)]] [[(v,l,n),...],...]
    #find.remove_edge(adjlist, 0, 1, 1)
    #print(adjlist)

    #L = find.Euler(adjlist)
    #print(L)
    """
    di_adjlist = [(1,[(4,1)]), 
    (-1,[(0,1),(2,1)]),
    (0, [(3,1),(0,1)]),
    (0, [(4,1)]),
    (0, [(1,1),(2,1)])]
    print("############################")
    for e in di_adjlist:
        print(e)
    elr.Di_to_Eulerian(di_adjlist)
    for e in di_adjlist:
        print(e)
    #print(di_adjlist)
    print("############################")
    print("Euler: ")
    #L = Difind.Euler(di_adjlist)
    EulerianCycle = Difind.FindDIEulerianCycle(di_adjlist)
    for i in range(len(EulerianCycle)):
        print(EulerianCycle[i])
    #for e in L:
    #    print("\t",e)
    print("############################")
    #print(L)
    """


if __name__ == '__main__':
    main()