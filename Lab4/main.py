import pandas as pd
from csv import Sniffer
import cv2

KEYWORDS = ["polar bear", "brown bear"]


def check_header(file_name: str) -> str:
    """
    Проверяет наличие загаловка у файла аннотации, добавлет его по необходимости
    :param file_name: Название файла аннотации
    """
    with open(file_name, "rb") as csv_file:
        sniffer = Sniffer()
        has_header = sniffer.has_header(csv_file.read(2048))
        csv_file.seek(0)
    if not has_header:
        df = pd.read_csv(file_name)
        header_list = ["Абсолютный путь", "Относительный путь", "Название класса"]
        new_name = "annotation.csv"
        df.to_csv(new_name, header=header_list, index=False)
        return new_name
    else:
        return file_name


def create_dataframe(file_name: str) -> pd.DataFrame:
    """
    Создает датафрейм по аннотации
    :param file_name: Название файла аннотации
    """
    actual_name = check_header(file_name)
    df = pd.read_csv(actual_name, usecols=["Абсолютный путь", "Название класса"])
    df = df.rename(columns={"Абсолютный путь": "absolute_path", "Название класса": "class_name"})
    return df


def add_columns(df: pd.DataFrame) -> None:
    """
    Добавляет в датафрейм столбцы: метка класса, высота, ширина и глубина цвета изображения
    :param df: Датафрейм
    """
    width = []
    height = []
    color_depth = []
    mark = (df.class_name != KEYWORDS[0])
    df["class_label"] = mark.astype(int)
    for path in df["absolute_path"]:
        image = cv2.imread(path)
        image_height, image_width, image_depth = image.shape
        height.append(image_height)
        width.append(image_width)
        color_depth.append(image_depth)
    df["height"] = height
    df["width"] = width
    df["depth"] = color_depth


