def correct_topological_sort(graph: dict[int, list[int]]) -> list[int] | None:
    indegree = [0] * len(graph)
    queue = []
    topo_order = []
    processed_vertices_count = 0

    for values in graph.values():
        for i in values:
            indegree[i] += 1

    for i in range(len(indegree)):
        if indegree[i] == 0:
            queue.append(i)

    while queue:
        vertex = queue.pop(0)
        processed_vertices_count += 1
        topo_order.append(vertex)

        for neighbor in graph[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if processed_vertices_count != len(graph):
        return None
    return topo_order


def buggy_topological_sort(graph: dict[int, list[int]]) -> list[int] | None:
    indegree = [0] * len(graph)
    queue = []
    topo_order = []
    processed_vertices_count = 0

    for values in graph.values():
        for i in values:
            indegree[i] += 1

    for i in range(len(indegree)):
        if indegree[i] == 0:
            queue.append(i)

    seen = set(queue)

    while queue:
        vertex = queue.pop(0)
        processed_vertices_count += 1
        topo_order.append(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in seen:
                indegree[neighbor] -= 1
                seen.add(neighbor)
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

    if processed_vertices_count != len(graph):
        return None
    return topo_order


def run_test(label, graph):
    expected = correct_topological_sort(graph)
    actual = buggy_topological_sort(graph)
    print(label)
    if actual != expected:
        print("TEST FAILED")
        print("input:", graph)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# TEST_1: empty graph (pass)
graph = {}
run_test("TEST_1", graph)

# TEST_2: single vertex (pass)
graph = {0: []}
run_test("TEST_2", graph)

# TEST_3: simple chain (pass)
graph = {0: [1], 1: [2], 2: [3], 3: []}
run_test("TEST_3", graph)

# TEST_4: branching tree, no joins (pass)
graph = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
run_test("TEST_4", graph)

# TEST_5: disconnected acyclic graph with isolated vertex (pass)
graph = {0: [1], 1: [], 2: [3], 3: [], 4: []}
run_test("TEST_5", graph)

# TEST_6: simple cycle (pass)
graph = {0: [1], 1: [2], 2: [0]}
run_test("TEST_6", graph)

# TEST_7: minimal join DAG (fail)
graph = {0: [2], 1: [2], 2: []}
run_test("TEST_7", graph)

# TEST_8: diamond-shaped DAG (fail)
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
run_test("TEST_8", graph)

# TEST_9: join after a longer chain (fail)
graph = {0: [1], 1: [3], 2: [3], 3: [4], 4: []}
run_test("TEST_9", graph)

# TEST_10: multiple predecessors joining into one sink (fail)
graph = {0: [3], 1: [3], 2: [3], 3: []}
run_test("TEST_10", graph)

# TEST_11: disconnected graph where one component has a join (fail)
graph = {0: [1], 1: [], 2: [4], 3: [4], 4: []}
run_test("TEST_11", graph)

# TEST_12: layered DAG with several joins (fail)
graph = {0: [2, 3], 1: [3], 2: [4], 3: [4], 4: [5], 5: []}
run_test("TEST_12", graph)