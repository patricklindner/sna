import itertools
import csv
import time

import networkx as nx
from matplotlib import pyplot as plt
from networkx import find_cliques, DiGraph, bridges, Graph
from networkx.algorithms.community import girvan_newman

from util import load_graph


def largest_connected_component(g: Graph):
    ccs = nx.connected_components(g)
    largest_cc = list()
    for cc in ccs:
        if len(cc) > len(largest_cc):
            largest_cc = cc
    return largest_cc


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


def process_girvan_newman(g: Graph, iterations: int):
    res = girvan_newman(g)
    current = 1
    for communities in itertools.islice(res, iterations):
        print("Iteration " + str(current) + " of " + str(iterations))
        current += 1

    return communities


def write_communities(communities: tuple[set[str]]):
    with open("generated/communities.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for community in communities:
            writer.writerow(community)


def read_communities() -> tuple[set[str]]:
    result = list()
    with open("generated/communities.csv") as file:
        reader = csv.reader(file)
        for line in reader:
            result.append(set(line))

    return tuple(result)



if __name__ == '__main__':
    start = time.time()
    # g = load_graph("data/soc-redditHyperlinks-title.tsv")
    # # #
    # g = g.to_undirected(reciprocal=False)
    # g = g.subgraph(largest_connected_component(g))
    #

    # nodes_with_degree = g.degree()
    # (largest_hub, degree) = sorted(nodes_with_degree, key=lambda x: x[1])[-1]
    #
    # print(largest_hub, degree)
    #
    # g = nx.ego_graph(g, largest_hub, radius=3)
    #
    # print(g)
    g = nx.fast_gnp_random_graph(100, 0.1)
    #
    # nx.draw(g)
    # plt.show()


    communities = process_girvan_newman(g, 10)
    print(f"end at {(time.time() - start) / 60 / 60}h")
    write_communities(communities)


    # print(read_communities())
    # nx.draw(g)
    # plt.show()


# process_girvan_newman(g)
