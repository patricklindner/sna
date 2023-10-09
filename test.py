import csv
import networkx as nx
import matplotlib.pyplot as plt


def load_graph(filename):
    G = nx.Graph()
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader)

        for line in tsv_reader:
            G.add_edge(line[0], line[1], weight=line[4])

    return G

def draw_first_x(G, x):
    nx.draw(G.subgraph(list(G.nodes)[:x]), with_labels=False, node_size=10)
    plt.show()

G = load_graph("data/soc-redditHyperlinks-title.tsv")

print(G)
print(nx.number_connected_components(G))

draw_first_x(G, 1000)
