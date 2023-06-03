import json
import os

import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms import tree

from utils import distance, distance_tuple, hours


def view_surrounding(symbol, starting):
    with open("systems.json", "r") as f:
        data = json.load(f)

    initial_node = next(node for node in data if node["symbol"] == starting)
    print(f"Generating {symbol} - {initial_node}")
    near_nodes = []
    nodes = []
    positions = {}
    colors = []
    is_jump = {}
    for wp in data:
        if distance(initial_node, wp) < 10000:
            near_nodes.append(wp)
            nodes.append((wp["symbol"], {"pos": (wp["x"], wp["y"])}))
            positions[wp["symbol"]] = (wp["x"], wp["y"])

            has_jump_gate = False
            for i in wp['waypoints']:
                if i['type'] == "JUMP_GATE":
                    has_jump_gate = True
                    break
            is_jump[wp["symbol"]] = has_jump_gate

            if wp["x"] == initial_node["x"] or wp["x"] == initial_node["x"]:
                colors.append("green")
            elif has_jump_gate:
                colors.append("purple")
            elif len(wp["waypoints"]) == 0:
                colors.append("grey")
            else:
                colors.append("red")

    plt.figure(num=None, figsize=(40, 40), dpi=160)

    G = nx.Graph()
    G.add_nodes_from(nodes)

    edges = nx.geometric_edges(G, radius=3000)
    G.add_edges_from(edges)
    for edge in edges:
        x, y = edge[0], edge[1]
        current_distance = distance_tuple(positions[x], positions[y])
        if is_jump[x] and is_jump[y] and current_distance < 2000:
            G[x][y]['weight'] = 0
            G[x][y]['time'] = "0"
        else:
            G[x][y]['weight'] = distance_tuple(positions[x], positions[y])
            G[x][y]['time'] = "{:2.1f}".format(hours(current_distance))

    # mst = tree.minimum_spanning_edges(G, algorithm='kruskal', data=True)

    paths = nx.single_source_dijkstra_path(G, starting)
    dijkstra_edges = []
    for key, value in paths.items():
        for i in range(len(value) - 1):
            dijkstra_edges.append((value[i], value[i + 1]))

    # t = list(mst)[::]

    G.remove_edges_from(edges)
    G.add_edges_from(dijkstra_edges)

    nx.draw_networkx(G, pos=positions, node_color=colors, with_labels=True, font_size=5, node_size=5 * 50)
    nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=nx.get_edge_attributes(G, 'time'))

    os.makedirs("factions-origen", exist_ok=True)
    plt.savefig(f"factions-origen/{symbol}.png")
