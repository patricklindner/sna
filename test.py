import networkx as nx
import matplotlib.pyplot as plt

from util import load_graph


def draw_first_x(G, x):
    nx.draw(G.subgraph(list(G.nodes)[:x]), with_labels=False, node_size=10)
    plt.show()

def print_stats(G):
    print(f"number of nodes: {len(G.nodes)}")
    print(f"number of edges: {len(G.edges)}")

    degree_sequence = [d for n, d in G.degree()]
    in_degree_sequence = [d for n, d in G.in_degree()]
    out_degree_sequence = [d for n, d in G.out_degree()]

    print(f"degree_sequence: {sum(degree_sequence)}")
    print(f"in_degree_sequence: {G.in_degree()}")
    print(f"out_degree_sequence: {G.out_degree()}")

    degree_centrality = dict(sorted(nx.degree_centrality(G).items(), key=lambda item: item[1], reverse=True))
    betweenness_centrality = dict(sorted(nx.betweenness_centrality(G).items(), key=lambda item: item[1], reverse=True))
    closeness_centrality = dict(sorted(nx.closeness_centrality(G).items(), key=lambda item: item[1], reverse=True))

    print(f"degree_centrality: {degree_centrality}")
    print(f"betweenness_centrality: {betweenness_centrality}")
    print(f"closeness_centrality: {closeness_centrality}")

    print(f"clustering_coefficient: {nx.average_clustering(G)}")
    # print(f"diameter: {nx.diameter(G)}")
    print(f"density: {nx.density(G)}")
    print(f"number weakly connected components: {len(list(nx.weakly_connected_components(G)))}")
    print(f"number strongly connected components: {len(list(nx.strongly_connected_components(G)))}")

    undirected_G = G.to_undirected(reciprocal=True)
    connected_components = list(nx.connected_components(undirected_G))
    component_sizes = [len(component) for component in connected_components]
    print(f"connected components: {connected_components}")
    print(f"sizes of connected components: {sorted(component_sizes, reverse=True)}")


G = load_graph("data/soc-redditHyperlinks-title.tsv")

print_stats(G.subgraph(list(G.nodes)[:100]))

# draw_first_x(G, 1000)
