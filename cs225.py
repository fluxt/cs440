BFS(G, v):
    Queue q
    setLabel(v, VISITED)
    q.enqueue(v)
    while !q.empty():
        v = q.dequeue()
        for Vertex w in G.adjacent(v):
            if getLabel(w) == UNEXPLORED:
                setLabel(v, w, DISCOVERY)
                setLabel(w, VISITED)
                q.enqueue(w)
            else if getLabel(v, w) == UNEXPLORED:
                setLabel(v, w, CROSS)



DFS(G, v):
    setLabel(v, VISITED)
    for Vertex w in G.adjacent(v):
        if getLabel(w) == UNEXPLORED:
            setLabel(v, w, DISCOVERY)
            DFS(G, w)
        else if getLabel(v, w) == UNEXPLORED:
            setLabel(v, w, BACK)



KrushalMST(G):
    DisjointSets forest
    for Vertex v in G:
        forest.makeSet(v)

    PriorityQueue Q
    for Edge e in G:
        Q.insert(e)

    Graph T = (V, {})
    while T.edges().size() < n-1:
        Vertex(u, v) = Q.removeMin()
        if forest.find(u) != forest.find(v):
            T.addEdge(u, v)
            forest.union( forest.find(u), forest.find(v) )

    return T



PrimMST(G, s):
    for Vertex v in G:
        d[v] = +inf
        p[v] = NULL
        d[s] = 0

    PriorityQueue Q
    Q.buildHeap(G.vertices())
    Graph T

    for i in n:
        Vertex m = Q.removeMin()
        T.add(m)
        for Vertex v in neighbors of m not in T:
            if cost(m, v) < d[v]:
                d[v] = cost(v, m)
                p[v] = m

    return T



# No Negative Edge Weights
DijkstraSSSP(G, s):
    for Vertex v in G:
        d[v] = +inf
        p[v] = NULL
        d[s] = 0

    PriorityQueue Q
    Q.buildHeap(G.vertices())
    Graph T

    for i in n:
        Vertex m = Q.removeMin()
        T.add(m)
        for Vertex v in neighbors of m not in T:
            if cost(u, v) + d[m] < d[v]:
                d[v] = cost(v, m) + d[m]
                p[v] = m



FloydWarshall(G):
    # Let d be a adj. matrix initialized to +inf
    for Vertex v in G:
        d[v][v] = 0
    for Edge (u, v) in G:
        d[u][v] = cost(u, v)

    for Vertex u in G:
        for Vertex v in G:
            for Vertex w in G:
                if d[u][v] > d[u][w] + d[w][v]:
                    d[u][v] = d[u][w] + d[w][v]

    return d
