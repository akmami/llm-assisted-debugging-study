import math


class CorrectGraph:
    def __init__(self, n=0):
        self.n = n
        self.w = [[math.inf for _ in range(n)] for _ in range(n)]
        self.dp = [[math.inf for _ in range(n)] for _ in range(n)]

    def add_edge(self, u, v, w):
        self.dp[u][v] = w

    def floyd_warshall(self):
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.dp[i][j] = min(self.dp[i][j], self.dp[i][k] + self.dp[k][j])

    def show_min(self, u, v):
        return self.dp[u][v]


class BuggyGraph:
    def __init__(self, n=0):
        self.n = n
        self.w = [[math.inf for _ in range(n)] for _ in range(n)]
        self.dp = [[math.inf for _ in range(n)] for _ in range(n)]

    def add_edge(self, u, v, w):
        self.dp[u][v] = w

    def floyd_warshall(self):
        for i in range(self.n):
            for k in range(self.n):
                if self.dp[i][k] == math.inf:
                    continue
                for j in range(self.n):
                    if self.dp[k][j] == math.inf:
                        continue
                    candidate = self.dp[i][k] + self.dp[k][j]
                    if candidate < self.dp[i][j]:
                        self.dp[i][j] = candidate

    def show_min(self, u, v):
        return self.dp[u][v]


def run_test(label, n, edges, query):
    correct = CorrectGraph(n)
    buggy = BuggyGraph(n)

    for u, v, w in edges:
        correct.add_edge(u, v, w)
        buggy.add_edge(u, v, w)

    correct.floyd_warshall()
    buggy.floyd_warshall()

    expected = correct.show_min(query[0], query[1])
    actual = buggy.show_min(query[0], query[1])

    print(label)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"n": n, "edges": edges, "query": query})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# Passing tests
run_test(
    "TEST_1",
    2,
    [(0, 1, 5)],
    (0, 1),
)

run_test(
    "TEST_2",
    3,
    [(0, 1, 1), (1, 2, 2)],
    (0, 2),
)

run_test(
    "TEST_3",
    3,
    [(0, 1, 7)],
    (2, 1),
)

run_test(
    "TEST_4",
    3,
    [(0, 1, 2), (1, 2, 5), (0, 2, 4)],
    (0, 2),
)

run_test(
    "TEST_5",
    4,
    [(0, 1, 2), (1, 2, 2), (2, 3, 2)],
    (0, 3),
)

run_test(
    "TEST_6",
    1,
    [],
    (0, 0),
)

# Failing tests
run_test(
    "TEST_7",
    4,
    [(0, 2, 1), (2, 1, 1), (1, 3, 1)],
    (0, 3),
)

run_test(
    "TEST_8",
    4,
    [(0, 2, 2), (2, 1, 2), (1, 3, 2), (0, 3, 10)],
    (0, 3),
)

run_test(
    "TEST_9",
    4,
    [(3, 2, 1), (2, 0, 1), (0, 1, 1)],
    (3, 1),
)

run_test(
    "TEST_10",
    5,
    [(0, 4, 1), (4, 2, 1), (2, 1, 1), (1, 3, 1)],
    (0, 3),
)