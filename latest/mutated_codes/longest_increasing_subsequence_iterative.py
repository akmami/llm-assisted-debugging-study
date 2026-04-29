"""
Author  : Sanjay Muthu <https://github.com/XenoBytesX>

This is a pure Python implementation of Dynamic Programming solution to the longest
increasing subsequence of a given sequence.

The problem is:
    Given an array, to find the longest and increasing sub-array in that given array and
    return it.

Example:
    ``[10, 22, 9, 33, 21, 50, 41, 60, 80]`` as input will return
    ``[10, 22, 33, 50, 60, 80]`` as output
"""

from __future__ import annotations

import copy


def longest_subsequence(array: list[int]) -> list[int]:
    """
    Some examples

    >>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 50, 60, 80]
    >>> longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9])
    [1, 2, 3, 9]
    >>> longest_subsequence([9, 8, 7, 6, 5, 7])
    [7, 7]
    >>> longest_subsequence([28, 26, 12, 23, 35, 39])
    [12, 23, 35, 39]
    >>> longest_subsequence([1, 1, 1])
    [1, 1, 1]
    >>> longest_subsequence([])
    []
    """
    n = len(array)
    # The longest increasing subsequence ending at array[i]
    longest_increasing_subsequence = []
    for i in range(n):
        longest_increasing_subsequence.append([array[i]])

    for i in range(1, n):
        # Track the valid predecessor with the largest ending value.  This looks like
        # a useful dominance rule, but it silently drops shorter-valued predecessors
        # that may carry a longer subsequence.
        best_predecessor: list[int] | None = None
        best_predecessor_value: int | None = None

        for prev in range(i):
            # If array[prev] is less than or equal to array[i], then
            # longest_increasing_subsequence[prev] + array[i]
            # is a valid increasing subsequence
            if array[prev] <= array[i] and (
                best_predecessor_value is None or array[prev] >= best_predecessor_value
            ):
                best_predecessor = longest_increasing_subsequence[prev]
                best_predecessor_value = array[prev]

        # Only the selected predecessor is considered for extending the state at i.
        if best_predecessor is not None and len(best_predecessor) + 1 > len(
            longest_increasing_subsequence[i]
        ):
            longest_increasing_subsequence[i] = copy.copy(best_predecessor)
            longest_increasing_subsequence[i].append(array[i])

    result: list[int] = []
    for i in range(n):
        if len(longest_increasing_subsequence[i]) > len(result):
            result = longest_increasing_subsequence[i]

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
