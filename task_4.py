from __future__ import annotations

import argparse
import uuid

import matplotlib
matplotlib.use("TkAgg")  # IMPORTANT: before importing pyplot

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        graph.add_edge(node.id, node.left.id)
        l = x - 1 / 2**layer
        pos[node.left.id] = (l, y - 1)
        add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        r = x + 1 / 2**layer
        pos[node.right.id] = (r, y - 1)
        add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, title="Tree", out_file="heap.png", show=False):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)

    plt.savefig(out_file, dpi=150, bbox_inches="tight")
    print(f"✅ Heap plot saved: {out_file}")

    if show:
        plt.show(block=True)

    plt.close()


def heap_to_tree(heap: list[int]) -> Node | None:
    if not heap:
        return None

    nodes = [Node(v) for v in heap]

    for i in range(len(nodes)):
        left_i = 2 * i + 1
        right_i = 2 * i + 2
        if left_i < len(nodes):
            nodes[i].left = nodes[left_i]
        if right_i < len(nodes):
            nodes[i].right = nodes[right_i]

    return nodes[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true", help="Show the plot window")
    parser.add_argument("--out", default="heap.png", help="Output image filename")
    args = parser.parse_args()

    heap = [0, 4, 1, 5, 10, 3]
    root = heap_to_tree(heap)
    if root is None:
        print("Empty heap")
        return

    draw_tree(root, title="Binary Heap visualization", out_file=args.out, show=args.show)


if __name__ == "__main__":
    main()




