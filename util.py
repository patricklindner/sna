import csv

from networkx import DiGraph


def load_graph(filename, group_by_year=False) -> DiGraph | dict[int, DiGraph]:
    solo_graph = DiGraph()
    graphs_by_year: dict[int, DiGraph] = {}
    with open(filename) as file:
        tsv_reader = csv.reader(file, delimiter="\t")
        next(tsv_reader)

        for line in tsv_reader:
            if group_by_year:
                year = int(line[3][0:4])
                if graphs_by_year.get(year) is None:
                    graphs_by_year[year] = DiGraph()
                g = graphs_by_year.get(year)
            else:
                g = solo_graph
            g.add_edge(line[0], line[1], weight=line[4])

    if group_by_year:
        return graphs_by_year
    else:
        return solo_graph
