#!/usr/bin/env python3
"""Generate a combined, GitHub-style contribution heatmap for the whole org.

GitHub has no org-level contribution graph, so we build one: pull weekly
commit activity (repos/{org}/{repo}/stats/commit_activity — 52 weeks of
per-day commit counts) for every listed repo, sum them day-by-day, and render
the familiar 53x7 green-square heatmap as an SVG committed to this repo and
embedded in profile/README.md.

Auth: uses the `gh` CLI's logged-in token, so private repos the caller can
read (e.g. CIRCA) are included in the totals. Repos that return 403/404 are
skipped with a note. The stats endpoint returns 202/{} while GitHub computes
a repo's stats — we retry a few times, then skip.

Run from the repo root:  python3 scripts/generate_contribution_graph.py
Output:                  profile/assets/contribution-graph.svg
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

ORG = "Verma-Lab"
REPOS = [
    "CIRCA",
    "platlas",
    "platlas-frontend",
    "platlas-backend",
    "Care-Bench",
    "hcc-rare-variant-analysis",
    "hepatic-fat-gwas",
    "pmbb_idp_gwas",
    "ECGFounder-ukb",
    "protoecgnet-ukb",
    ".github",
]
OUT = Path(__file__).resolve().parent.parent / "profile" / "assets" / "contribution-graph.svg"

CELL = 11          # square size
GAP = 4            # gap between squares
PITCH = CELL + GAP
LEFT = 34          # room for weekday labels
TOP = 84           # room for title + subtitle + breathing room + month labels

# GitHub's palettes (light, dark) — 5 buckets from empty to most active.
LIGHT = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
DARK = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def fetch_repo_activity(repo: str, tries: int = 5, wait: float = 6.0):
    """52 weeks of {week, days[7]} for one repo, or None if unavailable."""
    for attempt in range(tries):
        try:
            raw = subprocess.run(
                ["gh", "api", f"repos/{ORG}/{repo}/stats/commit_activity"],
                capture_output=True, text=True, timeout=60,
            )
        except Exception as e:  # gh missing / network death — give up on repo
            print(f"  {repo}: gh failed ({e})")
            return None
        if raw.returncode != 0:
            print(f"  {repo}: skipped ({raw.stderr.strip()[:80]})")
            return None
        try:
            data = json.loads(raw.stdout or "{}")
        except json.JSONDecodeError:
            data = {}
        if isinstance(data, list) and data:
            return data
        # {} => HTTP 202, stats still being computed server-side
        time.sleep(wait)
    print(f"  {repo}: stats never became ready — skipped")
    return None


def collect() -> tuple[dict[dt.date, int], list[str]]:
    counts: dict[dt.date, int] = defaultdict(int)
    included: list[str] = []
    for repo in REPOS:
        weeks = fetch_repo_activity(repo)
        if not weeks:
            continue
        total = 0
        for wk in weeks:
            start = dt.date.fromtimestamp(wk["week"])  # week starts Sunday
            for i, n in enumerate(wk.get("days", [])):
                if n:
                    counts[start + dt.timedelta(days=i)] += n
                    total += n
        included.append(repo)
        print(f"  {repo}: +{total}")
    return counts, included


def bucket(n: int, max_n: int) -> int:
    if n <= 0:
        return 0
    if max_n <= 1:
        return 2
    # quartiles over the active range, like GitHub
    q = n / max_n
    return 1 if q <= 0.25 else 2 if q <= 0.5 else 3 if q <= 0.75 else 4


def render(counts: dict[dt.date, int], included: list[str]) -> str:
    today = dt.date.today()
    # grid ends on the current week's Saturday; 53 columns back
    end_sunday = today - dt.timedelta(days=(today.weekday() + 1) % 7)
    start_sunday = end_sunday - dt.timedelta(weeks=52)
    total = sum(v for d, v in counts.items() if d >= start_sunday)
    max_n = max([v for d, v in counts.items() if d >= start_sunday] or [0])

    width = LEFT + 53 * PITCH + GAP
    height = TOP + 7 * PITCH + 14

    cells, month_labels = [], []
    seen_month = None
    for col in range(53):
        sunday = start_sunday + dt.timedelta(weeks=col)
        if sunday.month != seen_month:
            seen_month = sunday.month
            if col < 51:  # don't crowd the right edge
                month_labels.append(
                    f'<text x="{LEFT + col * PITCH}" y="{TOP - 8}" class="lbl">'
                    f"{sunday.strftime('%b')}</text>"
                )
        for row in range(7):
            day = sunday + dt.timedelta(days=row)
            if day > today:
                continue
            n = counts.get(day, 0)
            b = bucket(n, max_n)
            cells.append(
                f'<rect x="{LEFT + col * PITCH}" y="{TOP + row * PITCH}" '
                f'width="{CELL}" height="{CELL}" rx="2" class="c{b}">'
                f"<title>{day.isoformat()}: {n} commit{'s' if n != 1 else ''}</title></rect>"
            )

    day_labels = [
        f'<text x="{LEFT - 8}" y="{TOP + row * PITCH + CELL - 2}" class="lbl" text-anchor="end">{name}</text>'
        for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    ]
    legend_x = width - 5 * (CELL + 3) - 70
    legend = [
        f'<text x="{legend_x - 34}" y="{height - 8}" class="lbl">Less</text>',
        *(
            f'<rect x="{legend_x + i * (CELL + 3)}" y="{height - 18}" width="{CELL}" height="{CELL}" rx="2" class="c{i}"/>'
            for i in range(5)
        ),
        f'<text x="{legend_x + 5 * (CELL + 3) + 6}" y="{height - 8}" class="lbl">More</text>',
    ]

    style = (
        "text{font:12px -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;fill:#57606a}"
        ".title{font-size:16px;font-weight:600;fill:#1f2328}"
        ".sub{font-size:12px;fill:#57606a}"
        + "".join(f".c{i}{{fill:{c}}}" for i, c in enumerate(LIGHT))
        + "@media(prefers-color-scheme:dark){"
        + "text{fill:#8b949e}.title{fill:#e6edf3}.sub{fill:#8b949e}"
        + "".join(f".c{i}{{fill:{c}}}" for i, c in enumerate(DARK))
        + "}"
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{total} combined contributions in the last year">'
        f"<style>{style}</style>"
        f'<text x="{LEFT}" y="22" class="title">{total:,} contributions in the last year</text>'
        f'<text x="{LEFT}" y="40" class="sub">combined across {len(included)} Verma-Lab repositories</text>'
        + "".join(month_labels)
        + "".join(day_labels)
        + "".join(cells)
        + "".join(legend)
        + "</svg>"
    )


def main() -> int:
    print(f"Collecting commit activity for {len(REPOS)} repos…")
    counts, included = collect()
    if not included:
        print("No repo stats available — not overwriting existing graph.")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(counts, included))
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
