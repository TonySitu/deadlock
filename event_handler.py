import tkinter as tk
from UI import View


def handle_exit(view: View):
    print(view.get_window())
    view.get_window().quit()


def handle_entry_click(textfield_string: tk.StringVar, textfield: tk.Entry):
    if textfield_string.get() == View.DEFAULT_INPUT_TEXT:
        textfield_string.set('')
        textfield.config(fg="black")
        print('focus in')


def handle_focus_out(textfield_string: tk.StringVar, textfield: tk.Entry):
    if textfield_string.get() == "":
        textfield_string.set(View.DEFAULT_INPUT_TEXT)
        textfield.config(fg="gray")
        print('focus out')


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


def handle_tab_change(view):
    selected_tab = view.get_notebook().select()
    player_tree = view.get_player_tree()
    player_tree.pack_forget()

    player_tree.master = selected_tab
    player_tree.pack(fill=tk.BOTH, expand=True)


def select_item(_, table):
    print(table.selection())
    for i in table.selection():
        print(table.item(i))
