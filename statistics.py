import csv

import networkx as nx


def load_graph(filename):
    G = nx.Graph()
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader)

        for line in tsv_reader:
            G.add_edge(line[0], line[1], weight=line[4])



    return G




G = load_graph("data/soc-redditHyperlinks-title.tsv")

print(nx.number_conncted_components(G))



