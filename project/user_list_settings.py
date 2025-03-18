import tkinter
from tkinter import ttk
from tkinter import filedialog
import os
import configparser

from functions.operations import dialog, true_path


class Settings:
    def __init__(self, main_root, menu, screen_width, screen_height):
        self.SETTINGS_FILE = true_path('project', 'settings.ini')

        self.main_root = main_root
        self.screen_width = screen_width + 45
        self.screen_height = screen_height + 50

        self.menu = menu
        self.config = configparser.ConfigParser()
        self.config['Settings'] = {}
        self.users_path = None
        self.password_path = None
        self.json_path = None
        self.adming_path = None
        self.load_settings()

        self.main_frame = None
        self.password_label = None
        self.password_path_entry = None
        self.password_add_button = None
        self.users_label = None
        self.users_entry = None
        self.users_add_button = None
        self.json_label = None
        self.json_entry = None
        self.adming_label = None
        self.adming_entry = None
        self.adming_add_button = None
        self.json_add_button = None
        self.save_button = None

        self.subroot = tkinter.Toplevel(self.main_root)
        self.root_configure(self.main_root)
        self.elements_configure()
        self.elements_creation()
        self.subroot.mainloop()

    # Загрузить пути из INI-файла в переменные
    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            self.config.read(self.SETTINGS_FILE)
            self.password_path = self.config.get('Settings', 'password_path', fallback=None)
            self.users_path = self.config.get('Settings', 'users_path', fallback=None)
            self.json_path = self.config.get('Settings', 'json_path', fallback=None)
            self.adming_path = self.config.get('Settings', 'adming_path', fallback=None)
        return self.password_path, self.users_path, self.json_path, self.adming_path

    @staticmethod
    def fill_settings(element, variable):
        if variable is not None and os.path.exists(variable):
            element.insert(0, variable)
        element.config(state='readonly')

    def save_settings(self):
        self.password_path = self.password_path_entry.get()
        self.users_path = self.users_entry.get()
        self.json_path = self.json_entry.get()
        self.adming_path = self.adming_entry.get()
        if self.password_path and self.users_path and self.json_path and self.adming_path:
            self.config['Settings']['password_path'] = self.password_path
            self.config['Settings']['users_path'] = self.users_path
            self.config['Settings']['json_path'] = self.json_path
            self.config['Settings']['adming_path'] = self.adming_path
            with open(self.SETTINGS_FILE, 'w') as configfile:
                self.config.write(configfile)
            self.menu.entryconfig("AdminG", state="normal")
            self.menu.entryconfig("Password", state="normal")
            self.menu.entryconfig("Users", state="normal")
            self.menu.entryconfig("JSON", state="normal")
        else:
            if self.password_path:
                self.config['Settings']['password_path'] = self.password_path
                with open(self.SETTINGS_FILE, 'w') as configfile:
                    self.config.write(configfile)
                self.menu.entryconfig("Password", state="normal")
            if self.users_path:
                self.config['Settings']['users_path'] = self.users_path
                with open(self.SETTINGS_FILE, 'w') as configfile:
                    self.config.write(configfile)
                self.menu.entryconfig("Users", state="normal")
            if self.json_path:
                self.config['Settings']['json_path'] = self.json_path
                with open(self.SETTINGS_FILE, 'w') as configfile:
                    self.config.write(configfile)
                self.menu.entryconfig("JSON", state="normal")
            if self.adming_path:
                self.config['Settings']['adming_path'] = self.adming_path
                with open(self.SETTINGS_FILE, 'w') as configfile:
                    self.config.write(configfile)
                self.menu.entryconfig("AdminG", state="normal")

            dialog('Не все поля заполнены!')
        self.close_settings()

    def close_settings(self):
        self.subroot.destroy()
        self.main_root.attributes('-alpha', 1)
        self.main_root.grab_release()

    # Выбрать файл соответствующего типа / директорию, вставить путь в энтри-элемент
    @staticmethod
    def get_file_path(entry_element, file_type):
        file_path = None
        if file_type == 'txt':
            file_path = filedialog.askopenfilename(defaultextension = ".txt",
                                                   filetypes = [("Text files", "*.txt"), ("All files", "*.*")])
        elif file_type == 'json':
            file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                   filetypes=[("Json files", "*.json"), ("All files", "*.*")])
        elif file_type == 'jar':
            file_path = filedialog.askopenfilename(defaultextension=".jar",
                                                   filetypes=[("Java files", "*.jar"), ("All files", "*.*")])
        elif file_type == 'dir':
            file_path = filedialog.askdirectory()

        if file_path:
            entry_element.config(state='normal')
            entry_element.delete(0, 'end')
            entry_element.insert(0, file_path)
            entry_element.config(state='readonly')

    def root_configure(self, root):
        self.subroot.title('Settings')
        self.subroot.geometry(f'275x155+{self.screen_width}+{self.screen_height}')
        self.subroot.resizable(False, False)
        self.subroot.focus_set()
        self.subroot.grab_set()
        self.subroot.transient(root)
        self.subroot.attributes('-toolwindow', True)
        self.main_root.attributes('-alpha', 0.75)
        self.subroot.protocol("WM_DELETE_WINDOW", self.close_settings)

    def elements_configure(self):
        self.main_frame = tkinter.Frame(self.subroot, width=275, height=155)

        self.password_label = tkinter.Label(self.main_frame, text='Password path:')
        self.password_path_entry = tkinter.Entry(self.main_frame)
        self.password_add_button = ttk.Button(self.main_frame, text='Add', width=6, command=lambda: self.get_file_path(self.password_path_entry, 'txt'))

        self.users_label = tkinter.Label(self.main_frame, text='Users (legacy):')
        self.users_entry = tkinter.Entry(self.main_frame)
        self.users_add_button = ttk.Button(self.main_frame, text='Add', width=6, command=lambda: self.get_file_path(self.users_entry, 'txt'))

        self.json_label = tkinter.Label(self.main_frame, text='JSON path:')
        self.json_entry = tkinter.Entry(self.main_frame)
        self.json_add_button = ttk.Button(self.main_frame, text='Add', width=6, command=lambda: self.get_file_path(self.json_entry, 'json'))

        self.adming_label = tkinter.Label(self.main_frame, text='AdminG path:')
        self.adming_entry = tkinter.Entry(self.main_frame)
        self.adming_add_button = ttk.Button(self.main_frame, text='Add', width=6, command=lambda: self.get_file_path(self.adming_entry, 'dir'))

        self.fill_settings(self.password_path_entry, self.password_path)
        self.fill_settings(self.users_entry, self.users_path)
        self.fill_settings(self.json_entry, self.json_path)
        self.fill_settings(self.adming_entry, self.adming_path)

        self.save_button = ttk.Button(self.main_frame, text='Save', width=6, command=lambda: self.save_settings())

    def elements_creation(self):
        self.main_frame.place(x=0, y=0)
        self.password_label.place(x=3, y=15)
        self.password_path_entry.place(x=90, y=15)
        self.password_add_button.place(x=220, y=12)
        self.users_label.place(x=7, y=40)
        self.users_entry.place(x=90, y=40)
        self.users_add_button.place(x=220, y=37)
        self.json_label.place(x=25, y=65)
        self.json_entry.place(x=90, y=65)
        self.json_add_button.place(x=220, y=62)
        self.adming_label.place(x=9, y=90)
        self.adming_entry.place(x=90, y=90)
        self.adming_add_button.place(x=220, y=87)
        self.save_button.place(x=115, y=120)
