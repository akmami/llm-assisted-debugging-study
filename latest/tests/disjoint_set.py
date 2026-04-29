class CNode:
    def __init__(self, data: int) -> None:
        self.data = data
        self.rank = 0
        self.parent = self


def c_make_set(x: CNode) -> None:
    x.rank = 0
    x.parent = x


def c_find_set(x: CNode) -> CNode:
    if x != x.parent:
        x.parent = c_find_set(x.parent)
    return x.parent


def c_union_set(x: CNode, y: CNode) -> None:
    x, y = c_find_set(x), c_find_set(y)
    if x == y:
        return
    elif x.rank > y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank:
            y.rank += 1


class BNode:
    def __init__(self, data: int) -> None:
        self.data = data
        self.rank = 0
        self.parent = self


def b_make_set(x: BNode) -> None:
    x.rank = 0
    x.parent = x


def b_find_set(x: BNode) -> BNode:
    if x != x.parent:
        x.parent = b_find_set(x.parent)
    return x.parent


def b_union_set(x: BNode, y: BNode) -> None:
    x_root, y_root = x.parent, y.parent
    if x_root == y_root:
        return
    elif x.rank > y.rank:
        y.parent = x_root
    else:
        x.parent = y_root
        if x.rank == y.rank:
            y_root.rank += 1


def snapshot_components(nodes, find_fn):
    groups = {}
    for node in nodes:
        root = find_fn(node)
        groups.setdefault(id(root), []).append(node.data)
    return tuple(sorted(tuple(sorted(group)) for group in groups.values()))


def run_correct(n, ops):
    nodes = [CNode(i) for i in range(n)]
    for node in nodes:
        c_make_set(node)
    for op in ops:
        if op[0] == "union":
            _, a, b = op
            c_union_set(nodes[a], nodes[b])
        elif op[0] == "find":
            _, a = op
            c_find_set(nodes[a])
    return snapshot_components(nodes, c_find_set)


def run_buggy(n, ops):
    nodes = [BNode(i) for i in range(n)]
    for node in nodes:
        b_make_set(node)
    for op in ops:
        if op[0] == "union":
            _, a, b = op
            b_union_set(nodes[a], nodes[b])
        elif op[0] == "find":
            _, a = op
            b_find_set(nodes[a])
    return snapshot_components(nodes, b_find_set)


def run_test(label, n, ops):
    print(label)
    expected = run_correct(n, ops)
    actual = run_buggy(n, ops)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"n": n, "ops": ops})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


run_test("TEST_1", 0, [])
run_test("TEST_2", 1, [])
run_test("TEST_3", 2, [("union", 0, 1)])
run_test("TEST_4", 4, [("union", 0, 1), ("union", 2, 3), ("union", 1, 3)])
run_test("TEST_5", 4, [("union", 0, 1), ("union", 1, 2), ("union", 1, 3)])
run_test("TEST_6", 3, [("union", 0, 1), ("union", 0, 2)])
run_test("TEST_7", 4, [("union", 0, 1), ("union", 2, 3), ("union", 0, 2)])
run_test("TEST_8", 6, [("union", 0, 1), ("union", 1, 2), ("union", 3, 4), ("union", 3, 5)])
run_test("TEST_9", 4, [("union", 0, 1), ("union", 1, 2), ("union", 0, 3)])
run_test("TEST_10", 3, [("union", 0, 1), ("union", 1, 0), ("find", 0), ("find", 1)])
run_test("TEST_11", 3, [("union", 0, 1), ("union", 2, 1), ("union", 0, 2)])