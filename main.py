import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import pandas as pd
import random
import math
from itertools import chain, cycle


class MultiColumnListbox(object):

    def __init__(self):
        self.tree = None

        self.round = 0
        self.picking_team = 0
        self.pick_number = 0

        self.snake_order = self.snake(0, 11)
        self.draft_cycle = [next(self.snake_order) for _ in range(192)]

        self._setup_widgets()

    def _setup_widgets(self):
        container = ttk.Frame()
        container.pack(fill='both', expand=True)

        tk.Button(text="All", command=lambda: self.show_available(available_all), width=5).place(x=0, y=0)
        tk.Button(text="QB", command=lambda: self.show_available(available_qb), width=5).place(x=60, y=0)
        tk.Button(text="RB", command=lambda: self.show_available(available_rb), width=5).place(x=120, y=0)
        tk.Button(text="WR", command=lambda: self.show_available(available_wr), width=5).place(x=180, y=0)
        tk.Button(text="TE", command=lambda: self.show_available(available_te), width=5).place(x=240, y=0)
        tk.Button(text="Flex", command=lambda: self.show_available(available_flex), width=5).place(x=300, y=0)
        tk.Button(text="K", command=lambda: self.show_available(available_k), width=5).place(x=360, y=0)
        tk.Button(text="DST", command=lambda: self.show_available(available_dst), width=5).place(x=420, y=0)

        ttk.Style().configure('my.Treeview', font=(None, 8))
        ttk.Style().configure("Treeview.Heading", font=(None, 8))

        # create and populate the 'available players' tree view
        ttk.Label(text="Available players").place(x=10, y=30)
        self.tree = ttk.Treeview(columns=header, show="headings", height=16, style='my.Treeview')
        self.tree.bind("<Double-1>", lambda x: self.pick_player())
        self.tree.place(x=0, y=50)
        self.show_available(available_all)

        # create 'my team' tree view
        self.my_team_label = ttk.Label(text="My team").place(x=510, y=30)
        self.my_team = ttk.Treeview(columns=header, show="headings", height=16, style='my.Treeview')
        self.my_team.place(x=500, y=50)

        for col in header:
            self.my_team.heading(col, text=col.title(), command=lambda c=col: sort_by(self.my_team, c, 0))
            self.my_team.column(col, width=tkFont.Font().measure(col.title()))
        self.my_team.column('Player', width=120)
        self.my_team.column('Pos', width=60)

        # create and populate all team tree views
        self.team_trees = []
        for i in range(12):
            self.team_trees.append(ttk.Treeview(columns='Player', show="headings", height=16, style='my.Treeview'))
            self.team_trees[i].place(x=0+105*i, y=415)
            self.team_trees[i].column('Player', width=105)

        self.team_trees[0].heading('Player', text=draft_order[0], command=lambda c=col: self.pick_player(0))
        self.team_trees[0].bind("<Double-1>", lambda x: self.undo_player(0))

        self.team_trees[1].heading('Player', text=draft_order[1], command=lambda c=col: self.pick_player(1))
        self.team_trees[1].bind("<Double-1>", lambda x: self.undo_player(1))

        self.team_trees[2].heading('Player', text=draft_order[2], command=lambda c=col: self.pick_player(2))
        self.team_trees[2].bind("<Double-1>", lambda x: self.undo_player(2))

        self.team_trees[3].heading('Player', text=draft_order[3], command=lambda c=col: self.pick_player(3))
        self.team_trees[3].bind("<Double-1>", lambda x: self.undo_player(3))

        self.team_trees[4].heading('Player', text=draft_order[4], command=lambda c=col: self.pick_player(4))
        self.team_trees[4].bind("<Double-1>", lambda x: self.undo_player(4))

        self.team_trees[5].heading('Player', text=draft_order[5], command=lambda c=col: self.pick_player(5))
        self.team_trees[5].bind("<Double-1>", lambda x: self.undo_player(5))

        self.team_trees[6].heading('Player', text=draft_order[6], command=lambda c=col: self.pick_player(6))
        self.team_trees[6].bind("<Double-1>", lambda x: self.undo_player(6))

        self.team_trees[7].heading('Player', text=draft_order[7], command=lambda c=col: self.pick_player(7))
        self.team_trees[7].bind("<Double-1>", lambda x: self.undo_player(7))

        self.team_trees[8].heading('Player', text=draft_order[8], command=lambda c=col: self.pick_player(8))
        self.team_trees[8].bind("<Double-1>", lambda x: self.undo_player(8))

        self.team_trees[9].heading('Player', text=draft_order[9], command=lambda c=col: self.pick_player(9))
        self.team_trees[9].bind("<Double-1>", lambda x: self.undo_player(9))

        self.team_trees[10].heading('Player', text=draft_order[10], command=lambda c=col: self.pick_player(10))
        self.team_trees[10].bind("<Double-1>", lambda x: self.undo_player(10))

        self.team_trees[11].heading('Player', text=draft_order[11], command=lambda c=col: self.pick_player(11))
        self.team_trees[11].bind("<Double-1>", lambda x: self.undo_player(11))

    def snake(self, lower, upper):
        return cycle(chain(range(lower, upper + 1), range(upper, lower - 1, -1)))

    def pick_player(self, team=-1):
        # get selected player
        selected_player = self.tree.item(self.tree.selection())['values']

        # remove selected player from lists of available players
        for player in available_all:
            if player[0] == selected_player[0]:
                available_all.remove(player)
                removed_all.append(player)

        if selected_player[3].startswith('QB'):
            for player in available_qb:
                if player[0] == selected_player[0]:
                    available_qb.remove(player)

        elif selected_player[3].startswith('RB'):
            for player in available_rb:
                if player[0] == selected_player[0]:
                    available_rb.remove(player)
                    available_flex.remove(player)

        elif selected_player[3].startswith('WR'):
            for player in available_wr:
                if player[0] == selected_player[0]:
                    available_wr.remove(player)
                    available_flex.remove(player)

        elif selected_player[3].startswith('TE'):
            for player in available_te:
                if player[0] == selected_player[0]:
                    available_te.remove(player)
                    available_flex.remove(player)

        elif selected_player[3].startswith('K'):
            for player in available_k:
                if player[0] == selected_player[0]:
                    available_k.remove(player)

        elif selected_player[3].startswith('DST'):
            for player in available_dst:
                if player[0] == selected_player[0]:
                    available_dst.remove(player)

        # delete selected player from tree view
        self.tree.delete(self.tree.selection())

        # insert player to team's tree view
        if team == -1:
            self.picking_team = self.draft_cycle[self.pick_number]
            self.pick_number = self.pick_number + 1
        else:
            self.picking_team = team

        self.tag = self.set_row_tag(selected_player, False)
        self.team_trees[self.picking_team].insert('', 'end', values=(selected_player[1],), tag=self.tag)
        self.team_trees[self.picking_team].tag_configure(self.tag, background=self.tag)
        self.team_trees[self.picking_team].tag_configure('gold', background='gold')
        self.team_trees[self.picking_team].tag_configure('salmon', background='salmon')
        self.team_trees[self.picking_team].tag_configure('LightBlue3', background='LightBlue3')
        self.team_trees[self.picking_team].tag_configure('green', background='pale green')
        self.team_trees[self.picking_team].tag_configure('light slate blue', background='light slate blue')
        self.team_trees[self.picking_team].tag_configure('hot pink', background='hot pink')
        self.team_trees[self.picking_team].tag_configure('yellow', background='gold')
        self.team_trees[self.picking_team].tag_configure('red', background='salmon')
        self.team_trees[self.picking_team].tag_configure('blue', background='LightBlue3')
        self.team_trees[self.picking_team].tag_configure('green', background='pale green')
        self.team_trees[self.picking_team].tag_configure('light', background='light slate blue')
        self.team_trees[self.picking_team].tag_configure('pink', background='hot pink')

        if self.picking_team == my_draft_position:
            self.my_team.insert('', 'end', values=selected_player, tag=self.tag)

            if selected_player[3].startswith('RB'):
                my_rb_byes.append(selected_player[4])
                self.show_available(available_all)

            if selected_player[3].startswith('WR'):
                my_wr_byes.append(selected_player[4])
                self.show_available(available_all)

            self.my_team.tag_configure(self.tag, background=self.tag)
            self.my_team.tag_configure('gold', background='gold')
            self.my_team.tag_configure('salmon', background='salmon')
            self.my_team.tag_configure('LightBlue3', background='LightBlue3')
            self.my_team.tag_configure('green', background='pale green')
            self.my_team.tag_configure('light slate blue', background='light slate blue')
            self.my_team.tag_configure('hot pink', background='hot pink')

            self.my_team.tag_configure('yellow', background='gold')
            self.my_team.tag_configure('red', background='salmon')
            self.my_team.tag_configure('blue', background='LightBlue3')
            self.my_team.tag_configure('green', background='pale green')
            self.my_team.tag_configure('light', background='light slate blue')
            self.my_team.tag_configure('pink', background='hot pink')

    # set color/font based on player's position and bye week
    def set_row_tag(self, player, check_byes):
        if player[3].startswith('QB'):
            tag = 'gold'
        elif player[3].startswith('RB'):
            tag = 'salmon'
            if check_byes and (player[4] in my_rb_byes):
                tag = 'salmon_bold'
        elif player[3].startswith('WR'):
            tag = 'LightBlue3'
            if check_byes and player[4] in my_wr_byes:
                tag = 'LightBlue3_bold'
        elif player[3].startswith('TE'):
            tag = 'pale green'
        elif player[3].startswith('K'):
            tag = 'light slate blue'
        elif player[3].startswith('DST'):
            tag = 'hot pink'

        return tag


    # show available players for the selected position(s)
    def show_available(self, pos):
        self.tree.delete(*self.tree.get_children())
        for col in header:
            self.tree.heading(col, text=col.title(), command=lambda c=col: sort_by(self.tree, c, 0))
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        self.tree.column('Player', width=120)
        self.tree.column('Pos', width=60)

        for player in pos:
            self.tree.insert('', 'end', values=player, tags=self.set_row_tag(player, True))
            # adjust column's width if necessary to fit each value
            for i, val in enumerate(player):
                if i > 1:
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(header[i], width=None) < col_w:
                        self.tree.column(header[i], width=col_w)

        self.tree.tag_configure('gold', background='gold')
        self.tree.tag_configure('salmon', background='salmon')
        self.tree.tag_configure('LightBlue3', background='LightBlue3')
        self.tree.tag_configure('green', background='pale green')
        self.tree.tag_configure('light slate blue', background='light slate blue')
        self.tree.tag_configure('hot pink', background='hot pink')

        self.tree.tag_configure('yellow', background='gold')
        self.tree.tag_configure('red', background='salmon')
        self.tree.tag_configure('blue', background='LightBlue3')
        self.tree.tag_configure('green', background='pale green')
        self.tree.tag_configure('light', background='light slate blue')
        self.tree.tag_configure('pink', background='hot pink')

        customfont = tkFont.Font(size=8, weight=tkFont.BOLD, slant=tkFont.ITALIC)
        self.tree.tag_configure('salmon_bold', background='salmon', font=customfont)
        self.tree.tag_configure('LightBlue3_bold', background='LightBlue3', font=customfont)

    def undo_player(self, team):
        selected_player = self.team_trees[team].item(self.team_trees[team].selection())['values']
        self.team_trees[team].delete(self.team_trees[team].selection())

        if team == my_draft_position:
            my_team_list = self.my_team.get_children()
            for row in my_team_list:
                if self.my_team.item(row)['values'][1] == selected_player[0]:
                    if self.my_team.item(row)['values'][3].startswith('RB'):
                        my_rb_byes.remove(self.my_team.item(row)['values'][4])
                    if self.my_team.item(row)['values'][3].startswith('WR'):
                        my_wr_byes.remove(self.my_team.item(row)['values'][4])
                    self.my_team.delete(row)


        # grabbing all values for player we will be re-inserting into the available player tree view
        i = 0
        for player in all:
            if selected_player[0] == player[1]:
                insert_player = all[i]
            else:
                i = i + 1

        self.insert_into_available_all(insert_player)
        self.insert_into_available_pos(insert_player)

    def insert_into_available_all(self, insert_player):
        # find the correct index to insert the player into
        j = 0
        j = 0
        for player in available_all:
            if insert_player[0] < player[0]:
                available_all.insert(j, insert_player)
                self.show_available(available_all)
                return
            else:
                j = j + 1

    def insert_into_available_pos(self, insert_player):
        idx = 0
        if insert_player[3].startswith('QB'):
            for player in available_qb:
                if insert_player[0] < player[0]:
                    available_qb.insert(idx, insert_player)
                    self.show_available(all)
                    return
                else:
                    idx = idx + 1

        if insert_player[3].startswith('RB'):
            for player in available_rb:
                if insert_player[0] < player[0]:
                    available_rb.insert(idx, insert_player)
                    self.show_available(available_all)
                    self.insert_into_available_flex(insert_player)
                    return
                else:
                    idx = idx + 1

        if insert_player[3].startswith('WR'):
            for player in available_wr:
                if insert_player[0] < player[0]:
                    available_wr.insert(idx, insert_player)
                    self.show_available(available_all)
                    self.insert_into_available_flex(insert_player)
                    return
                else:
                    idx = idx + 1

        if insert_player[3].startswith('TE'):
            for player in available_te:
                if insert_player[0] < player[0]:
                    available_te.insert(idx, insert_player)
                    self.show_available(available_te)
                    self.insert_into_available_flex(insert_player)
                    return
                else:
                    idx = idx + 1

        if insert_player[3].startswith('TE'):
            for player in available_qb:
                if insert_player[0] < player[0]:
                    available_qb.insert(idx, insert_player)
                    self.show_available(available_qb)
                    return
                else:
                    idx = idx + 1

    def insert_into_available_flex(self, insert_player):
        idx = 0
        for player in available_flex:
            if insert_player[0] < player[0]:
                available_flex.insert(idx, insert_player)
                self.show_available(available_all)
                return
            else:
                idx = idx + 1


