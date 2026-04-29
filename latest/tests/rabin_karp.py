alphabet_size = 256
modulus = 1000003


def correct_rabin_karp(pattern: str, text: str) -> bool:
    p_len = len(pattern)
    t_len = len(text)
    if p_len > t_len:
        return False

    p_hash = 0
    text_hash = 0
    modulus_power = 1

    for i in range(p_len):
        p_hash = (ord(pattern[i]) + p_hash * alphabet_size) % modulus
        text_hash = (ord(text[i]) + text_hash * alphabet_size) % modulus
        if i == p_len - 1:
            continue
        modulus_power = (modulus_power * alphabet_size) % modulus

    for i in range(t_len - p_len + 1):
        if text_hash == p_hash and text[i : i + p_len] == pattern:
            return True
        if i == t_len - p_len:
            continue
        text_hash = (
            (text_hash - ord(text[i]) * modulus_power) * alphabet_size
            + ord(text[i + p_len])
        ) % modulus
    return False


def buggy_rabin_karp(pattern: str, text: str) -> bool:
    p_len = len(pattern)
    t_len = len(text)
    if p_len > t_len:
        return False

    p_hash = 0
    text_hash = 0
    modulus_power = 1

    for i in range(p_len):
        p_hash = (p_hash + ord(pattern[i]) * modulus_power) % modulus
        text_hash = (text_hash + ord(text[i]) * modulus_power) % modulus
        modulus_power = (modulus_power * alphabet_size) % modulus

    inverse_alphabet = pow(alphabet_size, modulus - 2, modulus)

    for i in range(t_len - p_len + 1):
        if text_hash == p_hash and text[i : i + p_len] == pattern:
            return True
        if i == t_len - p_len:
            continue
        text_hash = (
            (text_hash - ord(text[i])) * inverse_alphabet
            + ord(text[i + p_len]) * modulus_power
        ) % modulus
    return False


def run_test(label, pattern, text):
    print(label)
    expected = correct_rabin_karp(pattern, text)
    actual = buggy_rabin_karp(pattern, text)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"pattern": pattern, "text": text})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


run_test("TEST_1", "", "")
run_test("TEST_2", "", "abc")
run_test("TEST_3", "ab", "abc")
run_test("TEST_4", "abcd", "abc")
run_test("TEST_5", "d", "abc")
run_test("TEST_6", "Lü", "Lüsai")

run_test("TEST_7", "b", "ab")
run_test("TEST_8", "c", "abc")
run_test("TEST_9", "bc", "abc")
run_test("TEST_10", "aba", "xaba")
run_test("TEST_11", "ü", "aü")
run_test("TEST_12", "AAAB", "ABAAAAAB")