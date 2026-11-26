"""Deutsche Bahn: cumulative 3D-printed parts, 2015-2025.

Data: 04_industries/rail/tables/04_rl_db_milestones.csv (DB press releases and reports quoting them).
Output: 04_rl_db_printed_parts.png next to this file. Style: Inter, grey data, one blue accent, no title.
Run: python 04_industries/rail/figures/04_rl_db_printed_parts.py
"""
import csv
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
TABLE = HERE.parent / "tables" / "04_rl_db_milestones.csv"

INK, QUIET, GRID, MUTED, ACCENT = "#1F2933", "#52606D", "#E4E7EB", "#9AA5B1", "#2A78D6"
plt.rcParams.update({"font.family": "Inter", "font.size": 11})


def year_frac(iso):
    d = date.fromisoformat(iso)
    return d.year + (d.timetuple().tm_yday - 1) / 365.25


rows = [r for r in csv.DictReader(TABLE.open(encoding="utf-8")) if r["parts"]]
xs = [year_frac(r["date"]) for r in rows]
ys = [int(r["parts"]) for r in rows]

fig, ax = plt.subplots(figsize=(10, 5.2), dpi=200)
ax.plot(xs, ys, color=MUTED, lw=2, zorder=2)
ax.scatter(xs[:-1], ys[:-1], s=40, color=MUTED, zorder=3)
ax.scatter(xs[-1:], ys[-1:], s=70, color=ACCENT, zorder=4)
for x, y, r in zip(xs, ys, rows):
    last = r is rows[-1]
    ax.annotate(f"{y:,}", (x, y), xytext=(-8, 9), textcoords="offset points", ha="right",
                color=INK, fontweight="bold" if last else "normal")

# start marker: first printed part (coat hook), 2015
ax.scatter([2015.5], [0], marker="D", s=40, color=QUIET, zorder=3, clip_on=False)
ax.annotate("First printed part: a coat hook (2015)", (2015.5, 0), xytext=(10, 8),
            textcoords="offset points", color=QUIET, fontsize=10)

ax.set_xlim(2015, 2026.5)
ax.set_ylim(0, 225000)
ax.set_xticks(range(2015, 2027))
ax.set_yticks([0, 50000, 100000, 150000, 200000])
ax.set_yticklabels(["0", "50k", "100k", "150k", "200k"])
ax.set_ylabel("Cumulative printed parts", color=QUIET)
ax.grid(axis="y", color=GRID)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(QUIET)
ax.tick_params(colors=QUIET, length=0)
fig.tight_layout()
fig.savefig(HERE / "04_rl_db_printed_parts.png")
