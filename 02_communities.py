import networkx as nx
from matplotlib import pyplot as plt
from networkx import find_cliques, DiGraph, bridges
from networkx.algorithms.community import girvan_newman

from util import load_graph


def process_cliques(g: DiGraph):
    undirected = g.to_undirected(reciprocal=True)
    cliques = find_cliques(undirected)
    for clique in cliques:
        if len(clique) > 5:
            nx.draw(undirected.subgraph(clique), with_labels=True)
            plt.show()


def process_bridges(g: DiGraph):
    undirected = g.to_undirected(reciprocal=True)

    bridge = bridges(undirected)
    print(list(bridge))


def process_girvan_newman(g: DiGraph):
    communities = girvan_newman(g)
    for community in communities:
        print(community)


g = load_graph("data/soc-redditHyperlinks-title.tsv")

process_girvan_newman(g)


