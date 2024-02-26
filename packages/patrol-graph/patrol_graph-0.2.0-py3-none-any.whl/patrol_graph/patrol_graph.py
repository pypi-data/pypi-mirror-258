from pathlib import Path
from itertools import combinations
import pprint
import toml
import networkx as nx
import metis

config = toml.load("config.toml")
grade = config["grade"]
number = config["number_partitions"]
colors = config["colors"][0:number]

G = nx.DiGraph()


def get_edges():
    with open(Path("data") / f"edges{grade}.txt") as f:
        for line in f.readlines():
            first, *rest = line.split()
            for item in rest:
                G.add_edge(first, item, weight=config["normal"])


def get_besties():
    with open(Path("data") / f"besties{grade}.txt") as f:
        for line in f.readlines():
            first, *other = line.split()
            if other:
                G.add_edge(first, other[0], weight=config["bestie"])


def get_negs():
    with open(Path("data") / f"negs{grade}.txt") as f:
        for line in f.readlines():
            first, *other = line.split()
            if other:
                G.add_edge(first, other[0], weight=config["neg"])

def get_patrols():
    patrols = set()
    with open(Path("data") / f"patrols{grade}.txt") as f:
        for line in f.readlines():
            first, other, weight = line.split()
            if other:
                patrols.add(other)
                G.add_edge(first, other, weight=int(weight))
        for patrol, other in combinations(patrols, 2):
            G.add_edge(patrol, other, weight=-1000)



def configure_graph():
    G.graph["edge_weight_attr"] = "weight"


def partition_graph(graph, number):
    return metis.part_graph(metis.networkx_to_metis(graph), number)


def color_nodes(parts):
    nodeslist = list(G.nodes)
    for i, p in enumerate(parts):
        G.nodes[nodeslist[i]]["color"] = colors[p]


def draw_output():
    nx.drawing.nx_pydot.write_dot(G, Path("output") / "output.dot")


def make_patrols():
    patrols = {}

    for color in colors:
        patrols[color] = []
        for node in G.nodes:
            if G.nodes[node]["color"] == color:
                patrols[color].append(node)

    return patrols


def print_output(patrols):
    pprint.pprint(patrols)


def write_output(patrols):
    with open(Path("output") / "output.txt", "w") as f:
        for tup in zip(*patrols.values()):
            print(tup)
            f.write("\t".join(tup) + "\n")


def main():
    get_edges()
    get_besties()
    get_negs()
    get_patrols()
    configure_graph()
    edgecuts, parts = partition_graph(G, number)
    color_nodes(parts)
    draw_output()
    patrols = make_patrols()
    print_output(patrols)
    write_output(patrols)


if __name__ == "__main__":
    main()
