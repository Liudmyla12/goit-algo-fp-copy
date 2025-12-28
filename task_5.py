from __future__ import annotations

import os
import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
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


def build_nx_graph(root: Node):
    g = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(g, root, pos)
    return g, pos


def hex_color(step: int, total: int) -> str:
    # темний -> світлий
    start = (20, 60, 160)
    end = (200, 230, 255)
    if total <= 1:
        r, g, b = end
    else:
        t = step / (total - 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
    return f"#{r:02X}{g:02X}{b:02X}"


def list_nodes(root: Node) -> list[Node]:
    # Зберемо всі ноди (без рекурсії — просто стек)
    res = []
    stack = [root]
    seen = set()
    while stack:
        n = stack.pop()
        if n.id in seen:
            continue
        seen.add(n.id)
        res.append(n)
        if n.right:
            stack.append(n.right)
        if n.left:
            stack.append(n.left)
    return res


def save_frame(g, pos, title: str, path: str):
    colors = [node[1]["color"] for node in g.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in g.nodes(data=True)}
    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(g, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def dfs_visual(root: Node, out_dir: str):
    g, pos = build_nx_graph(root)
    nodes = list_nodes(root)
    total = len(nodes)

    # скидаємо кольори
    for _, data in g.nodes(data=True):
        data["color"] = "skyblue"

    visited = set()
    stack = [root]
    order = []

    while stack:
        n = stack.pop()
        if n.id in visited:
            continue
        visited.add(n.id)
        order.append(n.id)

        # DFS: спочатку правий, потім лівий, щоб лівий обробився раніше
        if n.right:
            stack.append(n.right)
        if n.left:
            stack.append(n.left)

    for i, node_id in enumerate(order):
        g.nodes[node_id]["color"] = hex_color(i, total)
        save_frame(g, pos, f"DFS step {i+1}/{total}", os.path.join(out_dir, f"dfs_{i+1:02d}.png"))

    print(f"✅ DFS frames saved: {out_dir}")


def bfs_visual(root: Node, out_dir: str):
    g, pos = build_nx_graph(root)
    nodes = list_nodes(root)
    total = len(nodes)

    for _, data in g.nodes(data=True):
        data["color"] = "skyblue"

    visited = set()
    q = deque([root])
    order = []

    while q:
        n = q.popleft()
        if n.id in visited:
            continue
        visited.add(n.id)
        order.append(n.id)

        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)

    for i, node_id in enumerate(order):
        g.nodes[node_id]["color"] = hex_color(i, total)
        save_frame(g, pos, f"BFS step {i+1}/{total}", os.path.join(out_dir, f"bfs_{i+1:02d}.png"))

    print(f"✅ BFS frames saved: {out_dir}")


def main():
    # Дерево як у прикладі
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    out_dir = "traversal_output"
    os.makedirs(out_dir, exist_ok=True)

    dfs_visual(root, out_dir)
    bfs_visual(root, out_dir)


if __name__ == "__main__":
    main()
