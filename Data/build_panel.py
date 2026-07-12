import pandas as pd
import glob
import os

# this script sits inside the Data folder
data = os.path.dirname(os.path.abspath(__file__))
spf = os.path.join(data, "SPF_raw", "SPF_individual_forecasts")

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
                rows.append([name, year, quarter, col[1], col[0], col[2]])

panel = pd.DataFrame(rows, columns=["round", "year", "quarter", "forecaster", "target", "point"])
panel["point"] = pd.to_numeric(panel["point"], errors="coerce")

panel.to_csv(os.path.join(data, "spf_panel.csv"), index=False)
print(len(panel), "forecasts from", panel["round"].nunique(), "quarters")
