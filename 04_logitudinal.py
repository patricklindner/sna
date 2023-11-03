from itertools import islice

import matplotlib.pyplot as plt
import networkx as nx

from communities import process_girvan_newman
from util import load_graph

graphs = load_graph("data/soc-redditHyperlinks-title.tsv", group_by_year=True)

print("graph loaded")
# find common nodes
common_nodes = graphs.get(2014).nodes & graphs.get(2015).nodes & graphs.get(2016).nodes & graphs.get(2017).nodes

print("common nodes found")
for year in graphs:
    graph = graphs.get(year).to_undirected(reciprocal=True)
    largest_of_year = list()
    for connected_comp in nx.connected_components(graph):
        if len(connected_comp) > len(largest_of_year):
            largest_of_year = connected_comp

    print("largest comp of year " + str(year), len(largest_of_year))
    communities = process_girvan_newman(graph.subgraph(largest_of_year))
    for community in islice(communities, 3):
        print(community)
    # print("communities calculated, found " + str(len(list(communities))))
    # nx.write_graphml(graph.subgraph(largest_of_year), "generated/"+str(year)+"_largest_cc.graphml")

# for i in range(2013, 2018):
#    print(graphs.get(i).subgraph(common_nodes))
