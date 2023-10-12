import csv
import networkx as nx


def load_graph(filename):
    G = nx.DiGraph()
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader)

        for line in tsv_reader:
            G.add_edge(line[0], line[1], weight=line[4])

    return G