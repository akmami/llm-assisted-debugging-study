from __future__ import annotations

def correct_depth_first_search(graph: dict, start: str) -> set[str]:
    explored, stack = set(start), [start]

    while stack:
        v = stack.pop()
        explored.add(v)
        for adj in reversed(graph[v]):
            if adj not in explored:
                stack.append(adj)
    return explored


def buggy_depth_first_search(graph: dict, start: str) -> set[str]:
    explored, stack = set(), [start]
    next_child = {start: 0}

    while stack:
        v = stack.pop()
        if v in explored:
            continue

        explored.add(v)
        neighbors = list(reversed(graph[v]))
        child_index = next_child.get(v, 0)

        while child_index < len(neighbors):
            adj = neighbors[child_index]
            child_index += 1
            next_child[v] = child_index

            if adj not in explored:
                next_child.setdefault(adj, 0)
                stack.append(adj)
                if graph.get(adj):
                    break

    return explored


def run_test(label, graph, start):
    print(label)
    expected = correct_depth_first_search(graph, start)
    actual = buggy_depth_first_search(graph, start)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"graph": graph, "start": start})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# TEST_1: isolated vertex -> should pass
graph_1 = {"A": []}
run_test("TEST_1", graph_1, "A")

# TEST_2: simple path -> should pass
graph_2 = {"A": ["B"], "B": ["C"], "C": []}
run_test("TEST_2", graph_2, "A")

# TEST_3: simple cycle -> should pass
graph_3 = {"A": ["B"], "B": ["C"], "C": ["A"]}
run_test("TEST_3", graph_3, "A")

# TEST_4: branching, but chosen first DFS branch reaches the other node -> should pass
graph_4 = {"A": ["B", "C"], "B": [], "C": ["B"]}
run_test("TEST_4", graph_4, "A")

# TEST_5: duplicate neighbors -> should pass
graph_5 = {"A": ["B", "B"], "B": []}
run_test("TEST_5", graph_5, "A")

# TEST_6: minimal branching star -> should fail
graph_6 = {"A": ["B", "C"], "B": [], "C": []}
run_test("TEST_6", graph_6, "A")

# TEST_7: branching with missed sibling subtree -> should fail
graph_7 = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
run_test("TEST_7", graph_7, "A")

# TEST_8: three-way branch -> should fail
graph_8 = {"A": ["B", "C", "D"], "B": [], "C": [], "D": []}
run_test("TEST_8", graph_8, "A")

# TEST_9: original sample graph from reference -> should fail
graph_9 = {
    "A": ["B", "C", "D"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "D"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}
run_test("TEST_9", graph_9, "A")

# TEST_10: later sibling has unique reachable nodes -> should fail
graph_10 = {"A": ["B", "C"], "B": ["E"], "C": ["D"], "D": [], "E": []}
run_test("TEST_10", graph_10, "A")