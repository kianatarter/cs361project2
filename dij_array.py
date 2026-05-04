"""
CS361 Project 2 - Array-Based Dijkstra's Algorithm
Implementations:
  - Adjacency List  (recommended for sparse graphs)
  - Adjacency Matrix (recommended for dense graphs)
Both include path reconstruction via parent[] array (bonus).
"""

import time
import tracemalloc
import math
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Graphs
sparse_1 = {
    'A' : {'B': 4, 'C': 2},
    'B' : {'A': 4, 'D': 5},
    'C' : {'A': 2, 'D': 1},
    'D' : {'B': 5, 'C': 1, 'E': 3},
    'E' : {'D': 3, 'F': 2},
    'F' : {'E': 2}
}

sparse_2 = {
    '1' : {'2': 3, '3': 6},
    '2' : {'1': 3, '4': 2, '5': 5},
    '3' : {'1': 6, '5': 4},
    '4' : {'2': 2, '6': 7},
    '5' : {'3': 4, '7': 1, '2': 5},
    '6' : {'4': 7},
    '7' : {'5': 1}
}

dense_1 = {
    'A' : {'B': 2, 'C': 5, 'D': 1, 'E': 4},
    'B' : {'A': 2, 'C': 3, 'D': 2, 'E': 6},
    'C' : {'A': 5, 'B': 3, 'D': 3, 'E': 1},
    'D' : {'A': 1, 'B': 2, 'C': 3, 'E': 2},
    'E' : {'A': 4, 'B': 6, 'C': 1, 'D': 2}
}

dense_2 = {
    '1' : {'2': 3, '3': 2, '4': 6, '5': 5, '6': 4},
    '2' : {'1': 3, '3': 1, '4': 2, '5': 4, '6': 7},
    '3' : {'1': 2, '2': 1, '4': 3, '5': 6, '6': 5},
    '4' : {'1': 6, '2': 2, '3': 3, '5': 2, '6': 4},
    '5' : {'1': 5, '2': 4, '3': 6, '4': 2, '6': 1},
    '6' : {'1': 4, '2': 7, '3': 5, '4': 4, '5': 1}
}

dense_3 = {
    'A' : {'B': 7, 'C': 3, 'D': 6, 'E': 2},
    'B' : {'A': 7, 'C': 4, 'D': 8, 'E': 5},
    'C' : {'A': 3, 'B': 4, 'D': 1, 'E': 9},
    'D' : {'A': 6, 'B': 8, 'C': 1, 'E': 3},
    'E' : {'A': 2, 'B': 5, 'C': 9, 'D': 3}
}

# Convert dict of dicts to adjacency matrix
def to_matrix(graph):
    # Use keys first, then add any neighbor-only vertices
    seen = dict.fromkeys(graph.keys())
    for neighbors in graph.values():
        for v in neighbors:
            seen.setdefault(v, None)
    vertices = list(seen.keys())
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    matrix = [[0] * n for _ in range(n)]
    for u, neighbors in graph.items():
        for v, w in neighbors.items():
            matrix[idx[u]][idx[v]] = w
    return matrix, vertices

