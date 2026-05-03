''' CS 361: Project 2
Dijkstra's Algorithm implementation using a priority queue

Kiana Tarter and Neveah Martinez

'''

import heapq
import time

# Syntax: {src: { neighbor: weight} }
sparse_1 = {
    'A' : {'B': 4, 'C' : 2},
    'B' : {'D' : 5},
    'C' : {'D' : 1},
    'D' : {'E' : 3},
    'E' : {'F' : 2},
    'F' : {}
}

sparse_2 = {
    '1' : {'2' : 3, '3' : 6},
    '2' : {'4' : 2, '5' : 5},
    '3' : {'5' : 4},
    '4' : {'6' : 7},
    '5' : {'7' : 1},
    '6' : {},
    '7' : {}
}

dense_1 = {
    'A' : {'B' : 2, 'C' : 5, 'D' : 1, 'E' : 4},
    'B' : {'C' : 3, 'D' : 2, 'E' : 6},
    'C' : {'D' : 3, 'E' : 1},
    'D' : {'E' : 2}
}

dense_2 = {
    '1' : {'2' : 3, '3' : 2, '5' : 5},
    '2' : {'3' : 1, '4' : 2, '5' : 4},
    '3' : {'4' : 3, '5' : 6},
    '4' : {'5' : 2},
    '5' : {'6' : 1},
    '6' : {}
}



def priority_queue_dij(adj, src): 
    start = time.perf_counter()
    # set all elements of solution to infinity initially
    dist = {v: float('inf') for v in adj}
    
    # set the path from the source to itself to 0
    dist[src] = 0

    queue = [(0,src)]

    while queue: 
        d, u = heapq.heappop(queue)

        if (d > dist[u]):
            continue

        for vertex, cost in adj[u].items():

            if dist[u] + cost < dist[vertex]:
                dist[vertex] = dist[u] + cost
                heapq.heappush(queue, (dist[vertex], vertex))

    end = time.perf_counter()
    total_time = end - start
    print(f"Time: {total_time * 1000: .6f} seconds")
    return dist

'''
Helper function to ensure that graphs are undirected
'''
def undirected(graph):
    new_graph = {}

    for u in graph:
        if u not in new_graph:
            new_graph[u] = {}

        for v, w in graph[u].items():
            new_graph[u][v] = w

            if v not in new_graph:
                new_graph[v] = {}

            new_graph[v][u] = w

    return new_graph

'''
Helper function to benchmark runtimes
'''
def benchmark(graph, src, trials=5):
    times = []

    for _ in range(trials):
        start = time.perf_counter()
        priority_queue_dij(graph, src)
        end = time.perf_counter()

        times.append(end-start)
    avg_time = sum(times) / trials
    return avg_time * 1000

'''
Main program to run implementation
'''
def main():
    sparse_1_graph = undirected(sparse_1)
    sparse_2_graph = undirected(sparse_2)
    dense_1_graph = undirected(dense_1)
    dense_2_graph = undirected(dense_2)

    
    print("------SPARSE GRAPH 1:-------")
    print(benchmark(sparse_1_graph, 'A'))

    print("------SPARSE GRAPH 2:--------")
    print(benchmark(sparse_2_graph, '1'))

    print("------DENSE GRAPH 1:----------")
    print(benchmark(dense_1_graph, 'A'))

    print("------DENSE GRAPH 2:----------")
    print(benchmark(dense_2_graph, '1'))


if __name__ == "__main__":
    main()
