import tkinter
from functions.operations import select_all_text


def add_placeholder(entry_field: tkinter.Entry, placeholder_text: str):
    def focus_in(event):
        if entry_field.get() == placeholder_text:
            entry_field.delete(0, tkinter.END)
            entry_field.config(fg='black')
        select_all_text(event)

    def focus_out(event):
        if not entry_field.get():
            entry_field.config(fg='gray')
            entry_field.insert(0, placeholder_text)

    entry_field.config(fg='gray')
    entry_field.insert(0, placeholder_text)

    entry_field.bind('<FocusIn>', focus_in)
    entry_field.bind('<FocusOut>', focus_out)
