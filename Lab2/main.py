import csv
import os

CLASSES = ["polar bear", "brown bear"]


def check_file(directory: str) -> None:
    """
    Проверяет существование файла annotation.csv.
    :param directory: Название директории.
    """
    try:
        if os.path.isfile(f"{directory}/annotation.csv"):
            os.remove(f"{directory}/annotation.csv")
    except OSError as err:
        print(f"Error: {err}")


class Annotation:
    def __init__(self, directory: str, class_name: str) -> None:
        """
        :param directory: Название директории
        :param class_name: Название класса
        """
        self.directory = directory
        self.class_name = class_name
        self.row = 0

    def add(self, abs_path: str, img_name: str, count: int) -> None:
        """
        Добавление строки, в которой содержатся абсолютный и относительный пути к файлу и название класса
        :param abs_path: Абсолютный путь к файлу
        :param img_name: Название файла с изображением
        :param count: Число вхождений. Необходимо, чтобы постоянно не записывалась строка: "Absolute path,
        Relative path, Class name"
        """
        with open(os.path.join(self.directory, "annotation.csv"), "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            if (self.row == 0) & (count == 0):
                writer.writerow(["Absolute path", "Relative path", "Class name"])
                self.row += 1
            writer.writerow([abs_path, os.path.join(self.directory, self.class_name, img_name), self.class_name])
            self.row += 1


if __name__ == "__main__":
    count = 0
    check_file("dataset")
    for class_name in CLASSES:
        obj = Annotation("dataset", class_name)
        for index in range(999):
            abs_path = os.path.abspath(os.path.join(class_name, f"{index:04d}.jpg"))
            obj.add(abs_path, f"{index:04d}.jpg", count)
        count += 1
