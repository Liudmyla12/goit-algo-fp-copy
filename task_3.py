from __future__ import annotations

import heapq
from typing import Dict, List, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


def dijkstra(graph: Graph, start: str) -> Tuple[Dict[str, float], Dict[str, str | None]]:
    dist = {v: float("inf") for v in graph}
    prev: Dict[str, str | None] = {v: None for v in graph}
    dist[start] = 0.0

    pq: list[tuple[float, str]] = [(0.0, start)]  # (distance, vertex)

    while pq:
        cur_dist, u = heapq.heappop(pq)
        if cur_dist > dist[u]:
            continue

        for v, w in graph[u]:
            nd = cur_dist + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


def reconstruct_path(prev: Dict[str, str | None], start: str, goal: str) -> list[str]:
    path = []
    cur: str | None = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == start else []


def main() -> None:
    # Приклад зваженого графа
    graph: Graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 5), ("D", 10)],
        "C": [("A", 2), ("B", 5), ("D", 3)],
        "D": [("B", 10), ("C", 3), ("E", 4)],
        "E": [("D", 4)],
    }

    start = "A"
    dist, prev = dijkstra(graph, start)

    print("=== Dijkstra (heapq) ===")
    print(f"Start: {start}")
    for v in dist:
        print(f" - {v}: {dist[v]}")

    goal = "E"
    path = reconstruct_path(prev, start, goal)
    print(f"Path {start}->{goal}: {path}")


if __name__ == "__main__":
    main()
