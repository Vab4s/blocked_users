import tkinter
from tkinter import ttk
import os
import configparser

from functions.add_user import add_user_info_to_bd
from functions.check_user import check_user
from functions.placeholder import add_placeholder
from functions.operations import open_path, true_path

from project.user_list_settings import Settings


class UsersList:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.settings = None
        self.password_path = None
        self.users_path = None
        self.json_path = None
        self.adming_path = None
        self.load_settings()

        self.main_frame = None
        self.main_menu = None
        self.menu = None
        self.menu_settings = None
        self.input_frame = None
        self.radio_frame = None
        self.output_frame = None
        self.dates_label = None
        self.dates_text = None
        self.add_symbol = None
        self.comment_label = None
        self.comment_entry = None
        self.plus = None
        self.minus = None
        self.email_label = None
        self.email_entry = None
        self.email_check_button = None
        self.email_add_button = None

        self.root = tkinter.Tk()
        self.screen_width = int(self.root.winfo_screenwidth() / 3)
        self.screen_height = int(self.root.winfo_screenheight() / 3)
        self.root_configure()
        self.elements_configure()
        self.elements_creation()

        self.root.mainloop()

    def create_settings(self):
        self.settings = Settings(self.root, self.menu, self.screen_width, self.screen_height)

    def load_settings(self):
        if os.path.exists(true_path('project', 'settings.ini')):
            self.config.read(true_path('project', 'settings.ini'))
            self.password_path = self.config.get('Settings', 'password_path', fallback=None)
            self.users_path = self.config.get('Settings', 'users_path', fallback=None)
            self.json_path = self.config.get('Settings', 'json_path', fallback=None)
            self.adming_path = self.config.get('Settings', 'adming_path', fallback=None)
        return self.password_path, self.users_path, self.json_path, self.adming_path

    def root_configure(self):
        self.root.title('BlockedUsers')
        self.root.iconbitmap(true_path('project', 'blocked.ico'))
        self.root.winfo_screenwidth()
        self.root.winfo_screenheight()
        self.root.geometry(f'335x205+{self.screen_width}+{self.screen_height}')
        self.root.resizable(False, False)

    def menu_configure(self):
        if self.password_path is None or not os.path.exists(self.password_path):
            self.menu.entryconfig("Password", state="disabled")
        if self.users_path is None or not os.path.exists(self.users_path):
            self.menu.entryconfig("Users", state="disabled")
        if self.json_path is None or not os.path.exists(self.json_path):
            self.menu.entryconfig("JSON", state="disabled")
        if self.adming_path is None or not os.path.exists(self.adming_path):
            self.menu.entryconfig("AdminG", state="disabled")

    def elements_configure(self):
        self.main_menu = tkinter.Menu(self.root)
        self.menu = tkinter.Menu(self.main_menu, tearoff=0)
        self.menu.add_command(label="AdminG", command=lambda: open_path(self.load_settings()[3]))
        self.menu.add_separator()
        self.menu.add_command(label="Password", command=lambda: open_path(self.load_settings()[0]))
        self.menu.add_command(label="Users", command=lambda: open_path(self.load_settings()[1]))
        self.menu.add_command(label="JSON", command=lambda: open_path(self.load_settings()[2]))
        self.menu.add_separator()
        self.menu.add_command(label="Settings", command=lambda: self.create_settings())
        self.main_menu.add_cascade(label='Меню ☰', menu=self.menu)
        self.root.config(menu=self.main_menu)
        self.menu_configure()

        self.main_frame = ttk.Frame(self.root, width=335, height=205)
        self.input_frame = ttk.Frame(self.main_frame, width=400, height=40)
        self.radio_frame = ttk.Frame(self.main_frame, width=400, height=25)
        self.output_frame = ttk.Frame(self.main_frame, width=400, height=120)

        self.dates_label = tkinter.Label(self.output_frame, text='dates:', width=8)
        self.dates_text = tkinter.Text(self.output_frame, wrap="word", width=34, height=6)

        self.add_symbol = tkinter.StringVar()
        self.comment_label = tkinter.Label(self.radio_frame, text='comm:')
        self.comment_entry = tkinter.Entry(self.radio_frame, width=25)
        self.plus = ttk.Radiobutton(self.radio_frame, text='+', variable=self.add_symbol, value='+')
        self.minus = ttk.Radiobutton(self.radio_frame, text='-', variable=self.add_symbol, value='-')
        self.add_symbol.set('+')

        self.email_label = tkinter.Label(self.input_frame, text='e-mail:')
        self.email_entry = tkinter.Entry(self.input_frame, width=25)
        add_placeholder(self.email_entry, 'example@email.com')
        self.email_check_button = ttk.Button(self.input_frame,
                                             text='Check',
                                             command=lambda: check_user(self.email_entry, self.dates_text, self.load_settings()[2]),
                                             width=8
                                             )
        self.email_add_button = ttk.Button(self.input_frame,
                                           text='Add',
                                           command=lambda: add_user_info_to_bd(self.email_entry,
                                                                               self.dates_text,
                                                                               self.add_symbol.get(),
                                                                               self.comment_entry,
                                                                               self.load_settings()[1],
                                                                               self.load_settings()[2]),
                                           width=8)

    def elements_creation(self):
        self.main_frame.place(x=0, y=0)
        self.input_frame.place(x=0, y=0)
        self.radio_frame.place(x=0, y=40)
        self.output_frame.place(x=0, y=65)

        self.email_label.place(x=6, y=20, anchor='w')
        self.email_entry.place(x=50, y=20, anchor='w')
        self.email_check_button.place(x=210, y=20, anchor='w')
        self.email_add_button.place(x=270, y=20, anchor='w')

        self.comment_label.place(x=5, y=10, anchor='w')
        self.comment_entry.place(x=50, y=10, anchor='w')
        self.plus.place(x=265, y=10, anchor='w')
        self.minus.place(x=300, y=10, anchor='w')

        self.dates_label.place(x=0, y=55, anchor='w')
        self.dates_text.place(x=50, y=60, anchor='w')


if __name__ == '__main__':
    users_list_app = UsersList()
