import pandas as pd
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

data = pd.read_csv('rankings.csv', usecols=['Rank', 'Overall', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP'])

all, qb, rb, wr, te, k, dst = [], [], [], [], [], [], []

for row in data.itertuples():
    all.append(row)

    if "QB" in row.Pos:
        qb.append(row)

    if "RB" in row.Pos:
        rb.append(row)

    if "WR" in row.Pos:
        wr.append(row)

    if "TE" in row.Pos:
        te.append(row)

    if "K" in row.Pos:
        k.append(row)

    if "DST" in row.Pos:
        dst.append(row)

print(qb)