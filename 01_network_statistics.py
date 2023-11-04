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

    centrality_values = list(degree_centrality.values())

    centrality_values = list(degree_centrality.values())
    plt.cla()
    plt.hist(centrality_values, bins=20, alpha=0.5, color='b')
    plt.title("Degree Centrality Histogram")
    plt.xlabel("Degree Centrality")
    plt.ylabel("Frequency")

    # Display the histogram
    plt.show()

    centrality_values = list(closeness_centrality.values())
    plt.cla()
    plt.hist(centrality_values, bins=20, alpha=0.5, color='b')
    plt.title("Closeness Centrality Histogram")
    plt.xlabel("Closeness Centrality")
    plt.ylabel("Frequency")

    # Display the histogram
    plt.show()

    centrality_values = list(betweenness_centrality.values())
    plt.cla()
    plt.hist(centrality_values, bins=20, alpha=0.5, color='b')
    plt.title("Betweenness Centrality Histogram")
    plt.xlabel("Betweenness Centrality")
    plt.ylabel("Frequency")

    # Display the histogram
    plt.show()

    uG = G.to_undirected(reciprocal=True)

    d = dict(nx.degree_centrality(G))
    nx.draw(uG, with_labels=True, font_size=9, nodelist=d, node_size=[v * 1000 for v in d.values()])
    plt.show()
    plt.cla()
    d = dict(nx.betweenness_centrality(G))
    nx.draw(uG, with_labels=True, font_size=9, nodelist=d, node_size=[v * 1000 for v in d.values()])
    plt.show()


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

    strongly_connected_components = list(nx.strongly_connected_components(G))
    weakly_connected_components = list(nx.weakly_connected_components(G))

    # Calculate the sizes of the strongly connected components
    s_component_sizes = [len(component) for component in strongly_connected_components]
    print(sorted(s_component_sizes))
    w_component_sizes = [len(component) for component in weakly_connected_components]
    print(sorted(w_component_sizes))

    # Plot a histogram of the component sizes
    plt.hist(component_sizes, bins=20, alpha=0.5, color='b', edgecolor='black', log=True)
    plt.xlabel('Weakly Connected Component Size')
    plt.ylabel('Frequency')
    plt.title('Weakly Connected Component Size Histogram')
    plt.show()

    # Plot a histogram of the component sizes
    plt.hist(sorted(component_sizes, reverse=True)[1:], bins=20, alpha=0.5, color='b', edgecolor='black', log=True)
    plt.xlabel('Weakly Connected Component Size')
    plt.ylabel('Frequency')
    plt.title('Weakly Connected Component Size Histogram')
    plt.show()


G = load_graph("data/soc-redditHyperlinks-title.tsv")

G = G.subgraph(list(G.nodes)[:])
print_stats(G)