import networkx as nx
from roadNetwork import RoadNetwork
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edge('A', 'B', length=2)
    G.add_edge('B', 'C', length=1)
    G.add_edge('A', 'C', length=4)

    rn = RoadNetwork(G)
    src = rn.index_of['A']
    dst = rn.index_of['C']

    path_indices = rn.shortest_path_sparse(src, dst)
    print([rn.node_of[i] for i in path_indices])  # Should print shortest path like ['A', 'B', 'C']
    print(rn.sparse)
    print(rn.edge_travel_time(0,2))