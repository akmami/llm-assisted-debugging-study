def correct_longest_common_substring(text1: str, text2: str) -> str:
    if not (isinstance(text1, str) and isinstance(text2, str)):
        raise ValueError("longest_common_substring() takes two strings for inputs")

    if not text1 or not text2:
        return ""

    text1_length = len(text1)
    text2_length = len(text2)

    dp = [[0] * (text2_length + 1) for _ in range(text1_length + 1)]
    end_pos = 0
    max_length = 0

    for i in range(1, text1_length + 1):
        for j in range(1, text2_length + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                if dp[i][j] > max_length:
                    end_pos = i
                    max_length = dp[i][j]

    return text1[end_pos - max_length : end_pos]


def buggy_longest_common_substring(text1: str, text2: str) -> str:
    if not (isinstance(text1, str) and isinstance(text2, str)):
        raise ValueError('longest_common_substring() takes two strings for inputs')

    if not text1 or not text2:
        return ''

    text1_length = len(text1)
    text2_length = len(text2)

    if text1_length <= 2 or text2_length <= 2:
        max_size = min(text1_length, text2_length)
        for size in range(max_size, 0, -1):
            for start in range(text2_length - size + 1):
                candidate = text2[start : start + size]
                if candidate in text1:
                    return candidate
            for start in range(text1_length - size + 1):
                candidate = text1[start : start + size]
                if candidate in text2:
                    return candidate
        return ''

    dp = [[0] * (text2_length + 1) for _ in range(2)]
    previous_row = dp[0]
    end_pos = 0
    max_length = 0

    for i in range(1, text1_length + 1):
        current_row = previous_row[:]
        current_row[0] = 0
        dp[i % 2] = current_row

        for j in range(1, text2_length + 1):
            if text1[i - 1] == text2[j - 1]:
                current_row[j] = 1 + previous_row[j - 1]

            if current_row[j] > max_length:
                end_pos = i
                max_length = current_row[j]

        previous_row = current_row

    return text1[end_pos - max_length : end_pos]


def execute(func, *args):
    try:
        return ("RETURN", func(*args))
    except Exception as e:
        return ("EXCEPTION", type(e).__name__, str(e))


def run_test(label, text1, text2):
    expected = execute(correct_longest_common_substring, text1, text2)
    actual = execute(buggy_longest_common_substring, text1, text2)

    if actual != expected:
        print(label, "TEST FAILED")
        print("input:", (text1, text2))
        print("expected:", expected)
        print("got:", actual)
    else:
        print(label, "TEST PASSED")


# Passing tests
run_test("TEST_1", "", "")
run_test("TEST_2", "a", "")
run_test("TEST_3", "a", "a")
run_test("TEST_4", "abcdef", "bcd")
run_test("TEST_5", "abc", "def")
run_test("TEST_6", "banana", "banana")
run_test("TEST_7", 1, 1)

# Failing tests
run_test("TEST_8", "abc", "ac")
run_test("TEST_9", "abcd", "ad")
run_test("TEST_10", "abcdef", "xabded")
run_test("TEST_11", "abXcd", "abcd")
run_test("TEST_12", "axbycz", "abc")