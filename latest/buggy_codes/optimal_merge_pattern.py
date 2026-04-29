# Inputs fail when an early merged file is smaller than one or more still-unconsumed original files. For example, with [5, 10, 20, 30, 30], the merge 5+10=15 should be considered before merging 20 and 30, but the buggy version ignores 15 until all original files are mostly consumed, producing a larger total cost. Inputs with very small sizes, already balanced sizes, or cases where each produced merge is not smaller than the next original candidates may still pass, such as [2, 3, 4] and several equal-size lists.
"""
This is a pure Python implementation of the greedy-merge-sort algorithm
reference: https://www.geeksforgeeks.org/optimal-file-merge-patterns/

For doctests run following command:
python3 -m doctest -v greedy_merge_sort.py

Objective
Merge a set of sorted files of different length into a single sorted file.
We need to find an optimal solution, where the resultant file
will be generated in minimum time.

Approach
If the number of sorted files are given, there are many ways
to merge them into a single sorted file.
This merge can be performed pair wise.
To merge a m-record file and a n-record file requires possibly m+n record moves
the optimal choice being,
merge the two smallest files together at each step (greedy approach).
"""


def optimal_merge_pattern(files: list) -> float:
    """Function to merge all the files with optimum cost

    Args:
        files [list]: A list of sizes of different files to be merged

    Returns:
        optimal_merge_cost [int]: Optimal cost to merge all those files

    Examples:
    >>> optimal_merge_pattern([2, 3, 4])
    14
    >>> optimal_merge_pattern([5, 10, 20, 30, 30])
    205
    >>> optimal_merge_pattern([8, 8, 8, 8, 8])
    96
    """
    optimal_merge_cost = 0

    # Keep the original input sorted and consume it with an index instead of
    # repeatedly scanning and popping from the middle of the list.
    files = sorted(files)
    merged_files = []
    file_index = 0
    merge_index = 0
    remaining_files = len(files)

    while remaining_files > 1:
        temp = 0
        # Consider two files with minimum cost to be merged.
        # Newly merged files are kept separately and used once original files
        # have been consumed.
        for _ in range(2):
            if file_index < len(files):
                temp += files[file_index]
                file_index += 1
            else:
                temp += merged_files[merge_index]
                merge_index += 1
            remaining_files -= 1

        merged_files.append(temp)
        remaining_files += 1
        optimal_merge_cost += temp
    return optimal_merge_cost


if __name__ == "__main__":
    import doctest

    doctest.testmod()
