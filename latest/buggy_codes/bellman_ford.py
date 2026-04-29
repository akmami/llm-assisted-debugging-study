# The buggy version will pass many simple graphs, especially graphs with non-negative weights or graphs where each vertex's shortest distance is finalized before its outgoing edges matter. It can also pass some negative-edge cases where improvements do not need to be propagated after a vertex has already been processed. It fails on graphs where a negative edge improves the distance to a previously active vertex and that improved distance must be propagated through outgoing edges. In such cases it may return distances that are too large, or the final validation may falsely raise `Exception: Negative cycle found` because some ordinary edge is still relaxable due to the incomplete propagation.
from __future__ import annotations


def print_distance(distance: list[float], src):
    print(f"Vertex\tShortest Distance from vertex {src}")
    for i, d in enumerate(distance):
        print(f"{i}\t\t{d}")


def check_negative_cycle(
    graph: list[dict[str, int]], distance: list[float], edge_count: int
):
    for j in range(edge_count):
        u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])
        if distance[u] != float("inf") and distance[u] + w < distance[v]:
            return True
    return False


def bellman_ford(
    graph: list[dict[str, int]], vertex_count: int, edge_count: int, src: int
) -> list[float]:
    """
    Returns shortest paths from a vertex src to all
    other vertices.
    >>> edges = [(2, 1, -10), (3, 2, 3), (0, 3, 5), (0, 1, 4)]
    >>> g = [{"src": s, "dst": d, "weight": w} for s, d, w in edges]
    >>> bellman_ford(g, 4, 4, 0)
    [0.0, -2.0, 8.0, 5.0]
    >>> g = [{"src": s, "dst": d, "weight": w} for s, d, w in edges + [(1, 3, 5)]]
    >>> bellman_ford(g, 4, 5, 0)
    Traceback (most recent call last):
     ...
    Exception: Negative cycle found
    """
    distance = [float("inf")] * vertex_count
    distance[src] = 0.0

    active_vertices: set[int] = {src}
    settled_vertices: set[int] = set()

    for _ in range(vertex_count - 1):
        if not active_vertices:
            break

        next_active_vertices: set[int] = set()

        for j in range(edge_count):
            u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])

            if (
                u in active_vertices
                and distance[u] != float("inf")
                and distance[u] + w < distance[v]
            ):
                distance[v] = distance[u] + w
                if v not in settled_vertices:
                    next_active_vertices.add(v)

        settled_vertices.update(active_vertices)
        active_vertices = next_active_vertices

    negative_cycle_exists = check_negative_cycle(graph, distance, edge_count)
    if negative_cycle_exists:
        raise Exception("Negative cycle found")

    return distance


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    V = int(input("Enter number of vertices: ").strip())
    E = int(input("Enter number of edges: ").strip())

    graph: list[dict[str, int]] = [{} for _ in range(E)]

    for i in range(E):
        print("Edge ", i + 1)
        src, dest, weight = (
            int(x)
            for x in input("Enter source, destination, weight: ").strip().split(" ")
        )
        graph[i] = {"src": src, "dst": dest, "weight": weight}

    source = int(input("\nEnter shortest path source:").strip())
    shortest_distance = bellman_ford(graph, V, E, source)
    print_distance(shortest_distance, 0)
