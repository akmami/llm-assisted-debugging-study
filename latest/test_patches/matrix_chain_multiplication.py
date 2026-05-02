from functools import cache
from sys import maxsize


def correct_matrix_chain_multiply(arr: list[int]) -> int:
    if len(arr) < 2:
        return 0
    n = len(arr)
    dp = [[maxsize for _ in range(n)] for _ in range(n)]
    for i in range(n - 1, 0, -1):
        for j in range(i, n):
            if i == j:
                dp[i][j] = 0
                continue
            for k in range(i, j):
                dp[i][j] = min(
                    dp[i][j], dp[i][k] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j]
                )
    return dp[1][n - 1]


def buggy_matrix_chain_multiply(arr: list[int]) -> int:
    if len(arr) < 2:
        return 0
    n = len(arr)
    dp = [[maxsize for _ in range(n)] for _ in range(n)]
    for i in range(1, n):
        dp[i][i] = 0
    for i in range(1, n):
        for j in range(i + 1, n):
            for k in range(i, j):
                dp[i][j] = min(
                    dp[i][j], dp[i][k] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j]
                )
    return dp[1][n - 1]


def correct_matrix_chain_order(dims: list[int]) -> int:
    @cache
    def a(i: int, j: int) -> int:
        return min(
            (a(i, k) + dims[i] * dims[k] * dims[j] + a(k, j) for k in range(i + 1, j)),
            default=0,
        )

    return a(0, len(dims) - 1)


def buggy_matrix_chain_order(dims: list[int]) -> int:
    def split_points(i: int, j: int) -> range:
        if j - i <= 2:
            return range(i + 1, j)
        return range(j - 1, j)

    @cache
    def a(i: int, j: int) -> int:
        return min(
            (
                a(i, k) + dims[i] * dims[k] * dims[j] + a(k, j)
                for k in split_points(i, j)
            ),
            default=0,
        )

    return a(0, len(dims) - 1)


def run_test(label: str, arr: list[int]) -> None:
    print(label)

    expected = correct_matrix_chain_multiply(arr)
    actual = buggy_matrix_chain_multiply(arr)
    if actual != expected:
        print("TEST FAILED")
        print("input:", arr)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")

    expected = correct_matrix_chain_order(arr)
    actual = buggy_matrix_chain_order(arr)
    if actual != expected:
        print("TEST FAILED")
        print("input:", arr)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


run_test("TEST_1", [])
run_test("TEST_2", [10])
run_test("TEST_3", [10, 20])
run_test("TEST_4", [19, 2, 19])
run_test("TEST_5", [1, 1, 1, 1])
run_test("TEST_6", [1, 2, 3, 4])
run_test("TEST_7", [1, 2, 3, 4, 5])
run_test("TEST_8", [10, 30, 5, 60])
run_test("TEST_9", [3, 1, 3, 1])
run_test("TEST_10", [30, 1, 40, 10])
run_test("TEST_11", [3, 1, 3, 1, 3])
run_test("TEST_12", [40, 20, 30, 10, 30])
run_test("TEST_13", [5, 10, 3, 12, 5, 50, 6])