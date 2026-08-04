# Org profile scripts

## Combined contribution graph

`generate_contribution_graph.py` builds the GitHub-style heatmap shown on the
org profile page (`profile/assets/contribution-graph.svg`). GitHub has no
org-level contribution graph, so this script makes one:

1. For every repo listed in `REPOS` (top of the script), it calls the GitHub
   API `repos/Verma-Lab/<repo>/stats/commit_activity` — 52 weeks of per-day
   commit counts on the default branch.
2. Sums the counts day-by-day across all repos.
3. Renders a 53x7 green-square SVG heatmap — month/weekday labels, Less→More
   legend, per-day hover tooltips, automatic light/dark theme
   (`prefers-color-scheme`), plus the "N contributions in the last year" title.

### How to refresh it (run monthly-ish, or whenever)

```bash
# prerequisite: gh CLI logged in (gh auth status) — the logged-in token is
# what lets PRIVATE repos (e.g. CIRCA) be counted; repos the token can't
# read are skipped automatically.
cd <this repo>
python3 scripts/generate_contribution_graph.py
git add profile/assets/contribution-graph.svg
git commit -m "refresh contribution graph"
git push
```

Notes:

- The stats endpoint returns `202`/`{}` while GitHub computes a repo's stats;
  the script retries a few times per repo (first run after a long gap can take
  a minute or two — rerun if repos print "stats never became ready").
- Only the **last 52 weeks** are counted (that's all this API exposes) and only
  commits on each repo's **default branch** — a repo whose work is older than a
  year contributes 0 even though it has history.
- Adding/removing repos = edit the `REPOS` list at the top of the script.
- Layout knobs are constants at the top (`CELL`, `GAP`, `TOP` for the padding
  between the title block and the grid, `LEFT` for weekday-label room).

## Repo cards

`profile/assets/card-circa.svg` and `card-carebench.svg` are hand-written
cards (same light/dark adaptive styling) used where GitHub's automatic
opengraph card images can't work: CIRCA is private (GitHub never renders
cards for private repos) and brand-new repos serve a generic fallback banner
until GitHub generates their card. Public, established repos use
`https://opengraph.githubassets.com/<any-cache-key>/Verma-Lab/<repo>` directly.
