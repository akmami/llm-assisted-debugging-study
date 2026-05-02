def correct_match_word_pattern(pattern: str, input_string: str) -> bool:
    def backtrack(pattern_index: int, str_index: int) -> bool:
        if pattern_index == len(pattern) and str_index == len(input_string):
            return True
        if pattern_index == len(pattern) or str_index == len(input_string):
            return False

        char = pattern[pattern_index]
        if char in pattern_map:
            mapped_str = pattern_map[char]
            if input_string.startswith(mapped_str, str_index):
                return backtrack(pattern_index + 1, str_index + len(mapped_str))
            return False

        for end in range(str_index + 1, len(input_string) + 1):
            substr = input_string[str_index:end]
            if substr in str_map:
                continue
            pattern_map[char] = substr
            str_map[substr] = char
            if backtrack(pattern_index + 1, end):
                return True
            del pattern_map[char]
            del str_map[substr]
        return False

    pattern_map = {}
    str_map = {}
    return backtrack(0, 0)


def buggy_match_word_pattern(pattern: str, input_string: str) -> bool:

    def backtrack(pattern_index: int, str_index: int) -> bool:
        """
        >>> backtrack(0, 0)
        True

        >>> backtrack(0, 1)
        True

        >>> backtrack(0, 4)
        False
        """
        if pattern_index == len(pattern) and str_index == len(input_string):
            return True
        if pattern_index == len(pattern) or str_index == len(input_string):
            return False

        state_key = (pattern_index, str_index)
        if state_key in failed_states:
            return False

        char = pattern[pattern_index]
        if char in pattern_map:
            mapped_str = pattern_map[char]
            if input_string.startswith(mapped_str, str_index):
                return backtrack(pattern_index + 1, str_index + len(mapped_str))
            else:
                return False
        ends = list(range(str_index + 1, len(input_string) + 1))
        ends.sort(key=lambda end: ((end - str_index) % 2, end))
        for end in ends:
            substr = input_string[str_index:end]
            if substr in str_map:
                continue
            pattern_map[char] = substr
            str_map[substr] = char
            if backtrack(pattern_index + 1, end):
                return True
            del pattern_map[char]
            del str_map[substr]
        failed_states.add(state_key)
        return False

    pattern_map: dict[str, str] = {}
    str_map: dict[str, str] = {}
    failed_states: set[tuple[int, int]] = set()
    return backtrack(0, 0)



def run_test(label, pattern, input_string):
    print(label)
    expected = correct_match_word_pattern(pattern, input_string)
    actual = buggy_match_word_pattern(pattern, input_string)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"pattern": pattern, "input_string": input_string})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


# Passing tests
run_test("TEST_1", "aba", "GraphTreesGraph")
run_test("TEST_2", "xyx", "PythonRubyPython")
run_test("TEST_3", "GG", "PythonJavaPython")
run_test("TEST_4", "", "")
run_test("TEST_5", "", "x")
run_test("TEST_6", "a", "hello")
run_test("TEST_7", "aaaa", "xyzxyzxyzxyz")
run_test("TEST_8", "ab", "aa")
run_test("TEST_9", "aba", "catdogmouse")
run_test("TEST_10", "abc", "ab")

# Failing tests
run_test("TEST_11", "abca", "abcdab")
run_test("TEST_12", "abca", "abcdEFab")
run_test("TEST_13", "abca", "xyzpqxyz")
run_test("TEST_14", "abca", "aBcDaB")
run_test("TEST_15", "abca", "redblueXred")