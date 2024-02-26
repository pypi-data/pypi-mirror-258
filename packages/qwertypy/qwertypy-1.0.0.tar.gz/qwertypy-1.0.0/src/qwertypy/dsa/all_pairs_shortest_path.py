def fw(graph, n):
    dist = [[float("inf")] * n for _ in range(n)]

    for i in range(n): dist[i][i] = 0

    for u in graph:
        for v in graph[u]:
            dist[u][v] = graph[u][v]

    for k in range(n):
        for i in range(n):
            if i == k: continue
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist