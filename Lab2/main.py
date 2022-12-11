import csv
import os

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
        print(f"Error: {err}")


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
        Добавление строки, в которой содержатся абсолютный и относительный пути к изображению, а также название класса
        :param abs_path: Абсолютный путь к изображению
        :param img_name: Название файла с изображением
        """
        with open(os.path.join(self.directory, "annotation.csv"), "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow([abs_path, os.path.join(self.directory, self.class_name, img_name), self.class_name])
            self.row_number += 1


if __name__ == "__main__":
    check_file("dataset")
    for keyword in KEYWORDS:
        obj = AnnotationFile("dataset", keyword)
        for number in range(999):
            abs_path = os.path.abspath(os.path.join(keyword, f"{number:04d}.jpg"))
            obj.add(abs_path, f"{number:04d}.jpg")
