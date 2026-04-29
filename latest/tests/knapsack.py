correct_f = None
buggy_f = None


def correct_mf_knapsack(i, wt, val, j):
    global correct_f
    if correct_f[i][j] < 0:
        if j < wt[i - 1]:
            val = correct_mf_knapsack(i - 1, wt, val, j)
        else:
            val = max(
                correct_mf_knapsack(i - 1, wt, val, j),
                correct_mf_knapsack(i - 1, wt, val, j - wt[i - 1]) + val[i - 1],
            )
        correct_f[i][j] = val
    return correct_f[i][j]


def correct_knapsack(w, wt, val, n):
    dp = [[0] * (w + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w_ in range(1, w + 1):
            if wt[i - 1] <= w_:
                dp[i][w_] = max(val[i - 1] + dp[i - 1][w_ - wt[i - 1]], dp[i - 1][w_])
            else:
                dp[i][w_] = dp[i - 1][w_]

    return dp[n][w_], dp


def correct_knapsack_with_example_solution(w: int, wt: list, val: list):
    if not (isinstance(wt, (list, tuple)) and isinstance(val, (list, tuple))):
        raise ValueError(
            "Both the weights and values vectors must be either lists or tuples"
        )

    num_items = len(wt)
    if num_items != len(val):
        msg = (
            "The number of weights must be the same as the number of values.\n"
            f"But got {num_items} weights and {len(val)} values"
        )
        raise ValueError(msg)
    for i in range(num_items):
        if not isinstance(wt[i], int):
            msg = (
                "All weights must be integers but got weight of "
                f"type {type(wt[i])} at index {i}"
            )
            raise TypeError(msg)

    optimal_val, dp_table = correct_knapsack(w, wt, val, num_items)
    example_optional_set = set()
    correct_construct_solution(dp_table, wt, num_items, w, example_optional_set)

    return optimal_val, example_optional_set


def correct_construct_solution(dp: list, wt: list, i: int, j: int, optimal_set: set):
    if i > 0 and j > 0:
        if dp[i - 1][j] == dp[i][j]:
            correct_construct_solution(dp, wt, i - 1, j, optimal_set)
        else:
            optimal_set.add(i)
            correct_construct_solution(dp, wt, i - 1, j - wt[i - 1], optimal_set)


def buggy_mf_knapsack(i, wt, val, j):
    global buggy_f
    if buggy_f[i][j] < 0:
        if j < wt[i - 1]:
            val = buggy_mf_knapsack(i - 1, wt, val, j)
        else:
            val = max(
                buggy_mf_knapsack(i - 1, wt, val, j),
                buggy_mf_knapsack(i, wt, val, j - wt[i - 1]) + val[i - 1],
            )
        buggy_f[i][j] = val
    return buggy_f[i][j]


def buggy_knapsack(w, wt, val, n):
    dp = [[0] * (w + 1) for _ in range(n + 1)]
    running = [0] * (w + 1)

    for i in range(1, n + 1):
        dp[i] = running[:]
        for w_ in range(1, w + 1):
            if wt[i - 1] <= w_:
                include_value = val[i - 1] + running[w_ - wt[i - 1]]
                exclude_value = running[w_]
                running[w_] = max(include_value, exclude_value)
            dp[i][w_] = running[w_]

    return dp[n][w], dp


def buggy_knapsack_with_example_solution(w: int, wt: list, val: list):
    if not (isinstance(wt, (list, tuple)) and isinstance(val, (list, tuple))):
        raise ValueError(
            "Both the weights and values vectors must be either lists or tuples"
        )

    num_items = len(wt)
    if num_items != len(val):
        msg = (
            "The number of weights must be the same as the number of values. "
            f"But got {num_items} weights and {len(val)} values"
        )
        raise ValueError(msg)
    for i in range(num_items):
        if not isinstance(wt[i], int):
            msg = (
                "All weights must be integers but got weight of "
                f"type {type(wt[i])} at index {i}"
            )
            raise TypeError(msg)

    optimal_val, dp_table = buggy_knapsack(w, wt, val, num_items)
    example_optional_set = set()
    buggy_construct_solution(dp_table, wt, num_items, w, example_optional_set)

    return optimal_val, example_optional_set


def buggy_construct_solution(dp: list, wt: list, i: int, j: int, optimal_set: set):
    if i > 0 and j > 0:
        if dp[i - 1][j] == dp[i][j]:
            buggy_construct_solution(dp, wt, i - 1, j, optimal_set)
        else:
            optimal_set.add(i)
            buggy_construct_solution(dp, wt, i - 1, j - wt[i - 1], optimal_set)


def safe_call(fn):
    try:
        return ("OK", fn())
    except Exception as e:
        return ("EXC", type(e).__name__, str(e))


def run_test(label, input_data, correct_fn, buggy_fn):
    print(label)
    expected = safe_call(correct_fn)
    actual = safe_call(buggy_fn)
    if actual != expected:
        print("TEST FAILED")
        print("input:", input_data)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


def correct_knapsack_value(w, wt, val):
    return correct_knapsack(w, wt, val, len(wt))[0]


def buggy_knapsack_value(w, wt, val):
    return buggy_knapsack(w, wt, val, len(wt))[0]


def correct_mf_value(i, wt, val, j):
    global correct_f
    correct_f = [[0] * (j + 1)] + [[0] + [-1] * (j + 1) for _ in range(i + 1)]
    return correct_mf_knapsack(i, wt, val, j)


def buggy_mf_value(i, wt, val, j):
    global buggy_f
    buggy_f = [[0] * (j + 1)] + [[0] + [-1] * (j + 1) for _ in range(i + 1)]
    return buggy_mf_knapsack(i, wt, val, j)


# TEST_1
w = 2
wt = [3]
val = [5]
run_test(
    "TEST_1",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_value(w, wt, val),
    lambda: buggy_knapsack_value(w, wt, val),
)

# TEST_2
w = 3
wt = [3]
val = [5]
run_test(
    "TEST_2",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_value(w, wt, val),
    lambda: buggy_knapsack_value(w, wt, val),
)

# TEST_3
w = 5
wt = [5, 4]
val = [10, 7]
run_test(
    "TEST_3",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_value(w, wt, val),
    lambda: buggy_knapsack_value(w, wt, val),
)

# TEST_4
w = 3
wt = "bad"
val = [1]
run_test(
    "TEST_4",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_with_example_solution(w, wt, val),
    lambda: buggy_knapsack_with_example_solution(w, wt, val),
)

# TEST_5
w = 3
wt = [4, 3, 2]
val = [10, 5, 3]
run_test(
    "TEST_5",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_with_example_solution(w, wt, val),
    lambda: buggy_knapsack_with_example_solution(w, wt, val),
)

# TEST_6
w = 3
wt = [4, 3, 2]
val = [10, 5, 3]
run_test(
    "TEST_6",
    {"i": len(wt), "wt": wt, "val": val, "j": w},
    lambda: correct_mf_value(len(wt), wt, val, w),
    lambda: buggy_mf_value(len(wt), wt, val, w),
)

# TEST_7
w = 2
wt = [1]
val = [2]
run_test(
    "TEST_7",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_value(w, wt, val),
    lambda: buggy_knapsack_value(w, wt, val),
)

# TEST_8
w = 4
wt = [2, 3]
val = [3, 4]
run_test(
    "TEST_8",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_value(w, wt, val),
    lambda: buggy_knapsack_value(w, wt, val),
)

# TEST_9
w = 10
wt = [1, 3, 5, 2]
val = [10, 20, 100, 22]
run_test(
    "TEST_9",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_value(w, wt, val),
    lambda: buggy_knapsack_value(w, wt, val),
)

# TEST_10
w = 2
wt = [1]
val = [2]
run_test(
    "TEST_10",
    {"w": w, "wt": wt, "val": val},
    lambda: correct_knapsack_with_example_solution(w, wt, val),
    lambda: buggy_knapsack_with_example_solution(w, wt, val),
)

# TEST_11
w = 2
wt = [1]
val = [2]
run_test(
    "TEST_11",
    {"i": len(wt), "wt": wt, "val": val, "j": w},
    lambda: correct_mf_value(len(wt), wt, val, w),
    lambda: buggy_mf_value(len(wt), wt, val, w),
)