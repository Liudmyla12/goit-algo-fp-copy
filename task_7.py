from __future__ import annotations

import argparse
import random
from collections import Counter

import matplotlib.pyplot as plt


ANALYTIC = {
    2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
    7: 6/36,
    8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
}


def simulate(n: int, seed: int = 42):
    random.seed(seed)
    counts = Counter()
    for _ in range(n):
        s = random.randint(1, 6) + random.randint(1, 6)
        counts[s] += 1
    probs = {k: counts[k] / n for k in range(2, 13)}
    return counts, probs


def save_plot(probs_mc: dict[int, float], out: str):
    xs = list(range(2, 13))
    ys_mc = [probs_mc[x] for x in xs]
    ys_an = [ANALYTIC[x] for x in xs]

    plt.figure(figsize=(10, 5))
    plt.plot(xs, ys_mc, marker="o", label="Monte Carlo")
    plt.plot(xs, ys_an, marker="s", label="Analytic")
    plt.xticks(xs)
    plt.grid(True, alpha=0.3)
    plt.xlabel("Sum")
    plt.ylabel("Probability")
    plt.title("Two dice: Monte Carlo vs Analytic")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=200)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    counts, probs = simulate(args.n, args.seed)

    print("=== Two dice Monte Carlo ===")
    print(f"Rolls: {args.n}, seed={args.seed}\n")

    print("| Sum | Monte Carlo | Analytic | Abs diff |")
    print("|----:|------------:|---------:|---------:|")
    for s in range(2, 13):
        mc = probs[s]
        an = ANALYTIC[s]
        diff = abs(mc - an)
        print(f"| {s:>3} | {mc:>10.6f} | {an:>8.6f} | {diff:>8.6f} |")

    if args.plot:
        out = "dice_probabilities.png"
        save_plot(probs, out)
        print(f"\n✅ Plot saved: {out}")


if __name__ == "__main__":
    main()
