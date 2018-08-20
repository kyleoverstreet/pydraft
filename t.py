'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import pandas as pd
import math

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        s = "hello"
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in header:
            self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for player in all_pos:
            self.tree.insert('', 'end', values=player)
            # adjust column's width if necessary to fit each value
            for i, val in enumerate(player):
                if i > 1:
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(header[i], width=None) < col_w:
                        self.tree.column(header[i], width=col_w)

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    if col == 'Rank' or col == 'Bye' or col == 'Best' or col == 'Worst' \
        or col == 'Avg' or col == 'ADP' or col == 'vs. ADP':
        data = change_numeric(data)
        #print(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


def change_numeric(data):
    #numbers = [x[0] for x in data]

    for i in range(len(data)):
        data[i] = (float(data[i][0]), data[i][1])

        if math.isnan(data[i][0]):
            data[i] = (999, data[i][1])

    return data


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# the test data ...

header = ['Rank', 'Player', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP']
rankings = pd.read_csv('rankings.csv',
                       index_col=0,
                       usecols=['Rank', 'Overall', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP'])
all_pos, qb, rb, wr, te, k, dst = [], [], [], [], [], [], []

for row in rankings.itertuples():
    all_pos.append(row)

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


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pydraft")
    root.geometry("800x800")
    listbox = MultiColumnListbox()
    root.mainloop()
