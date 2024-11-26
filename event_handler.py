import tkinter as tk
from UI import View


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


def handle_player_search():
    print('player searching')


def handle_match_search():
    print('match search')


def select_item(_, table):
    print(table.selection())
    for i in table.selection():
        print(table.item(i))

