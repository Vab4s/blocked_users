import json
import tkinter
import tkinter.messagebox
import subprocess
import os
import sys


def open_application(adming_app_path):
    subprocess.Popen(['java', '-jar', adming_app_path])

def open_path(path):
    if path:
        os.startfile(path)
    else:
        dialog('Не задан путь до файла/директории')

def load_file(file_path: str):
    with open(file_path, 'r') as file:
        if 'json' in file_path:
            return json.load(file)
        elif 'txt' in file_path:
            return file.readlines()

def save_dict(dictionary: dict, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(dictionary, file, indent=4)

def select_all_text(event):
    event.widget.select_range(0, tkinter.END)
    event.widget.icursor(tkinter.END)

def dialog(text: str, alert=1):
    if alert:
        tkinter.messagebox.showwarning('Внимание!', text)
    elif not alert:
        tkinter.messagebox.showinfo('Уведомление', text)

def true_path(folder, file):
    if getattr(sys, '_MEIPASS', False):  # Check if running from PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    file_path = os.path.join(base_path, folder, file)

    return file_path