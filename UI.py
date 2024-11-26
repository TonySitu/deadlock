import tkinter as tk
from tkinter import ttk


def get_sample_data1() -> list:
    return ['hi', 'this', 'is', 'a', 'test', 'for', 'some', 'data']  # todo remove later


def get_sample_data2() -> list:
    return ['this', 'is', 'the', 'second', 'set', 'of', 'sample', 'data']  # todo remove later


class View:  # todo create second tab that searches a player's champion stats opposed to match stats
    DEFAULT_INPUT_TEXT = 'Enter nothing for all players or search for a specific player name'
    controller = None
    window = None
    player_tree = None
    match_tree = None
    match_stats_tree = None
    top_frame = None
    middle_frame = None
    bottom_frame = None
    input_text = None
    textfield_string = None
    input_button = None
    menu = None

    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title('Deadlock Tracker')

        # init screen size
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        print(f'x:{screen_width} y:{screen_height}')
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.state('zoomed')
        self.window.bind('<Escape>', lambda event: self.window.quit())

        # init menu
        self.menu = tk.Menu(self.menu, tearoff=False)
        self.window.configure(menu=self.menu)
        add_menu = tk.Menu(self.menu, tearoff=False)
        add_menu.add_command(label='Add', command=lambda: None)  # todo add method to add matches
        self.menu.add_cascade(label='Add Match', menu=add_menu)

        # init top frame
        self.top_frame = ttk.Frame(self.window, width=screen_width * .32, height=screen_height * .1)
        self.top_frame.pack_propagate(False)

        self.textfield_string = tk.StringVar(value=self.DEFAULT_INPUT_TEXT)
        self.input_text = tk.Entry(self.top_frame, width=60, fg='gray', textvariable=self.textfield_string)
        self.input_text.pack(side=tk.LEFT)
        self.input_text.bind("<FocusIn>",
                             lambda event: self.controller.on_entry_click(textfield_string=self.textfield_string,
                                                                          textfield=self.input_text))
        self.input_text.bind("<FocusOut>",
                             lambda event: self.controller.on_focus_out(textfield_string=self.textfield_string,
                                                                        textfield=self.input_text))

        self.input_button = ttk.Button(self.top_frame, text='Search Player')
        self.input_button.pack(side=tk.RIGHT)
        self.top_frame.pack()

        # init middle frame
        self.middle_frame = ttk.Frame(self.window, width=screen_width * .8, height=screen_height * .3, borderwidth=10,
                                      relief=tk.RIDGE)
        self.middle_frame.pack_propagate(False)
        self.middle_frame.pack()

        # player tree config
        self.player_tree = ttk.Treeview(self.middle_frame, columns=('name',), show='headings', selectmode='browse')
        self.player_tree.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.player_tree.heading('name', text='Player Name')
        for data in get_sample_data1():
            self.player_tree.insert(parent='', index=tk.END, values=(data,))

        self.player_tree.bind('<<TreeviewSelect>>', lambda event: self.controller.on_player_search())  # todo update

        # match tree config
        self.match_tree = ttk.Treeview(self.middle_frame, columns=('more', 'data'), show='headings',
                                       selectmode='browse')

        self.match_tree.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.match_tree.heading('more', text='first set')
        self.match_tree.heading('data', text='second set')
        for data1, data2 in zip(get_sample_data1(), get_sample_data2()):
            self.match_tree.insert(parent='', index=tk.END, values=(data1, data2))

        self.match_tree.bind('<<TreeviewSelect>>', lambda event: self.controller.on_match_search())  # todo update

        # bottom frame config
        self.bottom_frame = ttk.Frame(self.window, width=screen_width * .8, height=screen_height * .5, borderwidth=10,
                                      relief=tk.RIDGE)
        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack()

        self.match_stats_tree = ttk.Treeview(self.bottom_frame,
                                             columns=('probably', 'going', 'to', 'be', 'lots', 'of', 'columns'),
                                             show='headings', selectmode='none')
        self.match_stats_tree.heading('probably', text='probably')
        self.match_stats_tree.heading('going', text='going')
        self.match_stats_tree.heading('to', text='to')
        self.match_stats_tree.heading('be', text='be')
        self.match_stats_tree.heading('lots', text='lots')
        self.match_stats_tree.heading('of', text='of')
        self.match_stats_tree.heading('columns', text='columns')
        self.autofit_treeview_columns(self.match_stats_tree)
        self.match_stats_tree.pack(fill='both')

    def get_match_tree(self) -> ttk.Treeview:
        return self.match_tree

    @staticmethod
    def autofit_treeview_columns(treeview: ttk.Treeview):
        for col in treeview["columns"]:
            max_length = len(col)  # Start with the header length
            for item in treeview.get_children():
                cell_value = str(treeview.set(item, col))  # Get cell value as string
                max_length = max(max_length, len(cell_value))
            # Add some padding for aesthetics
            treeview.column(col, width=(max_length + 2) * 7)

    def run(self):
        self.window.mainloop()

