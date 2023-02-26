import os
import re


def next_file(path: str) -> str:
    """
    Принимает на вход путь к файлу - возвращает путь к следующему после него файлу
    :param path: Путь к файлу
    """
    if os.path.isfile(path):
        keyword_path, file_name = os.path.split(path)
        number = re.search(r'\d{4}', file_name)
        img_num = int(number.group(0))
        img_num += 1
        if img_num < 1000:
            next_element = os.path.join(keyword_path, re.sub(r'\d{4}', f'{img_num:04d}', file_name))
            return next_element
        else:
            return None
    else:
        return "File doesn't exist"
