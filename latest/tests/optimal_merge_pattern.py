def correct_optimal_merge_pattern(files: list) -> float:
    optimal_merge_cost = 0
    while len(files) > 1:
        temp = 0
        for _ in range(2):
            min_index = files.index(min(files))
            temp += files[min_index]
            files.pop(min_index)
        files.append(temp)
        optimal_merge_cost += temp
    return optimal_merge_cost


def buggy_optimal_merge_pattern(files: list) -> float:
    optimal_merge_cost = 0
    files = sorted(files)
    merged_files = []
    file_index = 0
    merge_index = 0
    remaining_files = len(files)

    while remaining_files > 1:
        temp = 0
        for _ in range(2):
            if file_index < len(files):
                temp += files[file_index]
                file_index += 1
            else:
                temp += merged_files[merge_index]
                merge_index += 1
            remaining_files -= 1

        merged_files.append(temp)
        remaining_files += 1
        optimal_merge_cost += temp
    return optimal_merge_cost


def run_test(label, data):
    print(label)
    expected = correct_optimal_merge_pattern(list(data))
    actual = buggy_optimal_merge_pattern(list(data))
    if actual != expected:
        print("TEST FAILED")
        print("input:", data)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# Passing tests
run_test("TEST_1", [])
run_test("TEST_2", [7])
run_test("TEST_3", [2, 3])
run_test("TEST_4", [2, 3, 4])
run_test("TEST_5", [8, 8, 8, 8, 8])
run_test("TEST_6", [1, 1, 2, 2])

# Failing tests
run_test("TEST_7", [1, 2, 3, 4])
run_test("TEST_8", [5, 10, 20, 30, 30])
run_test("TEST_9", [0, 0, 5, 6])
run_test("TEST_10", [30, 5, 30, 10, 20])
run_test("TEST_11", [1, 2, 100, 101])