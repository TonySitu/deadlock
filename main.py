import tkinter as tk
from tkinter import ttk


def get_data():
    pass


def get_sample_data1() -> list:
    return ['hi', 'this', 'is', 'a', 'test', 'for', 'some', 'data']


def get_sample_data2() -> list:
    return ['this', 'is', 'the', 'second', 'set', 'of', 'sample', 'data']


def main():
    window = tk.Tk()
    window.geometry('1000x800')
    window.title('Deadlock Tracker')

    table = ttk.Treeview(window, columns=('some', 'data'), show='headings')
    table.pack()
    table.heading('some', text='first_set')
    table.heading('data', text='second_set')

    for data1, data2 in zip(get_sample_data1(), get_sample_data2()):
        table.insert(parent='', index=len(get_sample_data1()), values=(data1, data2))

    window.mainloop()


if __name__ == "__main__":
    main()
