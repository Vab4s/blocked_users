import tkinter
from functions.operations import load_file


def check_user(email: tkinter.Entry, text_field: tkinter.Text, json_path: str):
    if json_path is not None:
        text_field.configure(fg='black')
        my_dict = load_file(json_path)
        if 'black' in email.config()['foreground']:
            if email.get() in my_dict:
                text_field.delete('1.0', tkinter.END)
                for item in my_dict[email.get()]:
                    text_field.insert('1.0', item + '\n')
                # dialog('Пользователь уже присутствует в списке')
            elif email.get() and email.get() not in my_dict and '@' in email.get():
                text_field.delete('1.0', tkinter.END)
                text_field.insert('1.0', 'No unblocks for this user')
                # dialog('Пользователя нет в списке', 0)
            elif not email.get() or not '@' in email.get():
                text_field.delete('1.0', tkinter.END)
                # text_field.insert('1.0', 'Error! Enter e-mail!')
                text_field.insert('1.0', 'Введите e-mail!')
                # dialog('Введите e-mail!')
        elif 'gray' in email.config()['foreground']:
            text_field.delete('1.0', tkinter.END)
            # text_field.insert('1.0', 'Error! Enter e-mail!')
            text_field.insert('1.0', 'Введите e-mail!')
    else:
        text_field.configure(fg='red')
        text_field.delete('1.0', tkinter.END)
        # text_field.insert('1.0', 'Error! JSON file is not selected! Please specify the path to the JSON-file in the settings.')
        text_field.insert('1.0',
                          'Ошибка! Файл JSON не выбран! Пожалуйста, укажите путь до JSON файла в настройках.')