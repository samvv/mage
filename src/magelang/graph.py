

from collections.abc import Sequence
from typing import Generator, Iterator

from magelang.util import nonnull


class MultiDict[K, V]:

    def __init__(self) -> None:
        self._mapping = dict[K, list[V]]()
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def add(self, k: K, v: V) -> None:
        vs = self._mapping.get(k)
        if vs is None:
            vs = self._mapping[k] = []
        vs.append(v)
        self._count += 1

    def __contains__(self, k: K) -> bool:
        return k in self._mapping

    def __getitem__(self, k: K) -> Sequence[V]:
        return self._mapping.get(k, [])

    def __iter__(self) -> Iterator[K]:
        return iter(self._mapping)

    def items(self) -> Iterator[tuple[K, V]]:
        for k, vs in self._mapping.items():
            for v in vs:
                yield k, v

    def clear(self) -> None:
        self._count = 0
        self._mapping.clear()


class DGraph[V, L]:

    def __init__(self) -> None:
        self._src_to_dst = MultiDict[V, tuple[V, L]]()
        self._dst_to_src = MultiDict[V, tuple[V, L]]()
        self._vertices = set[V]()
        self._edge_count = 0

    def add_vertex(self, v: V) -> None:
        self._vertices.add(v)

    def add_edge(self, src: V, dst: V, label: L) -> None:
        self._src_to_dst.add(src, (dst, label))
        self._dst_to_src.add(dst, (src, label))
        self._vertices.add(src)
        self._vertices.add(dst)
        self._edge_count += 1

    def count_vertices(self) -> int:
        return len(self._vertices)

    def count_edges(self) -> int:
        return self._edge_count

    def get_vertices(self) -> Iterator[V]:
        return iter(self._vertices)

    def outgoing_edges(self, src: V) -> Iterator[tuple[V, L]]:
        return iter(self._src_to_dst[src])

    def incoming_edges(self, dst: V) -> Iterator[tuple[V, L]]:
        return iter(self._dst_to_src[dst])

    def outgoing_vertices(self, src: V) -> Iterator[V]:
        for v, _ in self.outgoing_edges(src):
            yield v

    def incoming_vertices(self, dst: V) -> Iterator[V]:
        for v, _ in self.incoming_edges(dst):
            yield v

    def clear(self) -> None:
        self._src_to_dst.clear()
        self._dst_to_src.clear()
        self._vertices.clear()
        self._edge_count = 0

class ToposortVertexData:
    index: int | None = None
    lowlink: int | None = None
    on_stack: bool = False

def toposort[V, L](graph: DGraph[V, L]) -> Iterator[list[V]]:

    mapping = dict[V, ToposortVertexData]()
    index = 0
    stack = list[V]()

    def get_data(v: V) -> ToposortVertexData:
        result = mapping.get(v)
        if result is not None:
            return result
        to_insert = ToposortVertexData()
        mapping[v] = to_insert
        return to_insert

    def strongconnect(v: V) -> Generator[list[V]]:

        nonlocal index

        v_data = get_data(v)
        v_data.index = index
        v_data.lowlink = index
        index += 1
        stack.append(v)
        v_data.on_stack = True

        for w in graph.outgoing_vertices(v):
            w_data = get_data(w)
            if w_data.index is None:
                yield from strongconnect(w)
                v_data.lowlink = min(v_data.lowlink, nonnull(w_data.lowlink))
            elif w_data.on_stack:
                v_data.lowlink = min(v_data.lowlink, w_data.index)

        if v_data.lowlink == v_data.index:
            scc = list[V]()
            while True:
                w = stack.pop()
                w_data = get_data(w)
                w_data.on_stack = False
                scc.append(w)
                if w == v:
                    break
            yield scc

    for v in graph.get_vertices():
        if v not in mapping:
            yield from strongconnect(v)
