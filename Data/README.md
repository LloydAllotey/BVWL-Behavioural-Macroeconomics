# SPF panel builder

`build_panel.py` reads the quarterly ECB SPF individual-forecast CSVs and stacks the
**1-year-ahead HICP point forecasts** into one file, `spf_panel.csv`.

Run:

```powershell
uv run python build_panel.py
```

It finds `SPF_raw/SPF_individual_forecasts/*.csv` relative to itself and writes
`spf_panel.csv` in the same `Data` folder.

**How the forecast is picked:** each survey round has one true 1-year-ahead
target and its month depends on the quarter (Q1→Dec, Q2→Mar, Q3→Jun, Q4→Sep, always
12 months out). The script builds that label per round and keeps those rows from the
HICP block only.

**Output columns:** `round, year, quarter, forecaster, target, point`
(one row per forecaster per quarter; blank `point` = respondent gave a distribution
but no point — kept as empty). Blanks dropped not imputed.

**Checked against the live repo (read-only):** 6,165 forecasts across all 110 rounds
(1999Q1–2026Q2), 5,355 with a usable point, 39–72 forecasters per round.




