import matplotlib.pyplot as plt

from util import load_graph


def get_subgraph_of_year():
    pass


graphs = load_graph("data/soc-redditHyperlinks-title.tsv", group_by_year=True)

print(graphs)
plt.plot(graphs.keys(), list(map(lambda graph: len(graph.edges), graphs.values())))
plt.show()
