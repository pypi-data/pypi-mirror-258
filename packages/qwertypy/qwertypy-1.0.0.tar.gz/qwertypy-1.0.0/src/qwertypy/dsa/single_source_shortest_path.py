import heapq

def dijkstra(graph, start, n):
    dist = [float("inf")] * n
    dist[start] = 0

    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue

        for v in graph[u]:
            cur = d + graph[u][v]
            if cur < dist[v]:
                dist[v] = cur
                heapq.heappush(heap, (cur, v))
    
    return dist