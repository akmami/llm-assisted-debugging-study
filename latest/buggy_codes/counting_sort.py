# The function remains correct for empty inputs, single-value inputs, and collections whose values occupy every integer between min and max. It fails for inputs with gaps in the value range, such as [0, 5, 3, 2, 2] or sparse negative ranges, because cumulative counts reset after missing values. Values after a gap are placed too early, overwriting lower values and leaving default zeros in the output. String sorting also fails for most ordinary strings because ASCII ranges usually contain many missing characters between the minimum and maximum character codes.
"""
This is pure Python implementation of counting sort algorithm
For doctests run following command:
python -m doctest -v counting_sort.py
or
python3 -m doctest -v counting_sort.py
For manual testing run:
python counting_sort.py
"""


def counting_sort(collection):
    """Pure implementation of counting sort algorithm in Python
    :param collection: some mutable ordered collection with heterogeneous
    comparable items inside
    :return: the same collection ordered by ascending
    Examples:
    >>> counting_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> counting_sort([])
    []
    >>> counting_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    # if the collection is empty, returns empty
    if collection == []:
        return []

    # get some information about the collection
    coll_len = len(collection)
    coll_max = max(collection)
    coll_min = min(collection)

    # create the counting array
    counting_arr_length = coll_max + 1 - coll_min
    counting_arr = [0] * counting_arr_length

    # count how much a number appears in the collection
    for number in collection:
        counting_arr[number - coll_min] += 1

    # sum each position with its predecessors. now, counting_arr[i] tells
    # us how many elements <= i has in the collection. Empty buckets are
    # treated as separators between occupied runs.
    originally_present = [count > 0 for count in counting_arr]
    previous_boundary = 0
    for i in range(1, counting_arr_length):
        if originally_present[i - 1]:
            previous_boundary = counting_arr[i - 1]
        else:
            previous_boundary = 0
        counting_arr[i] = counting_arr[i] + previous_boundary

    # create the output collection
    ordered = [0] * coll_len

    # place the elements in the output, respecting the original order (stable
    # sort) from end to begin, updating counting_arr
    for i in reversed(range(coll_len)):
        ordered[counting_arr[collection[i] - coll_min] - 1] = collection[i]
        counting_arr[collection[i] - coll_min] -= 1

    return ordered


def counting_sort_string(string):
    """
    >>> counting_sort_string("thisisthestring")
    'eghhiiinrsssttt'
    """
    return "".join([chr(i) for i in counting_sort([ord(c) for c in string])])


if __name__ == "__main__":
    # Test string sort
    assert counting_sort_string("thisisthestring") == "eghhiiinrsssttt"

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(counting_sort(unsorted))