# Path reconstuction from parent
def reconstruct_path(parent, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    if path[0] != source:
        return None
    return path

# Adjacency list
def dijkstra_array_list(graph, source):
    INF = math.inf

    # Collect all vertices
    all_verts = dict.fromkeys(graph.keys())
    for neighbors in graph.values():
        for v in neighbors:
            all_verts.setdefault(v, None)
    all_verts = list(all_verts.keys())

    dist = {v: INF  for v in all_verts}
    parent = {v: None for v in all_verts}  
    visited = {v: False for v in all_verts}

    dist[source] = 0

    for _ in range(len(all_verts)):
        # find unvisited vertex with smallest distance
        u = None
        for v in all_verts:
            if not visited[v]:
                if u is None or dist[v] < dist[u]:
                    u = v

        if u is None or dist[u] == INF:
            break  # All remaining vertices are unreachable

        visited[u] = True

        # Relax neighbors
        for neighbor, weight in graph.get(u, {}).items():
            if not visited[neighbor]:
                new_dist = dist[u] + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    parent[neighbor] = u 
    return dist, parent

# Adjacency Matrix
def dijkstra_array_matrix(graph, source):
    INF = math.inf
    matrix, vertices = to_matrix(graph)
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)} 

    dist = [INF] * n
    parent = [None] * n   
    visited = [False] * n

    dist[idx[source]] = 0

    for _ in range(n):
        # find unvisited vertex with smallest distance
        u = -1
        for i in range(n):
            if not visited[i]:
                if u == -1 or dist[i] < dist[u]:
                    u = i

        if u == -1 or dist[u] == INF:
            break

        visited[u] = True

        # Relax neighbors
        for v in range(n):
            if matrix[u][v] != 0 and not visited[v]:
                new_dist = dist[u] + matrix[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u 
    # Convert index-based results back to vertex labels
    dist_labeled = {vertices[i]: dist[i] for i in range(n)}
    parent_labeled = {vertices[i]: (vertices[parent[i]] if parent[i] is not None else None)
                      for i in range(n)}
    return dist_labeled, parent_labeled


# Benchmarking
def benchmark(fn, graph, source, trials=5):
    times = []
    peak_mem = 0
    result = None

    for _ in range(trials):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = fn(graph, source)
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append((t1 - t0) * 1000)
        peak_mem = max(peak_mem, peak)

    avg_ms  = sum(times) / len(times)
    peak_mb = peak_mem / (1024 * 1024)
    return avg_ms, peak_mb, result

# Printing
def print_results(label, source, dist, parent):
    print(f"\n{'-'*55}")
    print(f"  {label}     Source: {source}")
    print(f"{'-'*55}")
    print(f"  {'Vertex':<10} {'Distance':<12} {'Path'}")
    print(f"  {'-'*50}")
    for v in dist:
        d = dist[v]
        d_str = str(d) if d != math.inf else "infinity"
        path = reconstruct_path(parent, source, v)
        p_str = " → ".join(str(x) for x in path) if path else "unreachable"
        print(f"  {str(v):<10} {d_str:<12} {p_str}")

def print_benchmark_row(graph_name, method, avg_ms, peak_mb):
    print(f"  {graph_name:<12} {method:<30} {avg_ms:>10.4f} ms   {peak_mb:>8.4f} MB")

# Random graph generators for scaling plots
def generate_sparse_dict(V, seed=42):
    random.seed(seed)
    graph = {i: {} for i in range(V)}
    for i in range(V - 1): 
        w = random.randint(1, 20)
        graph[i][i + 1] = w
        graph[i + 1][i] = w
    for _ in range(V):     
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        if u != v:
            w = random.randint(1, 20)
            graph[u][v] = w
            graph[v][u] = w
    return graph

def generate_dense_dict(V, seed=42):
    random.seed(seed)
    graph = {i: {} for i in range(V)}
    for i in range(V):
        for j in range(i + 1, V):
            w = random.randint(1, 20)
            graph[i][j] = w
            graph[j][i] = w
    return graph


# MATPLOTLIB
COLORS = {
    'sparse' : "#FF07C1",
    'dense'  : "#994BF3",
}

def plot_example_graphs(results):
    labels = [r[0] for r in results]
    times = [r[2] for r in results]
    memories = [r[3] for r in results]
    colors = [COLORS['sparse'] if 'List' in r[1] else COLORS['dense'] for r in results]
    x = range(len(labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Array-Based Dijkstra — Example Graphs Benchmark",
                 fontsize=14, fontweight='bold', y=1.01)

    # Runtime
    bars = ax1.bar(x, times, color=colors, edgecolor='white', linewidth=0.8, width=0.55)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=18, ha='right', fontsize=9)
    ax1.set_ylabel("Avg Runtime (ms)", fontsize=10)
    ax1.set_title("Runtime Comparison", fontsize=11, fontweight='bold')
    ax1.bar_label(bars, fmt='%.4f', padding=3, fontsize=8)
    ax1.set_ylim(0, max(times) * 1.4)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    ax1.spines[['top', 'right']].set_visible(False)

    # Memory
    bars2 = ax2.bar(x, memories, color=colors, edgecolor='white', linewidth=0.8, width=0.55)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=18, ha='right', fontsize=9)
    ax2.set_ylabel("Peak Memory (MB)", fontsize=10)
    ax2.set_title("Memory Usage Comparison", fontsize=11, fontweight='bold')
    ax2.bar_label(bars2, fmt='%.4f', padding=3, fontsize=8)
    ax2.set_ylim(0, max(memories) * 1.4 if max(memories) > 0 else 0.01)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    ax2.spines[['top', 'right']].set_visible(False)

    patch_sparse = mpatches.Patch(color=COLORS['sparse'], label='Adj List  (Sparse)')
    patch_dense = mpatches.Patch(color=COLORS['dense'],  label='Adj Matrix (Dense)')
    fig.legend(handles=[patch_sparse, patch_dense], loc='upper right',
               fontsize=9, framealpha=0.85)

    plt.tight_layout()
    plt.show()


