import tkinter
import datetime
from tkinter import ttk
from functions.operations import load_file, save_dict


def add_user_info_to_bd(email_field: tkinter.Entry, text_field: tkinter.Text, signature: str, comment_field: tkinter.ttk.Entry, text_file_path: str, json_file_path: str):
    text_field.delete('1.0', tkinter.END)
    email_field_object = email_field
    email_field_get = email_field.get()
    today_date = datetime.date.today().strftime('%d.%m.%y')
    if not comment_field.get():
        today_date_with_signature = signature + datetime.date.today().strftime('%d.%m.%y')
    else:
        today_date_with_signature = signature + datetime.date.today().strftime('%d.%m.%y') + f' ({comment_field.get()})'

    if json_file_path is not None:
        text_field.configure(fg='black')
        my_dict = load_file(json_file_path)
    else:
        text_field.configure(fg='red')
        text_field.delete('1.0', tkinter.END)
        # text_field.insert('1.0', f'Error! JSON file is not selected! Please specify the path to the JSON-file in the settings.')
        text_field.insert('1.0', f'Ошибка! Файл JSON не выбран! Пожалуйста, укажите путь до JSON файла в настройках.')
        return False

    if text_file_path is not None:
        text_field.configure(fg='black')
    else:
        text_field.configure(fg='red')
        text_field.delete('1.0', tkinter.END)
        # text_field.insert('1.0', f'Error! Users text file is not selected! Please specify the path to the text file in the settings.')
        text_field.insert('1.0', f'Ошибка! Текстовый файл не выбран! Пожалуйста, укажите путь до текстового файла в настройках.')
        return False


    if email_field_get and '@' in email_field_get and 'black' in email_field_object.config()['foreground']:
        if email_field_get not in my_dict.keys():
            my_dict[email_field_get] = [today_date_with_signature]
            add_new_user_to_text_list(email_field_get, today_date_with_signature, text_file_path)
            text_field.delete('1.0', tkinter.END)
            text_field.insert('1.0', f'Новый пользователь {email_field_get} успешно добавлен {today_date_with_signature}')
        # elif '+' + today_date not in my_dict[email] and '-' + today_date not in my_dict[email] and not [today_date not in item for item in my_dict[email]]:
        elif not any((today_date in item for item in my_dict[email_field_get])):
            my_dict[email_field_get].append(today_date_with_signature)
            add_date_to_user_text_list(email_field_get, today_date_with_signature, text_file_path)
            text_field.delete('1.0', tkinter.END)
            text_field.insert('1.0', f'Дата {today_date_with_signature} добавлена для пользователя {email_field_get}')
        # elif '+' + today_date in my_dict[email] or '-' + today_date in my_dict[email] or [today_date in item for item in my_dict[email]]:
        elif any((today_date in item for item in my_dict[email_field_get])):
            # dialog(f'Дата {today_date} уже была добавлена ранее!')
            text_field.configure(fg='red')
            text_field.delete('1.0', tkinter.END)
            text_field.insert('1.0', f'Дата {today_date} уже была добавлена ранее!')
        save_dict(my_dict, json_file_path)
        comment_field.delete(0, 'end')
    elif not email_field_get or '@' not in email_field_get or 'gray' in email_field_object.config()['foreground']:
        # dialog('Введите e-mail!')
        text_field.delete('1.0', tkinter.END)
        text_field.insert('1.0', 'Введите e-mail!')

    return True


def add_new_user_to_text_list(email, today_date, text_file_path: str):
    line = '\n' + ('-' * 109) + '\n'
    if text_file_path is not None:
        with open(text_file_path, 'a') as text_list:
            text_list.write(line + email + '\t\t' + today_date)


def add_date_to_user_text_list(email, today_date, text_file_path: str):
    if text_file_path is not None:
        with open(text_file_path, 'r') as text_list:
            lines = text_list.readlines()

        with open(text_file_path, 'w') as text_list:
            for line in lines:
                if email in line:
                    line = line.strip() + '\t\t' + today_date + '\n'
                text_list.write(line)
