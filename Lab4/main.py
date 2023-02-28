import pandas as pd
from csv import Sniffer
import numpy as np
from matplotlib import pyplot as plt
import cv2

KEYWORDS = ["polar bear", "brown bear"]


def check_header(file_name: str) -> str:
    """
    Проверяет наличие заголовка у файла аннотации, добавлет его по необходимости
    :param file_name: Название файла аннотации
    """
    with open(file_name, "rb") as csv_file:
        sniffer = Sniffer()
        has_header = sniffer.has_header(csv_file.read(2048))
        csv_file.seek(0)
    if not has_header:
        df = pd.read_csv(file_name)
        header_list = ["Абсолютный путь", "Относительный путь", "Название класса"]
        new_name = "new_annotation.csv"
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
    height = []
    width = []
    depth = []
    mark = (df.class_name != KEYWORDS[0])
    df["class_mark"] = mark.astype(int)
    for path in df["absolute_path"]:
        image = cv2.imread(path)
        image_height, image_width, image_depth = image.shape
        height.append(image_height)
        width.append(image_width)
        depth.append(image_depth)
    df["height"] = height
    df["width"] = width
    df["depth"] = depth


def mark_filter(df: pd.DataFrame, mark: int) -> pd.DataFrame:
    """
    Фильтрует датафрейма по метке класса
    :param df: Датафрейм
    :param mark: Метка класса
    """
    return df[df.class_mark == mark]


def mark_and_max_filter(df: pd.DataFrame, mark: int, max_height: int, max_width: int) -> pd.DataFrame:
    """
    Фильтрует датафрейма по метке класса, максимальной высоте и ширине изображения
    :param df: Датафрейм
    :param mark: Метка класса
    :param max_height: Максимальное значение высоты изображения
    :param max_width: Максимальное значение ширины изображения
    """
    return df[((df.class_mark == mark) & (df.height <= max_height) & (df.width <= max_width))]


def grouping(df: pd.DataFrame) -> tuple:
    """
    Группирует датафрейм по максимальному, минимальному и среднему количеству пикселей, а также фильтрует по метке класса
    :param df: Датафрейм
    """
    df["pixel_count"] = df["height"] * df["width"] * df["depth"]
    return df.groupby("class_mark").max(), df.groupby("class_mark").min(), df.groupby("class_mark").mean()


def histogram(df: pd.DataFrame, mark: int) -> list:
    """
    Строит гистограмму по датафрейму и метке класса
    :param df: Датафрейм
    :param mark: Метка класса
    """
    df = mark_filter(df, mark)
    path = np.random.choice(df.absolute_path.to_numpy())
    image = cv2.imread(path)
    height, width, depth = image.shape
    return [cv2.calcHist([image], [0], None, [255], [0, 255]) / (height * width),
            cv2.calcHist([image], [1], None, [255], [0, 255]) / (height * width),
            cv2.calcHist([image], [2], None, [255], [0, 255]) / (height * width)]


def histogram_drawing(df: pd.DataFrame, mark: int) -> None:
    """
    Отрисовывает гистограмму
    :param df: Датафрейм
    :param mark: Метка класса
    """
    histograms = histogram(df, mark)
    plt.title("Histogram")
    plt.ylabel("Number of pixel")
    plt.xlabel("Intensity value")
    plt.xlim([0, 255])
    plt.plot(histograms[0], "b")
    plt.plot(histograms[1], "g")
    plt.plot(histograms[2], "r")
    plt.show()


if __name__ == "__main__":
    test = create_dataframe("annotation.csv")
    test.to_csv("DataFrame")
    mark_filter(test, 1).to_csv("DataFrame_1")
    mark_and_max_filter(test, 1, 310, 500).to_csv("DataFrame_2")
    histogram_drawing(test, 0)
