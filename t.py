import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import pandas as pd
import math


class MultiColumnListbox(object):

    def __init__(self):
        self.tree = None
        #self._build_available_tree()

        self.current_pick = 0
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
        self.all_button = tk.Button(text="All", command=lambda: self._available_players(all_pos), width=5)
        self.all_button.place(x=0, y=0)

        self.qb_button = tk.Button(text="QB", command=lambda: self._available_players(qb), width=5)
        self.qb_button.place(x=60, y=0)

        self.rb_button = tk.Button(text="RB", command=lambda: self._available_players(rb), width=5)
        self.rb_button.place(x=120, y=0)

        self.wr_button = tk.Button(text="WR", command=lambda: self._available_players(wr), width=5)
        self.wr_button.place(x=180, y=0)

        self.te_button = tk.Button(text="TE", command=lambda: self._available_players(te), width=5)
        self.te_button.place(x=240, y=0)

        self.te_button = tk.Button(text="Flex", command=lambda: self._available_players(flex), width=5)
        self.te_button.place(x=300, y=0)

        self.k_button = tk.Button(text="K", command=lambda: self._available_players(k), width=5)
        self.k_button.place(x=360, y=0)

        self.dst_button = tk.Button(text="DST", command=lambda: self._available_players(dst), width=5)
        self.dst_button.place(x=420, y=0)

        self.pick_button = ttk.Button(text="Picked", command=lambda: self._pick_player())
        self.pick_button.place(x=400, y=300)

        self.labels = []
        for i in range(6):
            self.labels.append(ttk.Label(textvariable=self.my_picked_players[i]))
            self.labels[i].place(x=10, y=320+20*i)

        # create and populate the 'available players' tree view
        self.available_label = ttk.Label(text="Available players").place(x=10, y=30)
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.place(x=0, y=50)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self._available_players(all_pos)

        # create and populate team tree views
        self.team_trees = []

        for i in range(12):
            self.team_trees.append(ttk.Treeview(columns='Player', show="headings", height=16))
            self.team_trees[i].place(x=0+120*i, y=350)
            vsb.grid(column=1, row=0, sticky='ns', in_=container)
            hsb.grid(column=0, row=1, sticky='ew', in_=container)
            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)
            self.team_trees[i].heading('Player', text='Team ' + str(i+1))
            self.team_trees[i].column('Player', width=120)


    def _pick_player(self):
        # get selected player
        selected_player = self.tree.item(self.tree.selection())['values']

        # remove selected player from appropriate lists
        del all_pos[selected_player[0] - 1]

        if selected_player[3].startswith('QB'):
            for player in qb:
                if player[0] == selected_player[0]:
                    qb.remove(player)
        elif selected_player[3].startswith('RB'):
            for player in rb:
                if player[0] == selected_player[0]:
                    rb.remove(player)
        elif selected_player[3].startswith('WR'):
            for player in wr:
                if player[0] == selected_player[0]:
                    wr.remove(player)
        elif selected_player[3].startswith('TE'):
            for player in te:
                if player[0] == selected_player[0]:
                    te.remove(player)
        elif selected_player[3].startswith('K'):
            for player in k:
                if player[0] == selected_player[0]:
                    k.remove(player)
        elif selected_player[3].startswith('DST'):
            for player in dst:
                if player[0] == selected_player[0]:
                    dst.remove(player)

        # delete selected player from tree view
        self.tree.delete(self.tree.selection())

        # insert player to team's tree view
        self.picking_team = self.current_pick % 12
        self.tag = self.set_color_tag(player)
        self.team_trees[self.picking_team].insert('', 'end', values=(selected_player[1],), tag=self.tag)
        self.team_trees[self.picking_team].tag_configure(self.tag, background=self.tag)

        self.team_trees[self.picking_team].tag_configure('yellow', background='gold')
        self.team_trees[self.picking_team].tag_configure('red', background='salmon')
        self.team_trees[self.picking_team].tag_configure('blue', background='LightBlue3')
        self.team_trees[self.picking_team].tag_configure('green', background='pale green')
        self.team_trees[self.picking_team].tag_configure('purple', background='light slate blue')
        self.team_trees[self.picking_team].tag_configure('pink', background='hot pink')
        self.current_pick = self.current_pick + 1

    # set color based on player's position
    def set_color_tag(self, player):
        if player[3].startswith('QB'):
            tag = 'gold'
        elif player[3].startswith('RB'):
            tag = 'salmon'
        elif player[3].startswith('WR'):
            tag = 'LightBlue3'
        elif player[3].startswith('TE'):
            tag = 'pale green'
        elif player[3].startswith('K'):
            tag = 'light slate blue'
        elif player[3].startswith('DST'):
            tag = 'hot pink'
        return tag


    # show available players for the selected position(s)
    def _available_players(self, pos):
        self.tree.delete(*self.tree.get_children())
        for col in header:
            self.tree.heading(col, text=col.title(), command=lambda c=col: sort_by(self.tree, c, 0))
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        self.tree.column('Player', width=120)
        self.tree.column('Pos', width=60)

        for player in pos:
            self.tree.insert('', 'end', values=player, tags=self.set_color_tag(player))

            # adjust column's width if necessary to fit each value
            for i, val in enumerate(player):
                if i > 1:
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(header[i], width=None) < col_w:
                        self.tree.column(header[i], width=col_w)

        self.tree.tag_configure('gold', background='gold')
        self.tree.tag_configure('salmon', background='salmon')
        self.tree.tag_configure('LightBlue3', background='LightBlue3')
        self.tree.tag_configure('pale green', background='pale green')
        self.tree.tag_configure('light slate blue', background='light slate blue')
        self.tree.tag_configure('hot pink', background='hot pink')


def group_by_position(data):
    for row in data.itertuples():
        all_pos.append(row)

        if "QB" in row.Pos:
            qb.append(row)

        if "RB" in row.Pos:
            rb.append(row)
            flex.append(row)

        if "WR" in row.Pos:
            wr.append(row)
            flex.append(row)

        if "TE" in row.Pos:
            te.append(row)
            flex.append(row)

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
all_pos, qb, rb, wr, te, flex, k, dst = ([] for _ in range(8))

group_by_position(rankings)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pydraft")
    root.geometry("1400x900")
    listbox = MultiColumnListbox()
    root.mainloop()
