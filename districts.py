import osmnx as ox
import networkx as nx
import MultiDiToAdjEuler as utils
import Difindcycle as di
import divide as div
import threading
import pickle
import os
import time
import random

DIR = 'data'

def save(graph, place):
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    with open('data/' + place + '.obj', 'wb') as file:
        pickle.dump(graph, file)

    #print('saved ' + place)


def load(place):
    try:
        with open('data/' + place + '.obj', 'rb') as file:
           graph = pickle.load(file)

        #print('loaded ' + place)
        return graph

    except:
        return None
    
def get_graph(place):
    graph = load(place)

    if graph == None:
        graph = ox.graph_from_place(place, network_type='drive')
        save(graph, place)
        
    return graph

def save_route(route, place):
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    with open('routes/' + place + '.route', 'wb') as file:
        pickle.dump(route, file)


def load_route(place):
    try:
        with open('routes/' + place + '.route', 'rb') as file:
           route = pickle.load(file)

        return route

    except:
        return None

def get_route(graph, place):
    route = load_route(place)

    if route == None:
        route = graph_to_route(graph)
        save_route(route, place)
        
    return route


def colors(n):
    cols = []
    for i in range(n):
        if i % 4 == 0:
            cols.append('r')
        elif i % 4 == 1:
            cols.append('y')
        elif i % 4 == 2:
            cols.append('g')
        else:
            cols.append('b')
    return cols

def rdm_color(n):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(n)]
    return color
        
def traduction(path, trad):
    new_path = []
    for i in path:
        new_path.append(trad[i])
    return new_path

def graph_to_route(G):
    trad, diadj = utils.DiGraph_to_Diadjlist(G)
    utils.Di_to_Eulerian(diadj)
    cycle = di.get_cycle(diadj)
    path = traduction(cycle, trad)
    return path

def read(): #modifier le read
    L = []
    f = open("quartier.txt", "r")
    for line in f:
        #tmp = line.split(" ")
        #for quart in tmp:
            #L.append(quart)
        if line[len(line) - 1] == "\n":
            L.append(line[:-1])
        else:
            L.append(line)
    return L

class myThread(threading.Thread):
    def __init__(self, district, routes):
        threading.Thread.__init__(self)
        self.district = district
        self.routes = routes

    def run(self):
        print("starting " + self.district)
        graph = get_graph(self.district + ", Montreal, Canada")
        #print(self.district + ": " + str(len(graph.nodes)) + " node")
        route = get_route(graph, self.district)
        self.routes.append((route, self.district))
        print("finished " + self.district)

t = time.time()

districts = read()
#districts =  ['Tetreaultville', 'Rene-Levesque', 'Nouveau-Bordeau', 'Upper Lachine', 'Hodge']
#districts = ['Edouard-Montpetit', 'LaSalle']

routes = []
i = 0

threads = []
while i < len(districts):
    if len(threads) < 5:
        thread = myThread(districts[i], routes)
        thread.start()
        threads.append(thread)
        i += 1
    
    for thread in threads:
        if not thread.is_alive():
            threads.remove(thread)
        
for thread in threads:
    thread.join()
    
montreal = get_graph('Montreal')
montreal = montreal.to_undirected()
    
edges = div.edgelist(montreal)

final_routes = []

for route, name in routes:
    print("compat " + name)
    new_route = [route[0]]
    for i in range(len(route) - 1):
        if (route[i], route[i+1]) not in edges and (route[i+1], route[i]) not in edges :
            print(route[i], route[i+1])
            if len(new_route) >= 2:
                print("seg")
                final_routes.append(new_route)
            new_route = []
        else:
            new_route.append(route[i+1])

    final_routes.append(new_route)
        
"""
for route, name in routes:
    print("compat " + name)
    compat = True
    for i in range(len(route) - 1):
        if (route[i], route[i+1]) not in edges and (route[i+1], route[i]) not in edges:
            compat = False
            print("fail")
            break
    if compat:
        final_routes.append(route)
        print("pass")"""
                    
                    
fig, ax = ox.plot_graph_routes(montreal, final_routes, route_colors=rdm_color(len(final_routes)), route_linewidth=1, node_size=0)

print("total time: ", time.time() - t)
    
"""
for i in range(len(districts)):
     districts[i] += ", Montreal, Canada"

places = ox.geocode_to_gdf(districts)
ax = ox.project_gdf(places).plot()
_ = ax.axis('off')

places = ox.geocode_to_gdf('Montreal')
ax = ox.project_gdf(places).plot()
_ = ax.axis('off')"""