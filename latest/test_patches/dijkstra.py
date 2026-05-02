import heapq


def correct_dijkstra(graph, start, end):
    heap = [(0, start)]
    visited = set()
    while heap:
        cost, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == end:
            return cost
        for v, c in graph[u]:
            if v in visited:
                continue
            heapq.heappush(heap, (cost + c, v))
    return -1


def buggy_dijkstra(graph, start, end):
    heap = [(0, start)]  # cost from start node,end node
    visited = set()
    queued = {start}
    while heap:
        (cost, u) = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == end:
            return cost
        neighbors = {}
        for v, c in graph[u]:
            if v not in neighbors or c < neighbors[v]:
                neighbors[v] = c
        for v, c in neighbors.items():
            if v in visited:
                continue
            if v in queued:
                continue
            next_item = cost + c
            queued.add(v)
            heapq.heappush(heap, (next_item, v))
    return -1


def run_test(label, graph, start, end):
    print(label)
    expected = correct_dijkstra(graph, start, end)
    actual = buggy_dijkstra(graph, start, end)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"graph": graph, "start": start, "end": end})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# TEST_1: provided sample, should pass
graph_1 = {
    "A": [["B", 2], ["C", 5]],
    "B": [["A", 2], ["D", 3], ["E", 1], ["F", 1]],
    "C": [["A", 5], ["F", 3]],
    "D": [["B", 3]],
    "E": [["B", 4], ["F", 3]],
    "F": [["C", 3], ["E", 3]],
}
run_test("TEST_1", graph_1, "E", "C")

# TEST_2: provided sample, should pass
graph_2 = {
    "B": [["C", 1]],
    "C": [["D", 1]],
    "D": [["F", 1]],
    "E": [["B", 1], ["F", 3]],
    "F": [],
}
run_test("TEST_2", graph_2, "E", "F")

# TEST_3: provided sample, should pass
graph_3 = {
    "B": [["C", 1]],
    "C": [["D", 1]],
    "D": [["F", 1]],
    "E": [["B", 1], ["G", 2]],
    "F": [],
    "G": [["F", 1]],
}
run_test("TEST_3", graph_3, "E", "F")

# TEST_4: start equals end, should pass
graph_4 = {
    "S": [["A", 5]],
    "A": [],
}
run_test("TEST_4", graph_4, "S", "S")

# TEST_5: unreachable destination, should pass
graph_5 = {
    "S": [["A", 1]],
    "A": [],
    "T": [],
}
run_test("TEST_5", graph_5, "S", "T")

# TEST_6: duplicate edges but cheapest is first, should pass
graph_6 = {
    "S": [["A", 1], ["A", 10]],
    "A": [],
}
run_test("TEST_6", graph_6, "S", "A")

# TEST_7: minimal failing case with duplicate edges, should fail
graph_7 = {
    "S": [["A", 10], ["A", 1]],
    "A": [],
}
run_test("TEST_7", graph_7, "S", "A")

# TEST_8: classic cheaper path discovered later, should fail
graph_8 = {
    "S": [["A", 10], ["B", 1]],
    "B": [["A", 1]],
    "A": [],
}
run_test("TEST_8", graph_8, "S", "A")

# TEST_9: blocked relaxation causes wrong downstream shortest path, should fail
graph_9 = {
    "S": [["A", 10], ["B", 1]],
    "B": [["A", 1]],
    "A": [["C", 1]],
    "C": [],
}
run_test("TEST_9", graph_9, "S", "C")

# TEST_10: zero-weight cheaper path discovered later, should fail
graph_10 = {
    "S": [["A", 5], ["B", 0]],
    "B": [["A", 0]],
    "A": [],
}
run_test("TEST_10", graph_10, "S", "A")

# TEST_11: longer chain where an early expensive enqueue freezes a node, should fail
graph_11 = {
    "S": [["X", 8], ["Y", 1]],
    "Y": [["Z", 1]],
    "Z": [["X", 1]],
    "X": [["T", 1]],
    "T": [],
}
run_test("TEST_11", graph_11, "S", "T")