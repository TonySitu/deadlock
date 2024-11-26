import tkinter as tk
from tkinter import ttk


def get_sample_data1() -> list:
    return ['hi', 'this', 'is', 'a', 'test', 'for', 'some', 'data']


def get_sample_data2() -> list:
    return ['this', 'is', 'the', 'second', 'set', 'of', 'sample', 'data']


def select_item(_, table):
    print(table.selection())
    for i in table.selection():
        print(table.item(i))


class View:
    window = None
    people_tree = None

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('1000x800')
        self.window.title('Deadlock Tracker')

        self.people_tree = ttk.Treeview(self.window, columns=('some', 'data'), show='headings', selectmode='browse')
        self.people_tree.pack()
        self.people_tree.heading('some', text='first_set')
        self.people_tree.heading('data', text='second_set')

        for data1, data2 in zip(get_sample_data1(), get_sample_data2()):
            self.people_tree.insert(parent='', index=tk.END, values=(data1, data2))

        add_button = ttk.Button(self.window, text="Add Children", command=self.add_children)
        add_button.pack()

        self.people_tree.bind('<<TreeviewSelect>>', lambda event: select_item(event, self.people_tree))

    def add_children(self):
        selected_items = self.people_tree.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        self.people_tree.insert(parent=selected_item, index=tk.END, values=("Detail A1", "Info A1"))
        self.people_tree.item(selected_item, open=True)

    def run(self):
        self.window.mainloop()


def main():
    view = View()
    view.run()


if __name__ == "__main__":
    main()
