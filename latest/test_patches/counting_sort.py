def correct_counting_sort(collection):
    if collection == []:
        return []

    coll_len = len(collection)
    coll_max = max(collection)
    coll_min = min(collection)

    counting_arr_length = coll_max + 1 - coll_min
    counting_arr = [0] * counting_arr_length

    for number in collection:
        counting_arr[number - coll_min] += 1

    for i in range(1, counting_arr_length):
        counting_arr[i] = counting_arr[i] + counting_arr[i - 1]

    ordered = [0] * coll_len

    for i in reversed(range(coll_len)):
        ordered[counting_arr[collection[i] - coll_min] - 1] = collection[i]
        counting_arr[collection[i] - coll_min] -= 1

    return ordered


def correct_counting_sort_string(string):
    return "".join([chr(i) for i in correct_counting_sort([ord(c) for c in string])])


def buggy_counting_sort(collection):
    if collection == []:
        return []

    coll_len = len(collection)
    coll_max = max(collection)
    coll_min = min(collection)

    counting_arr_length = coll_max + 1 - coll_min
    counting_arr = [0] * counting_arr_length

    for number in collection:
        counting_arr[number - coll_min] += 1

    originally_present = [count > 0 for count in counting_arr]
    previous_boundary = 0
    for i in range(1, counting_arr_length):
        if originally_present[i - 1]:
            previous_boundary = counting_arr[i - 1]
        else:
            previous_boundary = 0
        counting_arr[i] = counting_arr[i] + previous_boundary

    ordered = [0] * coll_len

    for i in reversed(range(coll_len)):
        ordered[counting_arr[collection[i] - coll_min] - 1] = collection[i]
        counting_arr[collection[i] - coll_min] -= 1

    return ordered


def buggy_counting_sort_string(string):
    return "".join([chr(i) for i in buggy_counting_sort([ord(c) for c in string])])


def run_list_test(label, data):
    expected = correct_counting_sort(data)
    actual = buggy_counting_sort(data)
    if actual != expected:
        print(label, "TEST FAILED")
        print("input:", data)
        print("expected:", expected)
        print("got:", actual)
    else:
        print(label, "TEST PASSED")


def run_string_test(label, data):
    expected = correct_counting_sort_string(data)
    actual = buggy_counting_sort_string(data)
    if actual != expected:
        print(label, "TEST FAILED")
        print("input:", data)
        print("expected:", expected)
        print("got:", actual)
    else:
        print(label, "TEST PASSED")


# Passing tests
run_list_test("TEST_1", [])
run_list_test("TEST_2", [7])
run_list_test("TEST_3", [3, 1, 2, 0])
run_list_test("TEST_4", [-1, 1, 0, -1, 1, 0])
run_string_test("TEST_5", "cbacba")
run_string_test("TEST_6", "")

# Failing tests
run_list_test("TEST_7", [0, 5, 3, 2, 2])
run_list_test("TEST_8", [1, 3])
run_list_test("TEST_9", [-2, -5, -45])
run_list_test("TEST_10", [0, 2, 2])
run_string_test("TEST_11", "thisisthestring")
run_string_test("TEST_12", "az")