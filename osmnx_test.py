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

def NodesToList(G):
    resList = []
    nodes = list(G.nodes())
    for (count, node) in enumerate(nodes):
        resList.append((count, node))
    return resList

def main():
    #city = ox.geocode_to_gdf("Montreal",  network_type = "drive")
    place = 'Rochefourchat'
    city = load(place)

    if city == None:
        city = ox.graph_from_place(place)
        G = ox.utils_graph.remove_isolated_nodes(city)
        list = NodesToList(G)
        for (a, b) in list:
            print((a, b))
        save(city, place)
    print(load)
    ox.plot_graph(city)

if __name__ == '__main__':
    main()