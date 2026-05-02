from __future__ import annotations

RADIX = 10


def radix_sort_correct(list_of_ints: list[int]) -> list[int]:
    placement = 1
    max_digit = max(list_of_ints)
    while placement <= max_digit:
        buckets: list[list] = [[] for _ in range(RADIX)]
        for i in list_of_ints:
            tmp = int((i / placement) % RADIX)
            buckets[tmp].append(i)
        a = 0
        for b in range(RADIX):
            for i in buckets[b]:
                list_of_ints[a] = i
                a += 1
        placement *= RADIX
    return list_of_ints


def radix_sort_buggy(list_of_ints: list[int]) -> list[int]:
    placement = 1
    max_digit = max(list_of_ints)
    while placement <= max_digit:
        buckets: list[list] = [[] for _ in range(RADIX)]
        active_buckets: list[int] = []
        for i in list_of_ints:
            tmp = int((i / placement) % RADIX)
            if not buckets[tmp]:
                active_buckets.append(tmp)
            buckets[tmp].append(i)
        a = 0
        for b in sorted(active_buckets):
            while buckets[b]:
                list_of_ints[a] = buckets[b].pop()
                a += 1
        placement *= RADIX
    return list_of_ints


def run_test(label: str, data: list[int]) -> None:
    original = data[:]
    expected = radix_sort_correct(data[:])
    actual = radix_sort_buggy(data[:])
    if actual != expected:
        print(label)
        print("TEST FAILED")
        print("input:", original)
        print("expected:", expected)
        print("got:", actual)
    else:
        print(label)
        print("TEST PASSED")


# TEST_1 - simple single-digit input, should pass
run_test("TEST_1", [0, 5, 3, 2, 2])

# TEST_2 - single-digit distinct values, should pass
run_test("TEST_2", [9, 1, 4, 7])

# TEST_3 - single element, should pass
run_test("TEST_3", [42])

# TEST_4 - multi-digit but no bucket collisions across relevant passes, should pass
run_test("TEST_4", [30, 21, 12, 3])

# TEST_5 - another multi-digit case with distinct ones/tens digits, should pass
run_test("TEST_5", [45, 12, 34, 23])

# TEST_6 - minimal failing pattern with shared lower digits and differing higher digits
run_test("TEST_6", [10, 100, 0])

# TEST_7 - small adversarial case exposing instability
run_test("TEST_7", [21, 11, 12])

# TEST_8 - documented failure-style mixed-width input
run_test("TEST_8", [1, 100, 10, 1000])

# TEST_9 - range crossing a power of ten, should fail
run_test("TEST_9", list(range(15)))

# TEST_10 - larger shared-zero-digit adversarial case, should fail
run_test("TEST_10", [0, 10, 20, 100, 200])