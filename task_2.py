from __future__ import annotations

import argparse
import math
import matplotlib.pyplot as plt


def draw_branch(ax, x1: float, y1: float, length: float, angle: float, depth: int) -> None:
    if depth == 0 or length <= 0:
        return

    x2 = x1 + length * math.cos(angle)
    y2 = y1 + length * math.sin(angle)
    ax.plot([x1, x2], [y1, y2], linewidth=1)

    # Дві гілки: ліво/право
    new_length = length * 0.72
    draw_branch(ax, x2, y2, new_length, angle + math.pi / 6, depth - 1)
    draw_branch(ax, x2, y2, new_length, angle - math.pi / 6, depth - 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=9, help="Рівень рекурсії (наприклад 7..12)")
    parser.add_argument("--out", type=str, default="pythagoras_tree.png")
    args = parser.parse_args()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect("equal")
    ax.axis("off")

    # Старт: знизу вгору
    draw_branch(ax, x1=0.0, y1=0.0, length=1.0, angle=math.pi / 2, depth=args.depth)

    plt.tight_layout()
    plt.savefig(args.out, dpi=200)
    print(f"✅ Saved: {args.out}")


if __name__ == "__main__":
    main()
