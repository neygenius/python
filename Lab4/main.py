import pandas as pd
import csv


def check_header(file_name: str) -> str:
    """
    Проверяет наличие загаловка у файла аннотации, добавлет его по необходимости
    :param file_name: Название файла аннотации
    """
    with open(file_name, "rb") as csv_file:
        sniffer = csv.Sniffer()
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
    df = df.rename(columns={"Абсолютный путь": "abs_path", "Название класса": "class_name"})
    return df


