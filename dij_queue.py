''' CS 361: Project 2
Dijkstra's Algorithm implementation using a priority queue

Kiana Tarter and Neveah Martinez

'''

import heapq
import sys

def priority_queue_dij(adj, src): 
    V = len(adj)

    queue = []

    # set all elements of solution to infinity initially
    dist = [sys.maxsize] * V
    
    # set the path from the source to itself to 0
    dist[src] = 0

    heapq.heappush(queue, (0,src))

    while queue: 
        d, u = heapq.heappop(queue)

        if (d > dist[u]):
            continue

        for vertex, cost in adj[u]:

            if dist[u] + cost < dist[vertex]:
                dist[vertex] = dist[u] + cost
                heapq.heappush(queue, (dist[vertex], cost))
    return dist