def group_by_position(data):
    for row in data.itertuples():
        all.append(row)
        available_all.append(row)

        if "QB" in row.Pos:
            qb.append(row)
            available_qb.append(row)

        if "RB" in row.Pos:
            rb.append(row)
            flex.append(row)
            available_rb.append(row)
            available_flex.append(row)

        if "WR" in row.Pos:
            wr.append(row)
            flex.append(row)
            available_wr.append(row)
            available_flex.append(row)

        if "TE" in row.Pos:
            te.append(row)
            flex.append(row)
            available_te.append(row)
            available_flex.append(row)

        if "K" in row.Pos:
            k.append(row)
            available_k.append(row)

        if "DST" in row.Pos:
            dst.append(row)
            available_dst.append(row)


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

with open('draftorder.txt') as f:
    draft_order = f.readlines()
draft_order = [x.strip() for x in draft_order]
#random.shuffle(draft_order)

my_draft_position = draft_order.index("Kyle")

header = ['Rank', 'Player', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP']

rankings = pd.read_csv('rankings.csv',
                       index_col=0,
                       usecols=['Rank', 'Overall', 'Team', 'Pos', 'Bye', 'Best', 'Worst', 'Avg', 'ADP', 'vs. ADP'])

available_all, available_qb, available_rb, available_wr, available_te, available_flex,\
    available_k, available_dst = ([] for _ in range(8))

all, qb, rb, wr, te, flex, k, dst = ([] for _ in range(8))

my_rb_byes = []
my_wr_byes = []

removed_all = []

group_by_position(rankings)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pydraft")
    root.geometry("1280x860")
    listbox = MultiColumnListbox()
    root.mainloop()
