# The buggy version passes searches with no substantial partial-match mismatch, such as direct matches, many non-overlapping patterns, and simple absent patterns. It fails on inputs where the pattern has a nontrivial prefix/suffix structure and a mismatch occurs after a partial match, especially when the valid occurrence overlaps with the failed partial occurrence. Examples include repeated or self-similar patterns such as `ABABX`, `AAAB`, `ababaca`, or longer prefix-reusing patterns embedded after misleading partial matches. In these cases, advancing `i` during fallback skips the text character that should be rechecked, causing the algorithm to miss existing matches or return a later match than the first one.
from __future__ import annotations


def knuth_morris_pratt(text: str, pattern: str) -> int:
    """
    The Knuth-Morris-Pratt Algorithm for finding a pattern within a piece of text
    with complexity O(n + m)

    1) Preprocess pattern to identify any suffixes that are identical to prefixes

        This tells us where to continue from if we get a mismatch between a character
        in our pattern and the text.

    2) Step through the text one character at a time and compare it to a character in
        the pattern updating our location within the pattern if necessary

    >>> kmp = "knuth_morris_pratt"
    >>> all(
    ...    knuth_morris_pratt(kmp, s) == kmp.find(s)
    ...    for s in ("kn", "h_m", "rr", "tt", "not there")
    ... )
    True
    """

    # 1) Construct the failure array
    failure = get_failure_array(pattern)

    # 2) Step through text searching for pattern
    i, j = 0, 0  # index into text, pattern
    while i < len(text):
        if pattern[j] == text[i]:
            if j == (len(pattern) - 1):
                return i - j
            j += 1

        # if this is a prefix in our pattern
        # just go back far enough to continue
        elif j > 0:
            fallback = failure[j - 1]
            shift = j - fallback
            i += shift
            j = fallback
            continue
        i += 1
    return -1


def get_failure_array(pattern: str) -> list[int]:
    """
    Calculates the new index we should go to if we fail a comparison
    :param pattern:
    :return:
    """
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Test 1)
    pattern = "abc1abc12"
    text1 = "alskfjaldsabc1abc1abc12k23adsfabcabc"
    text2 = "alskfjaldsk23adsfabcabc"
    assert knuth_morris_pratt(text1, pattern)
    assert knuth_morris_pratt(text2, pattern)

    # Test 2)
    pattern = "ABABX"
    text = "ABABZABABYABABX"
    assert knuth_morris_pratt(text, pattern)

    # Test 3)
    pattern = "AAAB"
    text = "ABAAAAAB"
    assert knuth_morris_pratt(text, pattern)

    # Test 4)
    pattern = "abcdabcy"
    text = "abcxabcdabxabcdabcdabcy"
    assert knuth_morris_pratt(text, pattern)

    # Test 5) -> Doctests
    kmp = "knuth_morris_pratt"
    assert all(
        knuth_morris_pratt(kmp, s) == kmp.find(s)
        for s in ("kn", "h_m", "rr", "tt", "not there")
    )

    # Test 6)
    pattern = "aabaabaaa"
    assert get_failure_array(pattern) == [0, 1, 0, 1, 2, 3, 4, 5, 2]
