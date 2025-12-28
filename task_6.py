from __future__ import annotations

import argparse


items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(budget: int):
    # сортуємо за calories/cost
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )
    chosen = []
    total_cost = 0
    total_cal = 0

    for name, data in ranked:
        if total_cost + data["cost"] <= budget:
            chosen.append(name)
            total_cost += data["cost"]
            total_cal += data["calories"]

    return chosen, total_cost, total_cal


def dynamic_programming(budget: int):
    names = list(items.keys())
    n = len(names)

    # dp[i][b] = max calories using first i items with budget b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]["cost"]
        cal = items[name]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]
            if cost <= b:
                candidate = dp[i - 1][b - cost] + cal
                if candidate > dp[i][b]:
                    dp[i][b] = candidate
                    keep[i][b] = True

    # reconstruct
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if keep[i][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]

    chosen.reverse()
    total_cost = sum(items[n]["cost"] for n in chosen)
    total_cal = sum(items[n]["calories"] for n in chosen)
    return chosen, total_cost, total_cal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=int, default=100)
    args = parser.parse_args()

    g = greedy_algorithm(args.budget)
    d = dynamic_programming(args.budget)

    print("=== Food selection ===")
    print(f"Budget: {args.budget}\n")

    print("Greedy:")
    print("  items   :", g[0])
    print("  cost    :", g[1])
    print("  calories:", g[2], "\n")

    print("DP (optimal):")
    print("  items   :", d[0])
    print("  cost    :", d[1])
    print("  calories:", d[2])


if __name__ == "__main__":
    main()
