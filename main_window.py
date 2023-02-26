import os
import sys
from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QFileDialog, QLabel
from dataset_copy import create_dataset, copy_img
from main import check_file, KEYWORDS, AnnotationFile
from random_dataset_copy import random_copy_img, RAND_DICT
from Iterator import FileIterator

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("PIC.WORK")
        self.setMinimumSize(1260, 700)
        self.setStyleSheet("background-color: #e6e6fa")

        self.folder = QFileDialog.getExistingDirectory(self, "Select folder")
        src = QLabel(f"MAIN DATASET: {self.folder}", self)
        src.setStyleSheet("color: #2525ba; font-family: Arial")
        src.setFixedSize(300, 50)
        src.move(5, 0)

        self.counter_one = 0
        self.counter_two = 0
        self.path_one = self.get_zero_path(KEYWORDS[0])
        self.path_two = self.get_zero_path(KEYWORDS[1])

        self.img_one = QLabel(self)
        self.img_one.resize(QSize(600, 400))
        self.img_one.setStyleSheet("border: None")
        self.img_one.move(20, 200)

        self.img_two = QLabel(self)
        self.img_two.resize(600, 400)
        self.img_two.setStyleSheet("border: None")
        self.img_two.move(640, 200)

        button_create_annotation = self.add_button("CREATE AN ANNOTATION", 25, 80)
        button_create_annotation.clicked.connect(self.create_annotation)

        button_copy = self.add_button("COPY A DATASET", 225, 80)
        button_copy.clicked.connect(self.dataset_copy)

        button_random_copy = self.add_button("RANDOM COPY A DATASET", 425, 80)
        button_random_copy.clicked.connect(self.random_copy)

        next_p_bear_button = self.add_button("SHOW NEXT POLAR BEAR", 625, 80)
        next_p_bear_button.clicked.connect(lambda class_name=KEYWORDS[0]: self.next_image(KEYWORDS[0]))

        next_b_bear_button = self.add_button("SHOW NEXT BROWN BEAR", 825, 80)
        next_b_bear_button.clicked.connect(lambda class_name=KEYWORDS[1]: self.next_image(KEYWORDS[1]))

        exit_button = self.add_button("QUIT", 1025, 80)
        exit_button.clicked.connect(self.quit)

        self.show()

    def get_zero_path(self, keyword: str) -> str:
        """
        Возвращает путь к первому изображению указанного класса
        :param keyword: Класс изображения
        """
        file_list = []
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.folder, keyword)):
            file_list.extend(filenames)
        path = os.path.join(self.folder, keyword, file_list[0])
        return path

    def add_button(self, button_name: str, x: int, y: int):
        """
        Добавление кнопки
        :param button_name: Надпись
        :param x: Координата по X
        :param y: Координата по Y
        """
        button = QPushButton(button_name, self)
        button.setFixedSize(QSize(180, 50))
        button.setStyleSheet("background-color: #6767e0; color: #e6e6fa; border: none; font-family: Arial")
        button.move(x, y)
        return button

    def create_annotation(self) -> None:
        """
        Создание аннотации
        """
        check_file(self.folder)
        n = 0
        for keyword in KEYWORDS:
            obj = AnnotationFile(self.folder, keyword)
            for num in range(len(os.listdir(os.path.join(self.folder, keyword)))):
                obj.add(os.path.abspath(os.path.join(keyword, f"{num:04d}.jpg")), f"{num:04d}.jpg")

    def dataset_copy(self) -> None:
        """
        Копирование датасета
        """
        new_folder = QFileDialog.getExistingDirectory(self, "Select folder for copying")
        if new_folder != self.folder:
            create_dataset(new_folder)
            check_file(new_folder)
            for keyword in KEYWORDS:
                for num in range(len(os.listdir(os.path.join(self.folder, keyword)))):
                    copy_img(AnnotationFile(new_folder, keyword), self.folder, num)

    def random_copy(self) -> None:
        """
        Копирует датасет в другую директорию с присвоением случайного номера
        """
        new_r_folder = QFileDialog.getExistingDirectory(self, "Select folder for copying")
        if new_r_folder != self.folder:
            create_dataset(new_r_folder)
            check_file(new_r_folder)
            flag = 0
            for keyword in KEYWORDS:
                for num in range(len(os.listdir(os.path.join(self.folder, keyword)))):
                    random_copy_img(AnnotationFile(new_r_folder, keyword), self.folder, num, RAND_DICT.get(num + flag))
                flag += 1000

    def next_image(self, keyword: str) -> None:
        """
        Выводит следующее изображение класса
        :param keyword: Класс изображения
        """
        if keyword == KEYWORDS[0]:
            if self.counter_one < len(os.listdir(os.path.join(self.folder, keyword))) - 1:
                self.counter_one += 1
                obj = FileIterator(self.path_one)
                self.path_one = obj.__next__()
                self.img_one.setPixmap(QtGui.QPixmap(self.path_one).scaled(self.img_one.size(),
                                                                           aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
        else:
            if self.counter_two < len(os.listdir(os.path.join(self.folder, keyword))) - 1:
                self.counter_two += 1
                obj = FileIterator(self.path_two)
                self.path_two = obj.__next__()
                self.img_two.setPixmap(QtGui.QPixmap(self.path_two).scaled(self.img_two.size(),
                                                                           aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

    def quit(self) -> None:
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()





