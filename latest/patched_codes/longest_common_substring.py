# Inputs fail when characters can be matched in order with gaps in text1, especially when text2 contains a contiguous block whose letters appear as a subsequence rather than a substring in text1. For example, cases like 'abcdef' versus 'xabded' can incorrectly build through the skipped 'c' and report a longer non-common slice such as 'bcde'. Cases where the true longest common substring is also the dominant contiguous diagonal match, such as empty inputs, single-character matches, or 'abcdef' versus 'bcd', may still pass.
'''
Longest Common Substring Problem Statement:
    Given two sequences, find the
    longest common substring present in both of them. A substring is
    necessarily continuous.

Example:
    ``abcdef`` and ``xabded`` have two longest common substrings, ``ab`` or ``de``.
    Therefore, algorithm should return any one of them.
'''


def longest_common_substring(text1: str, text2: str) -> str:
    '''
    Finds the longest common substring between two strings.

    >>> longest_common_substring('', '')
    ''
    >>> longest_common_substring('a','')
    ''
    >>> longest_common_substring('', 'a')
    ''
    >>> longest_common_substring('a', 'a')
    'a'
    >>> longest_common_substring('abcdef', 'bcd')
    'bcd'
    >>> longest_common_substring('abcdef', 'xabded')
    'ab'
    >>> longest_common_substring('GeeksforGeeks', 'GeeksQuiz')
    'Geeks'
    >>> longest_common_substring('abcdxyz', 'xyzabcd')
    'abcd'
    >>> longest_common_substring('zxabcdezy', 'yzabcdezx')
    'abcdez'
    >>> longest_common_substring('OldSite:GeeksforGeeks.org', 'NewSite:GeeksQuiz.com')
    'Site:Geeks'
    >>> longest_common_substring(1, 1)
    Traceback (most recent call last):
        ...
    ValueError: longest_common_substring() takes two strings for inputs
    '''

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


if __name__ == '__main__':
    import doctest

    doctest.testmod()