# The function will pass on graphs that are simple paths, isolated vertices, or cases where every reachable vertex lies along the first DFS branch selected by the neighbor ordering. It will fail on branching graphs where some reachable vertices are only accessible through later neighbors of an already visited vertex. In those cases, the traversal returns a strict subset of the reachable component because skipped siblings are never pushed or processed.
'''Non recursive implementation of a DFS algorithm.'''

from __future__ import annotations


def depth_first_search(graph: dict, start: str) -> set[str]:
    '''Depth First Search on Graph
    :param graph: directed graph in dictionary format
    :param start: starting vertex as a string
    :returns: the trace of the search
    >>> input_G = { 'A': ['B', 'C', 'D'], 'B': ['A', 'D', 'E'],
    ... 'C': ['A', 'F'], 'D': ['B', 'D'], 'E': ['B', 'F'],
    ... 'F': ['C', 'E', 'G'], 'G': ['F'] }
    >>> output_G = list({'A', 'B', 'C', 'D', 'E', 'F', 'G'})
    >>> all(x in output_G for x in list(depth_first_search(input_G, 'A')))
    True
    >>> all(x in output_G for x in list(depth_first_search(input_G, 'G')))
    True
    '''
    explored, stack = set(), [start]
    next_child = {start: 0}

    while stack:
        v = stack.pop()
        if v in explored:
            continue

        explored.add(v)
        neighbors = list(reversed(graph[v]))
        child_index = next_child.get(v, 0)

        while child_index < len(neighbors):
            adj = neighbors[child_index]
            child_index += 1
            next_child[v] = child_index

            if adj not in explored:
                next_child.setdefault(adj, 0)
                stack.append(adj)
                if graph.get(adj):
                    break

    return explored


G = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'D'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F'],
}

if __name__ == '__main__':
    import doctest

    doctest.testmod()
    print(depth_first_search(G, 'A'))