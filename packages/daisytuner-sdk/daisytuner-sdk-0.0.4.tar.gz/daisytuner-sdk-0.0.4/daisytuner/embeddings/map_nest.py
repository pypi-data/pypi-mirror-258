import dace

from typing import Set

from dace.sdfg.state import StateSubgraphView
from dace.sdfg.analysis.cutout import SDFGCutout


class MapNest(StateSubgraphView):
    def __init__(self, state: dace.SDFGState, root: dace.nodes.MapEntry) -> None:
        assert isinstance(root, dace.nodes.MapEntry) and state.entry_node(root) is None

        # Collect all nodes in subgraph
        map_exit = state.exit_node(root)
        subgraph_nodes = set(state.all_nodes_between(root, map_exit))
        subgraph_nodes.add(root)
        subgraph_nodes.add(map_exit)

        for edge in state.in_edges(root):
            # Ignore happens-before memlets
            if edge.data.data is None:
                continue

            for edge_ in state.memlet_path(edge):
                subgraph_nodes.add(edge_.src)

            access_node: dace.nodes.AccessNode = state.memlet_path(edge)[0].src
            if "views" in access_node.in_connectors:
                subgraph_nodes.add(state.predecessors(access_node)[0])
        for edge in state.out_edges(map_exit):
            for edge_ in state.memlet_path(edge):
                subgraph_nodes.add(edge_.dst)

            access_node: dace.nodes.AccessNode = state.memlet_path(edge)[-1].dst
            if "views" in access_node.out_connectors:
                subgraph_nodes.add(state.successors(access_node)[0])

        super().__init__(state, list(subgraph_nodes))
        self._root = root
        self._state = state

    @property
    def sdfg(self) -> dace.SDFG:
        return self._state.parent

    @property
    def state(self) -> dace.SDFGState:
        return self._state

    @property
    def root(self) -> dace.nodes.MapEntry:
        return self._root

    def inputs(self, wcr_as_input: bool = True) -> Set[dace.nodes.AccessNode]:
        nodes = set()
        for dnode in self.data_nodes():
            if self.in_degree(dnode) == 0:
                nodes.add(dnode)
            elif (
                self.out_degree(dnode) == 0
                and wcr_as_input
                and any(
                    [
                        e.data is not None and e.data.wcr is not None
                        for e in self.in_edges(dnode)
                    ]
                )
            ):
                nodes.add(dnode)

        return nodes

    def outputs(self) -> Set[dace.nodes.AccessNode]:
        nodes = set()
        for dnode in self.data_nodes():
            if self.out_degree(dnode) == 0:
                nodes.add(dnode)

        return nodes

    def as_cutout(self) -> dace.SDFG:
        cutout = SDFGCutout.singlestate_cutout(
            self._graph,
            *self.nodes(),
            make_copy=True,
            make_side_effects_global=False,
            use_alibi_nodes=False,
            symbols_map=self._graph.parent.constants,
        )
        for dnode in cutout.start_state.data_nodes():
            if cutout.start_state.out_degree(dnode) == 0:
                cutout.arrays[dnode.data].transient = False

        return cutout
