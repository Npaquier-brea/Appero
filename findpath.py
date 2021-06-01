#NON DI
def add_edge(adjlist, start, to, weight, amountofsnow, importance):
    #print("add:",end='')
    #print(start,end='-')
    #print(to)
    #print("add:",end='')
    #print(to,end='-')
    #print(start)
    adjlist[start].append((to, weight, amountofsnow, importance))
    adjlist[to].append((start, weight,amountofsnow, importance))

def remove_edge(adjlist, start, to, weight, amountofsnow, importance):
    #adjlist[start].remove((to,weight))
    #print(adjlist)
    for i in range(len(adjlist[start])):
        (node, poids, amountofsnowtmp, importancetmp) = adjlist[start][i]
        if node == to and poids == weight and amountofsnowtmp == amountofsnow and importancetmp == importance:
            #print("remove:",end='')
            #print(node,end='-')
            #print(start)
            adjlist[start].pop(i)
            break
    #adjlist[to].remove((start, weight))
    for j in range(len(adjlist[to])):
        (node, poids, amountofsnowtmp, importancetmp) = adjlist[to][j]
        if node == start and poids == weight and amountofsnowtmp == amountofsnow and importancetmp == importance:
            #print("remove:",end='')
            #print(node,end='-')
            #print(to)
            adjlist[to].pop(j)
            break

def Reachable(adjlist,u, visited):
    res = 1
    visited[u]= True
    for (node, weight, tmp, tmp1) in adjlist[u]:
        if visited[node] == False:
            res+= Reachable(adjlist, node, visited)
    return res

def isValidNext(adjlist, u, v, weight,amountofsnow, importance):
    if len(adjlist[u]) == 1:
        return True
    visited = [False]*len(adjlist)
    reachable1 = Reachable(adjlist, u, visited)

    remove_edge(adjlist, u, v, weight, amountofsnow, importance)
    visited = [False]*len(adjlist)
    reachable2 = Reachable(adjlist, u, visited)

    add_edge(adjlist, u, v, weight, amountofsnow, importance)

    return False if reachable1 > reachable2 else True

def addifedge(resadjlist, u, node, weight, amountofsnow, importance):
    if amountofsnow > 2 and amountofsnow < 16:
        resadjlist[u].append((node,weight, amountofsnow, importance))
        resadjlist[node].append((u, weight, amountofsnow, importance))

def EulerFromNode(adjlist, u, L,resadjlist):
    for (node, weight, amountofsnow, importance) in adjlist[u]:
        #print("Euler node:",u)
        #verif = isValidNext(adjlist, u, node, weight, amountofsnow, importance)
        #print(u,"-",node,"=",verif)
        if isValidNext(adjlist, u, node, weight, amountofsnow, importance):          
            L.append((u, node))
            addifedge(resadjlist, u, node, weight, amountofsnow,importance)
            remove_edge(adjlist, u, node, weight, amountofsnow, importance)
            EulerFromNode(adjlist, node, L, resadjlist)
            break

def removeisolatenode(adjlist):
    for i in range(len(adjlist)):
        if adjlist[i] == []:
            adjlist.pop(i)             

def Euler(adjlist):
    u=0
    res = []
    resadjlist = []
    for i in range (len(adjlist)):
        resadjlist.append([])
    for i in range(len(adjlist)):
        if len(adjlist[i]) %2 != 0:
            u = i
            break
    EulerFromNode(adjlist,u,res, resadjlist)
    #removeisolatenode(resadjlist)
    return (res,resadjlist)