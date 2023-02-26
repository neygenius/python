import csv
import os
import logging

file_log = logging.FileHandler("lab2.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.DEBUG)

KEYWORDS = ["polar bear", "brown bear"]


def check_file(path: str) -> None:
    """
    Проверяет существование файла annotation.csv
    :param path: Директория
    """
    try:
        if os.path.isfile(f"{path}/annotation.csv"):
            os.remove(f"{path}/annotation.csv")
    except OSError as err:
        logging.error(f"File was not found. Error: {err}", exc_info=True)


class AnnotationFile:
    def __init__(self, directory: str, class_name: str) -> None:
        """
        :param directory: Директория
        :param class_name: Название класса
        """
        self.row_number = 0
        self.directory = directory
        self.class_name = class_name

    def add(self, abs_path: str, img_name: str) -> None:
        """
        Добавление в файл аннотации строки, в которой содержатся абсолютный и относительный пути
        к изображению, а также название класса
        :param abs_path: Абсолютный путь к изображению
        :param img_name: Название файла с изображением
        """
        with open(os.path.join(self.directory, "annotation.csv"), "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow([abs_path, os.path.join(self.directory, img_name), self.class_name])
            self.row_number += 1
        logging.debug(f"Line about file <{img_name}> has been added to the annotation file")
