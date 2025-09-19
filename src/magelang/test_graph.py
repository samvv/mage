
from .graph import DGraph, toposort


def test_toposort_simple_cycle():

    g = DGraph()
    g.add_edge('a', 'b', None)
    g.add_edge('b', 'c', None)
    g.add_edge('c', 'a', None)
    g.add_edge('d', 'a', None)
    g.add_edge('e', 'd', None)
    g.add_edge('f', 'd', None)
    g.add_vertex('g')

    sccs = list(toposort(g))

    assert(len(sccs) == 5)

    for scc in sccs:
        scc.sort()

    def index(x: str) -> int:
        for i, scc in enumerate(sccs):
            if scc[0] == x:
                return i
        raise RuntimeError(f"'{x}' not found")

    a = index('a')
    d = index('d')
    e = index('e')
    f = index('f')
    g = index('g')

    assert(a < d and a < e and a < f)

    assert(len(sccs[a]) == 3)
    assert('a' in sccs[a])
    assert('b' in sccs[a])
    assert('c' in sccs[a])
    assert(len(sccs[d]) == 1)
    assert('d' in sccs[d])
    assert(len(sccs[e]) == 1)
    assert('e' in sccs[e])
    assert(len(sccs[f]) == 1)
    assert('f' in sccs[f])
    assert(len(sccs[g]) == 1)
    assert('g' in sccs[g])
