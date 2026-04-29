from __future__ import annotations

def correct_check_negative_cycle(
    graph: list[dict[str, int]], distance: list[float], edge_count: int
):
    for j in range(edge_count):
        u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])
        if distance[u] != float("inf") and distance[u] + w < distance[v]:
            return True
    return False


def correct_bellman_ford(
    graph: list[dict[str, int]], vertex_count: int, edge_count: int, src: int
) -> list[float]:
    distance = [float("inf")] * vertex_count
    distance[src] = 0.0

    for _ in range(vertex_count - 1):
        for j in range(edge_count):
            u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])
            if distance[u] != float("inf") and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    negative_cycle_exists = correct_check_negative_cycle(graph, distance, edge_count)
    if negative_cycle_exists:
        raise Exception("Negative cycle found")

    return distance


def buggy_check_negative_cycle(
    graph: list[dict[str, int]], distance: list[float], edge_count: int
):
    for j in range(edge_count):
        u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])
        if distance[u] != float("inf") and distance[u] + w < distance[v]:
            return True
    return False


def buggy_bellman_ford(
    graph: list[dict[str, int]], vertex_count: int, edge_count: int, src: int
) -> list[float]:
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

    negative_cycle_exists = buggy_check_negative_cycle(graph, distance, edge_count)
    if negative_cycle_exists:
        raise Exception("Negative cycle found")

    return distance


def run_impl(func, edges, vertex_count, src):
    graph = [{"src": s, "dst": d, "weight": w} for s, d, w in edges]
    try:
        return ("OK", func(graph, vertex_count, len(graph), src))
    except Exception as e:
        return ("EXC", str(e))


def run_test(label, edges, vertex_count, src):
    expected = run_impl(correct_bellman_ford, edges, vertex_count, src)
    actual = run_impl(buggy_bellman_ford, edges, vertex_count, src)

    if actual != expected:
        print(f"{label} TEST FAILED")
        print("input:", {"edges": edges, "vertex_count": vertex_count, "src": src})
        print("expected:", expected)
        print("got:", actual)
    else:
        print(f"{label} TEST PASSED")


# TEST_1: simple positive graph
run_test(
    "TEST_1",
    [(0, 1, 4), (0, 2, 5), (1, 2, 1), (2, 3, 3)],
    4,
    0,
)

# TEST_2: simple chain with one negative edge, no delayed propagation issue
run_test(
    "TEST_2",
    [(0, 1, 4), (1, 2, -2), (2, 3, 1)],
    4,
    0,
)

# TEST_3: unreachable vertex
run_test(
    "TEST_3",
    [(0, 1, 2)],
    3,
    0,
)

# TEST_4: single vertex, no edges
run_test(
    "TEST_4",
    [],
    1,
    0,
)

# TEST_5: actual negative cycle reachable from source
run_test(
    "TEST_5",
    [(2, 1, -10), (3, 2, 3), (0, 3, 5), (0, 1, 4), (1, 3, 5)],
    4,
    0,
)

# TEST_6: negative edge improvement while vertex is still effectively recoverable
run_test(
    "TEST_6",
    [(0, 1, 10), (0, 2, 5), (1, 3, 2), (2, 1, -10)],
    4,
    0,
)

# TEST_7: FAIL - delayed improvement to settled vertex; buggy falsely reports negative cycle
run_test(
    "TEST_7",
    [(0, 1, 10), (0, 3, 5), (1, 4, 2), (3, 2, 1), (2, 1, -10)],
    5,
    0,
)

# TEST_8: FAIL - same pattern with zero weights / boundary-like values
run_test(
    "TEST_8",
    [(0, 1, 0), (0, 3, 0), (1, 4, 0), (3, 2, 0), (2, 1, -1)],
    5,
    0,
)

# TEST_9: FAIL - different source and longer downstream propagation needed
run_test(
    "TEST_9",
    [(5, 1, 7), (5, 4, 2), (1, 0, 1), (4, 3, 1), (3, 1, -10), (0, 2, 3)],
    6,
    5,
)

# TEST_10: pass with duplicate edges but no problematic reactivation
run_test(
    "TEST_10",
    [(0, 1, 5), (0, 1, 2), (1, 2, 3), (0, 2, 10)],
    3,
    0,
)