def tarjanUndirected(graph):
    low = {}
    idx  = {}
    current_id = 0
    visited = set()
    stack = []
    inStack = set()
    
    def dfs(node, parent):
        nonlocal current_id
        low[node] = idx[node] = current_id
        current_id += 1
        
        visited.add(node)
        stack.append(node)
        inStack.add(node)
        
        for v in graph[node]:
            if v == parent: continue
            if v not in visited:
                dfs(v, node)
                low[node] = min(low[node], low[v])
            elif v in inStack:
                low[node] = min(low[node], idx[v])
                
        if low[node] == idx[node]:
            while node in inStack:
                v = stack.pop()
                low[v] = low[node]
                inStack.remove(v)
    
    for u in list(graph.keys()):
        if u not in visited: dfs(u, None)
    return low