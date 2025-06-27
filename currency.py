from collections import defaultdict, deque

def build_graph(rates): #O(E)
    graph = defaultdict(list)
    for src, dst, rate in rates:
        graph[src].append((dst, rate))
        graph[dst].append((src, 1 / rate))  # assume reversibility
    return graph

def find_conversion_rate(rates, query): #O(v+e)
    graph = build_graph(rates)
    src, dst = query

    if src not in graph or dst not in graph:
        return -1  # currency not in graph

    # BFS to find conversion
    visited = set()
    queue = deque([(src, 1.0)])

    while queue:
        current, product = queue.popleft()
        if current == dst:
            return round(product, 4)
        visited.add(current)
        for neighbor, rate in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, product * rate))

    return -1  # path not found
