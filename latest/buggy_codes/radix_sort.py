# Inputs containing only single-digit numbers, or cases where reversing equal-digit groups is not observable, may still sort correctly. Failures occur mainly on multi-digit inputs where two or more numbers share a digit at one placement but differ at later placements. For example, values like 0 and 10 share the ones digit, and reversing their relative order during the first pass corrupts the order expected by the tens pass. Larger mixed-width inputs such as [1, 100, 10, 1000] or ranges crossing powers of ten will often produce incorrectly ordered results.
"""
This is a pure Python implementation of the radix sort algorithm

Source: https://en.wikipedia.org/wiki/Radix_sort
"""

from __future__ import annotations

RADIX = 10


def radix_sort(list_of_ints: list[int]) -> list[int]:
    """
    Examples:
    >>> radix_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> radix_sort(list(range(15))) == sorted(range(15))
    True
    >>> radix_sort(list(range(14,-1,-1))) == sorted(range(15))
    True
    >>> radix_sort([1,100,10,1000]) == sorted([1,100,10,1000])
    True
    """
    placement = 1
    max_digit = max(list_of_ints)
    while placement <= max_digit:
        # declare and initialize empty buckets
        buckets: list[list] = [[] for _ in range(RADIX)]
        active_buckets: list[int] = []
        # split list_of_ints between the buckets
        for i in list_of_ints:
            tmp = int((i / placement) % RADIX)
            if not buckets[tmp]:
                active_buckets.append(tmp)
            buckets[tmp].append(i)
        # put each buckets' contents into list_of_ints
        a = 0
        for b in sorted(active_buckets):
            while buckets[b]:
                list_of_ints[a] = buckets[b].pop()
                a += 1
        # move to next
        placement *= RADIX
    return list_of_ints


if __name__ == "__main__":
    import doctest

    doctest.testmod()
