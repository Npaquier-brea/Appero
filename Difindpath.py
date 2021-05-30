#DI
def add_edge(adjlist, start, to, weight):
    adjlist[start][1].append((to, weight))
def remove_edge(adjlist, start, to, weight):
    #adjlist[start].remove((to,weight))
    #print(adjlist)
    for i in range(len(adjlist[start][1])):
        (node, poids) = adjlist[start][1][i]
        if node == to and poids == weight:
            adjlist[start][1].pop(i)
            break

def Reachable(adjlist,u, visited):
    res = 1
    visited[u]= True
    for (node, weight) in adjlist[u][1]:
        if visited[node] == False:
            res+= Reachable(adjlist, node, visited)
    return res

def isValidNext(adjlist, u, v, weight):
    if len(adjlist[u][1]) == 1:
        return True
    visited = [False]*len(adjlist)
    reachable1 = Reachable(adjlist, u, visited)

    remove_edge(adjlist, u, v, weight)
    visited = [False]*len(adjlist)
    reachable2 = Reachable(adjlist, u, visited)

    add_edge(adjlist, u, v, weight)

    return False if reachable1 > reachable2 else True

def EulerFromNode(adjlist, u, L):
    print("node = ", u, "\nadjlist = ",adjlist, "\nL = ",L)
    for (node, weight) in adjlist[u][1]:
        #print("Euler node:",u)
        #verif = isValidNext(adjlist, u, node, weight)
        #print(u,"-",node,"=",verif)
        if isValidNext(adjlist, u, node, weight):          
            L.append((u, node))
            remove_edge(adjlist, u, node, weight)
            EulerFromNode(adjlist, node, L)
            break

def Euler(adjlist):
    u=0
    res = []
    for i in range(len(adjlist)):
        if adjlist[i][0] %2 != 0:
            u = i
            break
    EulerFromNode(adjlist,u,res)
    return res

def FindDIEulerianCycle(adjList): # [(degree, [(voisins, poids), ...]), ...] |
    if len(adjList) == 0:
        return []
    current_path = [0]
    cycle = []
    EulerianCycle = []
    while current_path:
        curr_v = current_path[-1]
        if adjList[curr_v][1]:
           next_v = adjList[curr_v][1].pop()
           current_path.append(next_v[0])
        else:
            cycle.append(current_path.pop())
    for i in range(len(cycle) - 1, -1, -1):
        EulerianCycle.append(cycle[i])
    return EulerianCycle