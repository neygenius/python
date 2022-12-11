import os
import shutil
import main
from main import AnnotationFile


def create_dataset(directory: str) -> None:
    """
    Создание нового dataset и проверка его существования
    :param directory: Директория
    """
    try:
        if not os.path.isdir(directory):
            os.mkdir(directory)
        else:
            shutil.rmtree(directory)
            os.mkdir(directory)
    except OSError as err:
        print(f"Error: {err}")


def copy_img(obj: type(AnnotationFile), number: int) -> None:
    """
    Копирует изображение из dataset в dataset1, меняет его название и добавляет в новую аннотацию
    :param obj: Объект класса Annotation
    :param number: Номер изображения
    """
    shutil.copy(os.path.join("dataset", obj.class_name, f"{number:04d}.jpg"), obj.directory)
    os.rename(os.path.join(obj.directory, f"{number:04d}.jpg"),
              os.path.join(obj.directory, f"{obj.class_name}_{number:04d}.jpg"))
    obj.add(os.path.abspath(obj.directory), f"{obj.class_name}_{number:04d}.jpg")


if __name__ == "__main__":
    create_dataset("dataset1")
    main.check_file("dataset1")
    for keyword in main.KEYWORDS:
        for number in range(999):
            copy_img(AnnotationFile("dataset1", keyword), number)
