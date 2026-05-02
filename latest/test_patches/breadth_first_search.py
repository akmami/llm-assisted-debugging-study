from queue import Queue


class CorrectGraph:
    def __init__(self):
        self.vertices = {}

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex in self.vertices:
            self.vertices[from_vertex].append(to_vertex)
        else:
            self.vertices[from_vertex] = [to_vertex]

    def bfs(self, start_vertex):
        visited = set()
        queue = Queue()
        visited.add(start_vertex)
        queue.put(start_vertex)

        while not queue.empty():
            vertex = queue.get()
            for adjacent_vertex in self.vertices[vertex]:
                if adjacent_vertex not in visited:
                    queue.put(adjacent_vertex)
                    visited.add(adjacent_vertex)
        return visited


class BuggyGraph:
    def __init__(self):
        self.vertices = {}

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex in self.vertices:
            self.vertices[from_vertex].append(to_vertex)
        else:
            self.vertices[from_vertex] = [to_vertex]

    def bfs(self, start_vertex):
        visited = set()
        queue = Queue()
        visited.add(start_vertex)
        queue.put(start_vertex)

        while not queue.empty():
            vertex = queue.get()
            next_vertices = []

            for adjacent_vertex in self.vertices[vertex]:
                if adjacent_vertex not in visited:
                    next_vertices.append(adjacent_vertex)
                    visited.add(adjacent_vertex)

            if not queue.empty():
                continue

            for next_vertex in next_vertices:
                queue.put(next_vertex)

        return visited


def execute(graph_cls, edges, start):
    g = graph_cls()
    for u, v in edges:
        g.add_edge(u, v)
    try:
        return g.bfs(start)
    except Exception as e:
        return f"EXCEPTION: {type(e).__name__}: {e}"


def run_test(label, edges, start):
    print(label)
    expected = execute(CorrectGraph, edges, start)
    actual = execute(BuggyGraph, edges, start)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"edges": edges, "start": start})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")
    print()


# TEST_1: passing simple chain
run_test(
    "TEST_1",
    [(0, 1), (1, 2), (2, 3), (3, 3)],
    0,
)

# TEST_2: passing provided-style cyclic graph
run_test(
    "TEST_2",
    [(0, 1), (0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)],
    2,
)

# TEST_3: passing star where skipped vertices have no new reachability
run_test(
    "TEST_3",
    [(0, 1), (0, 2), (0, 3), (1, 1), (2, 2), (3, 3)],
    0,
)

# TEST_4: passing merge graph where skipped branch reaches already-covered node
run_test(
    "TEST_4",
    [(0, 1), (0, 2), (1, 3), (2, 3), (3, 3)],
    0,
)

# TEST_5: passing self-loop only
run_test(
    "TEST_5",
    [(0, 0)],
    0,
)

# TEST_6: failing minimal deep branch from first queued vertex
run_test(
    "TEST_6",
    [(0, 1), (0, 2), (1, 3), (2, 2), (3, 4), (4, 4)],
    0,
)

# TEST_7: failing branch with multiple newly visited nodes that are never expanded
run_test(
    "TEST_7",
    [(0, 1), (0, 2), (1, 3), (1, 4), (2, 2), (3, 5), (4, 4), (5, 5)],
    0,
)

# TEST_8: failing when one of several initial children has a deeper chain
run_test(
    "TEST_8",
    [(0, 1), (0, 2), (0, 3), (1, 4), (2, 2), (3, 3), (4, 5), (5, 5)],
    0,
)

# TEST_9: failing cyclic branch whose descendant is only reachable through skipped node
run_test(
    "TEST_9",
    [(0, 1), (0, 2), (1, 3), (2, 2), (3, 1), (3, 4), (4, 4)],
    0,
)

# TEST_10: failing middle queued vertex has unique descendants
run_test(
    "TEST_10",
    [(0, 1), (0, 2), (0, 3), (1, 1), (2, 4), (3, 3), (4, 5), (5, 5)],
    0,
)