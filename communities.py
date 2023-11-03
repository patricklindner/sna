import csv
import itertools
import logging
import time

import networkx as nx
from matplotlib import pyplot as plt
from networkx import find_cliques, DiGraph, bridges as calc_bridges, Graph
from networkx.algorithms.community import girvan_newman, louvain_communities

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
    cliques_generator = find_cliques(undirected)
    cliques = [x for x in cliques_generator]
    histogram: dict[int, int] = dict()
    for clique in cliques:
        if len(clique) >= 3:
            if len(clique) in histogram:
                histogram[len(clique)] += 1
            else:
                histogram[len(clique)] = 1
    histogram = dict(sorted(histogram.items()))
    print(histogram)
    x = [f"{x}" for x, y in histogram.items()]
    y = [y for x, y in histogram.items()]
    plt.bar(x, y)
    plt.show()

    nodes = set()
    for clique in cliques:
        if len(clique) == 9:
            print(clique)
            for node in clique:
                nodes.add(node)

    print(nodes)
    print(len(nodes))
    nx.draw(g.subgraph(nodes), with_labels=True, edge_color="green")
    plt.show()

    persist(g.subgraph(nodes), "cliques-9")
    return cliques


def process_bridges(g: DiGraph):
    undirected = g.to_undirected(reciprocal=True)

    bridges = list(calc_bridges(undirected))
    print(len(bridges))
    print(bridges)
    histogram = dict()
    for bridge in bridges:
        if bridge[0] in histogram:
            histogram[bridge[0]] += 1
        else:
            histogram[bridge[0]] = 1
        if bridge[1] in histogram:
            histogram[bridge[1]] += 1
        else:
            histogram[bridge[1]] = 1

    print(dict(sorted(histogram.items(), key=lambda x: x[1])))


def process_girvan_newman(g, iterations):
    res = girvan_newman(g)
    current = 1
    start_iteration = time.time()
    logging.warning("Starting first iteration")
    for communities in itertools.islice(res, iterations):
        logging.warning(
            f"Iteration {str(current)}/{str(iterations)} completed in {(time.time() - start_iteration) / 60} minutes")
        start_iteration = time.time()
        current += 1

    return communities


def draw_ego(node):
    pass


def process_louvine(g):
    print("starting louvain")
    coms = louvain_communities(g, weight=None)
    print("louvain finished")

    coms = sorted(coms, key=lambda x: len(x))

    histogram = dict()
    for com in coms:
        if len(com) in histogram:
            histogram[len(com)] += 1
        else:
            histogram[len(com)] = 1

    print(histogram)
    print(coms[-1])

    coms2 = louvain_communities(g.subgraph(coms[-1]), weight=None)
    print(len(coms2))
    coms2 = sorted(coms2, key=lambda x: len(x))
    print(coms2[-1])

    nx.write_gexf(g.subgraph(coms2[-1]), "generated/cc.gexf")
    nx.write_edgelist(g.subgraph(coms2[-1]), "generated/cc.el")
    nx.write_gml(g.subgraph(coms2[-1]), "generated/cc.gml")



def persist(g, name):
    nx.write_gexf((g), f"generated/{name}.gexf")


def write_communities(communities):
    with open("generated/communities.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for community in communities:
            writer.writerow(community)


def read_communities():
    result = list()
    with open("generated/communities.csv") as file:
        reader = csv.reader(file)
        for line in reader:
            result.append(set(line))

    return tuple(result)


def process_negative_influence_score(g: DiGraph, normalize=True):
    page_ranks = dict(sorted(nx.pagerank(g).items(), key=lambda x: x[1]))
    ni_scores = dict()
    max_ni_score = 0
    for node, rank in page_ranks.items():
        edges = g.out_edges(node)
        if len(edges) > 0:
            negative_edges = [e for e in edges if g.get_edge_data(*e)["weight"] < 0]
            # node_negativity = sum(map(lambda e: g.get_edge_data(*e)["weight"], edges))
            fraction_negative = len(negative_edges) / len(edges)
            ni_score = rank * fraction_negative
            ni_scores[node] = ni_score
            # update max negativity score for normalizing
            if ni_score > max_ni_score:
                max_ni_score = ni_score

    # normalize the score
    if normalize:
        for node, ni_score in ni_scores.items():
            ni_scores[node] = ni_score / max_ni_score

    # sort
    ni_scores = dict(sorted(ni_scores.items(), key=lambda x: x[1]))
    nx.set_node_attributes(g, ni_scores, "ni_score")

    # fig, ax = plt.subplots()
    # ax.hist(list(ni_scores.values()), bins=100)
    # ax.set_yscale('log')
    # plt.xlabel("distribution")
    # plt.ylabel("ni_score")
    # plt.show()

    print(ni_scores)


    return ni_scores


def process_homophily_analysis(g: DiGraph):
    ni_scores = nx.get_node_attributes(g, "ni_score")
    negative_nodes = [node for node, score in ni_scores.items() if score > 0.02]
    # fraction negative
    p = len(negative_nodes) / len(ni_scores)
    min_cross_fraction = 2 * p * (1 - p)

    number_cross_edges = 0
    for (v1, v2), _ in g.edges.items():
        if v1 in negative_nodes and v2 not in negative_nodes:
            number_cross_edges += 1

    fraction_cross_edges = number_cross_edges / len(g.edges.items())

    print(min_cross_fraction, fraction_cross_edges)


if __name__ == '__main__':
    start = time.time()
    logging.warning("Loading graph")
    g = load_graph("data/soc-redditHyperlinks-title.tsv")
    # g = g.to_undirected(reciprocal=True)
    # g = g.subgraph(largest_connected_component(g))
    logging.warning("graph loaded")

    # nx.draw(nx.ego_graph(g, "leagueoflegends"), with_labels=True)
    # plt.show()
    process_negative_influence_score(g)
    #process_homophily_analysis(g)
