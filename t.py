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
        #self._build_available_tree()

        self.my_picked_counter = 0
        self.my_picked_players = []
        for i in range(6):
            self.my_picked_players.append(tk.StringVar())
            self.my_picked_players[i].set("")


        self._setup_widgets()

    def _setup_widgets(self):
        container = ttk.Frame()
        container.pack(fill='both', expand=True)

        #buttons
        self.all_button = ttk.Button(text="All", command=lambda: self._available_players(all_pos))
        self.all_button.place(x=0, y=0)

        self.qb_button = ttk.Button(text="QB", command=lambda: self._available_players(qb))
        self.qb_button.place(x=100, y=0)

        self.rb_button = ttk.Button(text="RB", command=lambda: self._available_players(rb))
        self.rb_button.place(x=200, y=0)

        self.wr_button = ttk.Button(text="WR", command=lambda: self._available_players(wr))
        self.wr_button.place(x=300, y=0)

        self.te_button = ttk.Button(text="TE", command=lambda: self._available_players(te))
        self.te_button.place(x=400, y=0)

        self.k_button = ttk.Button(text="K", command=lambda: self._available_players(k))
        self.k_button.place(x=500, y=0)

        self.dst_button = ttk.Button(text="DST", command=lambda: self._available_players(dst))
        self.dst_button.place(x=600, y=0)

        self.pick_button = ttk.Button(text="Pick", command=lambda: self._show_selection())
        self.pick_button.place(x=600, y=600)

        # labels
        self.available_label = ttk.Label(text="Available players")
        self.available_label.place(x=10, y=80)

        self.my_team = ttk.Label(text="My team")
        self.my_team.place(x=10, y=350)

        self.labels = []
        for i in range(6):
            self.labels.append(ttk.Label(textvariable=self.my_picked_players[i]))
            self.labels[i].place(x=10, y=370+20*i)


        #self.chosen_label = ttk.Label(textvariable=self.selected).place(x=10, y=700)



        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.place(x=0, y=100)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self._available_players(all_pos)

    def _show_selection(self):
        selected_player = self.tree.item(self.tree.selection())['values'][1]
        self.my_picked_players[self.my_picked_counter].set(selected_player)
        self.tree.delete(self.tree.selection())
        self.my_picked_counter = self.my_picked_counter + 1

    def _available_players(self, pos):
        self.tree.delete(*self.tree.get_children())
        for col in header:
            self.tree.heading(col, text=col.title(), command=lambda c=col: sort_by(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        self.tree.column('Player', width=120)
        self.tree.column('Pos', width=60)

        for player in pos:
            self.tree.insert('', 'end', values=player)
            # adjust column's width if necessary to fit each value
            for i, val in enumerate(player):
                if i > 1:
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(header[i], width=None) < col_w:
                        self.tree.column(header[i], width=col_w)


def group_by_position(data):
    for row in data.itertuples():
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


def sort_by(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # if the data to be sorted is numeric change to float
    if col in ['Rank', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP']:
        data = change_numeric(data)

    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)

    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sort_by(tree, col, int(not descending)))


def change_numeric(data):
    for i in range(len(data)):
        data[i] = (float(data[i][0]), data[i][1])

        if math.isnan(data[i][0]):
            data[i] = (999, data[i][1])

    return data


header = ['Rank', 'Player', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP']
rankings = pd.read_csv('rankings.csv',
                       index_col=0,
                       usecols=['Rank', 'Overall', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP'])
all_pos, qb, rb, wr, te, k, dst = ([] for _ in range(7))

group_by_position(rankings)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pydraft")
    root.geometry("1200x800")
    listbox = MultiColumnListbox()
    root.mainloop()
