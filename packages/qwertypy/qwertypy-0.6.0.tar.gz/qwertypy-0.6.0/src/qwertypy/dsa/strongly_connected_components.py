def tarjan(graph):
    low = {}
    visited = set()
    stack = []
    inStack = set()
    
    def dfs(u):
        visited.add(u)
        low[u] = u
        stack.append(u)
        inStack.add(u)
        
        for v in graph[u]:
            if v not in visited:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif v in inStack:
                low[u] = low[v]
                
        if low[u] == u:
            while u in inStack:
                inStack.remove(stack.pop())
    
    for u in graph:
        if u not in visited: dfs(u)
    return low