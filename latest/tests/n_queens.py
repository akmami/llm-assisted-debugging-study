def correct_is_safe(board, row, column):
    n = len(board)
    return (
        all(board[i][j] != 1 for i, j in zip(range(row), [column] * row))
        and all(
            board[i][j] != 1
            for i, j in zip(range(row - 1, -1, -1), range(column - 1, -1, -1))
        )
        and all(
            board[i][j] != 1
            for i, j in zip(range(row - 1, -1, -1), range(column + 1, n))
        )
    )


def buggy_is_safe(board, row, column):
    n = len(board)
    occupied_columns = set()
    occupied_diagonals = set()

    for r in range(row):
        for c in range(n):
            if board[r][c] == 1:
                occupied_columns.add(c)
                occupied_diagonals.add(r - c)
                occupied_diagonals.add(r + c)

    return (
        column not in occupied_columns
        and row - column not in occupied_diagonals
        and row + column not in occupied_diagonals
        and all(board[i][j] != 1 for i, j in zip(range(row), [column] * row))
        and all(
            board[i][j] != 1
            for i, j in zip(range(row - 1, -1, -1), range(column - 1, -1, -1))
        )
        and all(
            board[i][j] != 1
            for i, j in zip(range(row - 1, -1, -1), range(column + 1, n))
        )
    )


def correct_solve_count(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    count = 0

    def solve(row):
        nonlocal count
        if row >= n:
            count += 1
            return
        for col in range(n):
            if correct_is_safe(board, row, col):
                board[row][col] = 1
                solve(row + 1)
                board[row][col] = 0

    solve(0)
    return count


def buggy_solve_count(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    count = 0
    occupied_columns = set()
    occupied_diagonals = set()

    def is_safe(row, column):
        return (
            column not in occupied_columns
            and row - column not in occupied_diagonals
            and row + column not in occupied_diagonals
            and all(board[i][j] != 1 for i, j in zip(range(row), [column] * row))
            and all(
                board[i][j] != 1
                for i, j in zip(
                    range(row - 1, -1, -1), range(column - 1, -1, -1)
                )
            )
            and all(
                board[i][j] != 1
                for i, j in zip(range(row - 1, -1, -1), range(column + 1, n))
            )
        )

    def solve(row):
        nonlocal count
        if row >= n:
            count += 1
            return
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 1
                occupied_columns.add(col)
                occupied_diagonals.add(row - col)
                occupied_diagonals.add(row + col)
                solve(row + 1)
                occupied_columns.discard(col)
                occupied_diagonals.discard(row - col)
                occupied_diagonals.discard(row + col)
                board[row][col] = 0

    solve(0)
    return count


def run_test(label, input_value, correct_callable, buggy_callable):
    print(label)
    expected = correct_callable()
    actual = buggy_callable()
    if actual != expected:
        print("TEST FAILED")
        print("input:", input_value)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# TEST_1
board_1 = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
row_1, col_1 = 1, 1
run_test(
    "TEST_1",
    {"board": board_1, "row": row_1, "column": col_1},
    lambda: correct_is_safe(board_1, row_1, col_1),
    lambda: buggy_is_safe(board_1, row_1, col_1),
)

# TEST_2
board_2 = [
    [0, 1, 0],
    [0, 0, 0],
    [0, 0, 0],
]
row_2, col_2 = 1, 1
run_test(
    "TEST_2",
    {"board": board_2, "row": row_2, "column": col_2},
    lambda: correct_is_safe(board_2, row_2, col_2),
    lambda: buggy_is_safe(board_2, row_2, col_2),
)

# TEST_3
board_3 = [
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
row_3, col_3 = 1, 1
run_test(
    "TEST_3",
    {"board": board_3, "row": row_3, "column": col_3},
    lambda: correct_is_safe(board_3, row_3, col_3),
    lambda: buggy_is_safe(board_3, row_3, col_3),
)

# TEST_4
n_4 = 1
run_test(
    "TEST_4",
    {"n": n_4},
    lambda: correct_solve_count(n_4),
    lambda: buggy_solve_count(n_4),
)

# TEST_5
n_5 = 2
run_test(
    "TEST_5",
    {"n": n_5},
    lambda: correct_solve_count(n_5),
    lambda: buggy_solve_count(n_5),
)

# TEST_6
n_6 = 3
run_test(
    "TEST_6",
    {"n": n_6},
    lambda: correct_solve_count(n_6),
    lambda: buggy_solve_count(n_6),
)

# TEST_7
board_7 = [
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]
row_7, col_7 = 3, 2
run_test(
    "TEST_7",
    {"board": board_7, "row": row_7, "column": col_7},
    lambda: correct_is_safe(board_7, row_7, col_7),
    lambda: buggy_is_safe(board_7, row_7, col_7),
)

# TEST_8
board_8 = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
row_8, col_8 = 3, 1
run_test(
    "TEST_8",
    {"board": board_8, "row": row_8, "column": col_8},
    lambda: correct_is_safe(board_8, row_8, col_8),
    lambda: buggy_is_safe(board_8, row_8, col_8),
)

# TEST_9
n_9 = 4
run_test(
    "TEST_9",
    {"n": n_9},
    lambda: correct_solve_count(n_9),
    lambda: buggy_solve_count(n_9),
)

# TEST_10
board_10 = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 0, 0, 0],
]
row_10, col_10 = 3, 2
run_test(
    "TEST_10",
    {"board": board_10, "row": row_10, "column": col_10},
    lambda: correct_is_safe(board_10, row_10, col_10),
    lambda: buggy_is_safe(board_10, row_10, col_10),
)