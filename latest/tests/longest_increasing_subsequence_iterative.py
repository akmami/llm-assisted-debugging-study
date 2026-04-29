import copy


def correct_longest_subsequence(array):
    n = len(array)
    longest_increasing_subsequence = []
    for i in range(n):
        longest_increasing_subsequence.append([array[i]])

    for i in range(1, n):
        for prev in range(i):
            if array[prev] <= array[i] and len(longest_increasing_subsequence[prev]) + 1 > len(
                longest_increasing_subsequence[i]
            ):
                longest_increasing_subsequence[i] = copy.copy(longest_increasing_subsequence[prev])
                longest_increasing_subsequence[i].append(array[i])

    result = []
    for i in range(n):
        if len(longest_increasing_subsequence[i]) > len(result):
            result = longest_increasing_subsequence[i]

    return result


def buggy_longest_subsequence(array):
    n = len(array)
    longest_increasing_subsequence = []
    for i in range(n):
        longest_increasing_subsequence.append([array[i]])

    for i in range(1, n):
        best_predecessor = None
        best_predecessor_value = None

        for prev in range(i):
            if array[prev] <= array[i] and (
                best_predecessor_value is None or array[prev] >= best_predecessor_value
            ):
                best_predecessor = longest_increasing_subsequence[prev]
                best_predecessor_value = array[prev]

        if best_predecessor is not None and len(best_predecessor) + 1 > len(
            longest_increasing_subsequence[i]
        ):
            longest_increasing_subsequence[i] = copy.copy(best_predecessor)
            longest_increasing_subsequence[i].append(array[i])

    result = []
    for i in range(n):
        if len(longest_increasing_subsequence[i]) > len(result):
            result = longest_increasing_subsequence[i]

    return result


def run_test(label, arr):
    print(label)
    expected = correct_longest_subsequence(arr[:])
    actual = buggy_longest_subsequence(arr[:])
    if actual != expected:
        print("TEST FAILED")
        print("input:", arr)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")
    print()


run_test("TEST_1", [])
run_test("TEST_2", [1])
run_test("TEST_3", [1, 2, 3, 4])
run_test("TEST_4", [1, 1, 1])
run_test("TEST_5", [9, 8, 7, 6, 5, 7])
run_test("TEST_6", [10, 22, 9, 33, 21, 50, 41, 60, 80])
run_test("TEST_7", [5, 4, 3, 2, 2])

run_test("TEST_8", [2, 1, 1, 2])
run_test("TEST_9", [3, 1, 2, 3])
run_test("TEST_10", [5, 1, 1, 1, 5])
run_test("TEST_11", [28, 26, 12, 23, 35, 39])
run_test("TEST_12", [4, 8, 7, 5, 1, 12, 2, 3, 9])
run_test("TEST_13", [4, 1, 2, 4])