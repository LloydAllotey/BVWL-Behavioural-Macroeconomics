import pandas as pd
import glob
import os
import sys

# this script lives in data/src/, so one level up is the data folder
data = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spf = os.path.join(data, "raw", "spf", "SPF_individual_forecasts")
out_path = os.path.join(data, "processed", "spf_panel.xlsx")

# don't build a second panel if one is already there
if os.path.exists(out_path):
    print("spf_panel.xlsx already exists in data/processed, delete it first to rebuild")
    sys.exit()

# the 1-year-ahead forecast falls on a different month depending on the survey quarter
month = {1: "Dec", 2: "Mar", 3: "Jun", 4: "Sep"}

rows = []
for path in sorted(glob.glob(os.path.join(spf, "*.csv"))):
    name = os.path.basename(path).replace(".csv", "")      # e.g. 2014Q1
    year = int(name[:4])
    quarter = int(name[5])

    # the target label I want for this round
    if quarter == 1:
        want = str(year) + "Dec"
    else:
        want = str(year + 1) + month[quarter]

    # each file has several blocks, I only want the HICP one (the first block)
    lines = open(path, encoding="utf-8-sig").read().splitlines()
    in_hicp = False
    for line in lines:
        if line.startswith("TARGET_PERIOD"):
            in_hicp = True
            continue
        if in_hicp:
            if line.strip() == "":
                continue
            if not line[:1].isdigit():
                break                                       # start of the next block
            col = line.split(",")
            if col[0] == want:
                rows.append([year, quarter, name, col[1], col[0], col[2]])

panel = pd.DataFrame(rows, columns=["year", "quarter", "round", "forecaster", "target", "point"])
panel["point"] = pd.to_numeric(panel["point"], errors="coerce")
panel["forecaster"] = pd.to_numeric(panel["forecaster"], errors="coerce")

# numeric time axis for scatter plots: 1999Q1 -> 1999.00, 1999Q2 -> 1999.25, ...
panel["round - helper"] = panel["year"] + (panel["quarter"] - 1) / 4

panel = panel[["year", "quarter", "round", "round - helper", "forecaster", "target", "point"]]
panel = panel.rename(columns={"point": "Expected Inflation - Median obs. per round"})

os.makedirs(os.path.dirname(out_path), exist_ok=True)
panel.to_excel(out_path, sheet_name="spf_panel", index=False)
print(len(panel), "forecasts from", panel["round"].nunique(), "quarters")