def plot_scaling(sizes):
    sparse_times = []
    dense_times = []

    print("\n  Running scaling benchmarks...")
    for V in sizes:
        print(f"    V = {V} ...", end=' ', flush=True)

        g = generate_sparse_dict(V)
        avg, _, _ = benchmark(dijkstra_array_list, g, 0, trials=3)
        sparse_times.append(avg)

        d = generate_dense_dict(V)
        avg, _, _ = benchmark(dijkstra_array_matrix, d, 0, trials=3)
        dense_times.append(avg)

        print(f"list={sparse_times[-1]:.3f}ms  matrix={dense_times[-1]:.3f}ms")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, sparse_times, 'o-', color=COLORS['sparse'],
            linewidth=2, markersize=6, label='Array + Adj List  (Sparse, O(V²))')
    ax.plot(sizes, dense_times,  's-', color=COLORS['dense'],
            linewidth=2, markersize=6, label='Array + Adj Matrix (Dense,  O(V²))')

    ax.set_xlabel("Number of Vertices (V)", fontsize=11)
    ax.set_ylabel("Avg Runtime (ms)", fontsize=11)
    ax.set_title("Array-Based Dijkstra — Runtime Scaling (O(V²))",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(linestyle='--', alpha=0.4)
    ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.show()

# Main
def main():
    # Sparse graphs -> adjacency list version
    dist, parent = dijkstra_array_list(sparse_1, 'A')
    print_results("Sparse Graph 1 — Adjacency List", 'A', dist, parent)

    dist, parent = dijkstra_array_list(sparse_2, '1')
    print_results("Sparse Graph 2 — Adjacency List", '1', dist, parent)

    # Dense graphs -> adjacency matrix version
    dist, parent = dijkstra_array_matrix(dense_1, 'A')
    print_results("Dense Graph 1 — Adjacency Matrix", 'A', dist, parent)

    dist, parent = dijkstra_array_matrix(dense_2, '1')
    print_results("Dense Graph 2 — Adjacency Matrix", '1', dist, parent)

    dist, parent = dijkstra_array_matrix(dense_3, 'A')
    print_results("Dense Graph 3 — Adjacency Matrix", 'A', dist, parent)

    # Benchmarks
    print("\n\n" + "-"*60)
    print("  BENCHMARKS")
    print("-"*60)
    print(f"  {'Graph':<12} {'Method':<30} {'Time':>13}   {'Memory':>10}")
    print(f"  {'-'*67}")

    avg1s, mem1s, _ = benchmark(dijkstra_array_list, sparse_1, 'A')
    avg2s, mem2s, _ = benchmark(dijkstra_array_list, sparse_2, '1')
    avg1d, mem1d, _ = benchmark(dijkstra_array_matrix, dense_1, 'A')
    avg2d, mem2d, _ = benchmark(dijkstra_array_matrix, dense_2, '1')
    avg3d, mem3d, _ = benchmark(dijkstra_array_matrix, dense_3, 'A')

    print_benchmark_row("Sparse-1", "Array (Adjacency List)", avg1s, mem1s)
    print_benchmark_row("Sparse-2", "Array (Adjacency List)", avg2s, mem2s)
    print_benchmark_row("Dense-1", "Array (Adjacency Matrix)", avg1d, mem1d)
    print_benchmark_row("Dense-2", "Array (Adjacency Matrix)", avg2d, mem2d)
    print_benchmark_row("Dense-3", "Array (Adjacency Matrix)", avg3d, mem3d)
    print()

    # Charts
    print("\n  Generating charts...")

    example_results = [
        ("Sparse-1\n(Adj List)", "List", avg1s, mem1s),
        ("Sparse-2\n(Adj List)", "List", avg2s, mem2s),
        ("Dense-1\n(Adj Matrix)", "Matrix", avg1d, mem1d),
        ("Dense-2\n(Adj Matrix)", "Matrix", avg2d, mem2d),
        ("Dense-3\n(Adj Matrix)", "Matrix", avg3d, mem3d),
    ]
    plot_example_graphs(example_results)
    plot_scaling(sizes=[100, 250, 500, 750, 1000])

if __name__ == "__main__":
    main()