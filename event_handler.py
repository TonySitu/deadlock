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

    connection.close()

    return player_list


def query_specific_player(player_name: str) -> list[dict]:
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

    connection.close()

    return player_list


def query_player_matches(player_id: str) -> list[dict]:
    DATABASE = 'deadlock.db'
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    match_list = []

    cursor.execute("""
            SELECT 
                match_stats.player_id, 
                match_stats.match_id, 
                match_stats.hero_id, 
                match_stats.match_kda, 
                hero.hero_name
            FROM match_stats
            JOIN hero ON match_stats.hero_id = hero.hero_id
            WHERE player_id = ?
       """, (player_id,))

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    for row in rows:
        match_list.append(dict(zip(column_names, row)))
    connection.close()

    return match_list


def query_match(player_id: str, hero_id: str, match_id: str) -> list[dict]:
    DATABASE = 'deadlock.db'
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    match_list = []

    cursor.execute("""
            SELECT 
                match_stats.match_mmr, 
                match_stats.match_kills, 
                match_stats.match_deaths, 
                match_stats.match_assists, 
                match_stats.match_kda,
                match_stats.match_souls_per_minute,
                match_stats.win_loss,
                hero.hero_name
            FROM match_stats
            JOIN hero ON match_stats.hero_id = hero.hero_id
            WHERE player_id = ? AND match_stats.hero_id = ? AND match_id = ?;
       """, (player_id, hero_id, match_id,))

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    for row in rows:
        match_list.append(dict(zip(column_names, row)))
    connection.close()

    return match_list


def query_hero_list(player_id: str) -> list[dict]:
    DATABASE = 'deadlock.db'
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    hero_list = []

    cursor.execute("""
                SELECT 
                    hero.hero_name, hero.hero_id
                FROM hero
                JOIN hero_stats ON hero.hero_id = hero_stats.hero_id
                WHERE player_id = ?
           """, (player_id,))

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    for row in rows:
        hero_list.append(dict(zip(column_names, row)))
    connection.close()

    return hero_list


def handle_button_search(view: View):
    player = view.get_textfield_string().get()

    if player == '' or player == View.DEFAULT_INPUT_TEXT:
        player_list = query_all_players()
    else:
        player_list = query_specific_player(player)

    player_tree = view.get_player_tree()
    clear_treeview(player_tree)
    clear_treeview(view.get_match_tree())
    clear_treeview(view.get_match_stats_tree())

    for player in player_list:
        player_tree.insert(parent='', index=tk.END, iid=player['player_id'], values=(player['player_name'],))

    print('button searching')


def handle_second_button_search(view: View):
    player = view.get_second_textfield_string().get()

    if player == '' or player == View.DEFAULT_INPUT_TEXT:
        player_list = query_all_players()
    else:
        player_list = query_specific_player(player)

    player_tree = view.get_second_player_tree()
    clear_treeview(player_tree)
    clear_treeview(view.get_hero_tree())
    clear_treeview(view.get_hero_stats_tree())

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

    player_id = player_tree.focus()
    match_list = query_player_matches(player_id)
    match_tree = view.get_match_tree()
    clear_treeview(match_tree)
    clear_treeview(view.get_match_stats_tree())
    for match in match_list:
        iid = f"{match['hero_id']}_{match['match_id']}"
        match_tree.insert(parent='', index=tk.END,
                          iid=iid, values=(match['hero_name'], match['match_kda'],))

    print('player searching')


def handle_match_search(view):
    match_tree = view.get_match_tree()
    current_match = match_tree.selection()

    # handle same match selection
    if current_match == view.get_previous_match_selection():
        match_tree.selection_set('')
        view.set_previous_match_selection(None)
        print('match unselected')
        return

    view.set_previous_match_selection(current_match)

    iid = match_tree.focus()
    if iid:
        player_id = view.get_player_tree().focus()
        hero_id, match_id = map(int, iid.split('_'))
        match_list = query_match(player_id, hero_id, match_id)
        match_stats_tree = view.get_match_stats_tree()
        clear_treeview(match_stats_tree)
        for match in match_list:
            match_stats_tree.insert(parent='', index=tk.END,
                                    values=(match['hero_name'],
                                            match['match_mmr'],
                                            match['match_kills'],
                                            match['match_deaths'],
                                            match['match_assists'],
                                            match['match_kda'],
                                            match['match_souls_per_minute'],
                                            match['win_loss'],))

        print('match search')


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

    player_id = player_tree.focus()
    hero_list = query_hero_list(player_id)
    hero_tree = view.get_hero_tree()
    clear_treeview(hero_tree)
    for hero in hero_list:
        iid = hero['hero_id']
        hero_tree.insert(parent='', index=tk.END,
                         iid=iid, values=(hero['hero_name'],))
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
