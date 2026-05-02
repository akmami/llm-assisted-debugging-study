from __future__ import annotations


def correct_get_failure_array(pattern: str) -> list[int]:
    failure = [0]
    i = 0
    j = 1
    while j < len(pattern):
        if pattern[i] == pattern[j]:
            i += 1
        elif i > 0:
            i = failure[i - 1]
            continue
        j += 1
        failure.append(i)
    return failure


def correct_knuth_morris_pratt(text: str, pattern: str) -> int:
    failure = correct_get_failure_array(pattern)
    i, j = 0, 0
    while i < len(text):
        if pattern[j] == text[i]:
            if j == (len(pattern) - 1):
                return i - j
            j += 1
        elif j > 0:
            j = failure[j - 1]
            continue
        i += 1
    return -1


def buggy_get_failure_array(pattern: str) -> list[int]:
    failure = [0]
    i = 0
    j = 1
    while j < len(pattern):
        if pattern[i] == pattern[j]:
            i += 1
        elif i > 0:
            i = failure[i - 1]
            continue
        j += 1
        failure.append(i)
    return failure


def buggy_knuth_morris_pratt(text: str, pattern: str) -> int:
    failure = buggy_get_failure_array(pattern)
    i, j = 0, 0
    while i < len(text):
        if pattern[j] == text[i]:
            if j == (len(pattern) - 1):
                return i - j
            j += 1
        elif j > 0:
            fallback = failure[j - 1]
            shift = j - fallback
            i += shift
            j = fallback
            continue
        i += 1
    return -1


def run_test(label: str, text: str, pattern: str) -> None:
    print(label)
    expected = correct_knuth_morris_pratt(text, pattern)
    actual = buggy_knuth_morris_pratt(text, pattern)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"text": text, "pattern": pattern})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")
    print()


# Passing tests
run_test("TEST_1", "abcdef", "abc")
run_test("TEST_2", "zzzabczzz", "abc")
run_test("TEST_3", "zzzz", "ab")
run_test("TEST_4", "banana", "n")
run_test("TEST_5", "hi", "hello")
run_test("TEST_6", "aaaaa", "aaa")

# Failing tests
run_test("TEST_7", "aab", "ab")
run_test("TEST_8", "aabc", "abc")
run_test("TEST_9", "aaba", "aba")
run_test("TEST_10", "aababa", "aba")
run_test("TEST_11", "aabab", "abab")
run_test("TEST_12", "AAAAB", "AAAB")
run_test("TEST_13", "ABABZABABX", "ABABX")