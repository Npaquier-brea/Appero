import osmnx as ox
import matplotlib.pyplot as plt
import pickle


def save(graph):
    with open('montreal.obj', 'wb') as file:
        pickle.dump(graph, file)
    print("saved")

def load():
    with open('montreal.obj', 'rb') as file:
       graph = pickle.load(file)
    print("loaded")
    return graph

def main():
    #city = ox.geocode_to_gdf("Montreal",  network_type = "drive")
    #place = "Montreal"
    #city = ox.graph_from_place(place)
    city = load()
    if city == None:
        place = "montreal"
        city = ox.graph_from_place(place)
        save(city)
    print(load)
    ox.plot_graph(city)

if __name__ == "__main__":
    main()