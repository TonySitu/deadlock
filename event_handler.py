import tkinter as tk
from UI import View
import sqlite3


def handle_exit(view):
    view.get_window().quit()


def handle_entry_click(textfield_string: tk.StringVar, textfield: tk.Entry):
    if textfield_string.get() == View.DEFAULT_INPUT_TEXT:
        textfield_string.set('')
        textfield.config(fg="black")
        print('focus in')


def handle_focus_out(textfield_string: tk.StringVar, textfield: tk.Entry):
    if textfield_string.get() == '':
        textfield_string.set(View.DEFAULT_INPUT_TEXT)
        textfield.config(fg="gray")
        print('focus out')


def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)


def query_all_players() -> list:
    DATABASE = 'deadlock.db'
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    player_list = []

    cursor.execute("""
        SELECT * FROM PLAYER;
    """)

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    print(column_names)

    for row in rows:
        player_list.append(dict(zip(column_names, row)))

    for player in player_list:
        print(player)
    connection.close()

    return player_list


def query_specific_player(player_name: str) -> list:
    DATABASE = 'deadlock.db'
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    player_list = []

    cursor.execute("""
        SELECT player_id, player_name
        FROM player
        WHERE player_name = ?
    """, (player_name,))

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    for row in rows:
        player_list.append(dict(zip(column_names, row)))

    for player in player_list:
        print(player)
    connection.close()

    return player_list


def handle_button_search(view: View):
    player = view.get_textfield_string().get()

    if player == '' or player == View.DEFAULT_INPUT_TEXT:
        player_list = query_all_players()
    else:
        player_list = query_specific_player(player)

    player_tree = view.get_player_tree()
    clear_treeview(player_tree)

    for player in player_list:
        player_tree.insert(parent='', index=tk.END, iid=player['player_id'], values=(player['player_name'],))

    print('button searching')


def handle_player_search(view: View):
    player_tree = view.get_player_tree()
    current_player = player_tree.selection()

    # handle same player selection
    if current_player == view.get_previous_player_selection():
        player_tree.selection_set('')
        view.set_previous_player_selection(None)
        print('player unselected')
        return

    view.set_previous_player_selection(current_player)
    print('player searching')


def handle_match_search(view):
    match_tree = view.get_match_tree()
    current_player = match_tree.selection()

    # handle same match selection
    if current_player == view.get_previous_match_selection():
        match_tree.selection_set('')
        view.set_previous_match_selection(None)
        print('match unselected')
        return

    view.set_previous_match_selection(current_player)
    print('match search')


def handle_tab_change(view: View):
    selected_tab = view.get_notebook().select()


def handle_second_player_search(view: View):
    player_tree = view.get_second_player_tree()
    current_player = player_tree.selection()

    # handle same player selection
    if current_player == view.get_second_previous_player_selection():
        player_tree.selection_set('')
        view.set_second_previous_player_selection(None)
        print('second player unselected')
        return

    view.set_second_previous_player_selection(current_player)
    print('second player searching')


def handle_hero_search(view: View):
    hero_tree = view.get_hero_tree()
    current_hero = hero_tree.selection()

    # handle same player selection
    if current_hero == view.get_previous_player_selection():
        hero_tree.selection_set('')
        view.set_previous_player_selection(None)
        print('hero unselected')
        return

    view.set_previous_player_selection(current_hero)
    print('hero searching')


def select_item(_, table):
    print(table.selection())
    for i in table.selection():
        print(table.item(i))
