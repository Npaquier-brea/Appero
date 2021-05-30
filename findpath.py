#NON DI
def add_edge(adjlist, start, to, weight):
    #print("add:",end='')
    #print(start,end='-')
    #print(to)
    #print("add:",end='')
    #print(to,end='-')
    #print(start)
    adjlist[start].append((to, weight))
    adjlist[to].append((start, weight))

def remove_edge(adjlist, start, to, weight):
    #adjlist[start].remove((to,weight))
    #print(adjlist)
    for i in range(len(adjlist[start])):
        (node, poids) = adjlist[start][i]
        if node == to and poids == weight:
            #print("remove:",end='')
            #print(node,end='-')
            #print(start)
            adjlist[start].pop(i)
            break
    #adjlist[to].remove((start, weight))
    for j in range(len(adjlist[to])):
        (node, poids) = adjlist[to][j]
        if node == start and poids == weight:
            #print("remove:",end='')
            #print(node,end='-')
            #print(to)
            adjlist[to].pop(j)
            break

def Reachable(adjlist,u, visited):
    res = 1
    visited[u]= True
    for (node, weight) in adjlist[u]:
        if visited[node] == False:
            res+= Reachable(adjlist, node, visited)
    return res

def isValidNext(adjlist, u, v, weight):
    if len(adjlist[u]) == 1:
        return True
    visited = [False]*len(adjlist)
    reachable1 = Reachable(adjlist, u, visited)

    remove_edge(adjlist, u, v, weight)
    visited = [False]*len(adjlist)
    reachable2 = Reachable(adjlist, u, visited)

    add_edge(adjlist, u, v, weight)

    return False if reachable1 > reachable2 else True

def EulerFromNode(adjlist, u, L):
    for (node, weight) in adjlist[u]:
        #print("Euler node:",u)
        verif = isValidNext(adjlist, u, node, weight)
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
        if len(adjlist[i]) %2 != 0:
            u = i
            break
    EulerFromNode(adjlist,u,res)
    return res