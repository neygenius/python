import os
import shutil
import main
from main import Annotation


def create_dataset(directory: str) -> None:
    """
    Создание нового Датасета и проверка его существования
    :param directory: Название директории
    """
    try:
        if not os.path.isdir(directory):
            os.mkdir(directory)
        else:
            shutil.rmtree(directory)
            os.mkdir(directory)
    except OSError as err:
        print(f"Error: {err}")


def copy_element(obj: type(Annotation), count: int, index: int) -> None:
    """
    Переносит элемент из dataset в dataset1, меняет его название и добавляет в новую аннотацию
    :param obj: Объект класса Annotation
    :param count: Число вхождений. Необходимо, чтобы постоянно не записывалась строка: "Absolute path,
    Relative path, Class name"
    :param index: Индекс изображения.
    """
    shutil.copy(os.path.join("dataset", obj.class_name, f"{index:04d}.jpg"), obj.directory)
    os.rename(os.path.join(obj.directory, f"{index:04d}.jpg"),
              os.path.join(obj.directory, f"{obj.class_name}_{index:04d}.jpg"))
    obj.add(os.path.abspath(obj.directory), f"{obj.class_name}_{index:04d}.jpg", count)


if __name__ == "__main__":
    count = 0
    create_dataset("dataset1")
    main.check_file("dataset1")
    for class_name in main.CLASSES:
        for index in range(999):
            copy_element(Annotation("dataset1", class_name), count, index)
            count += 1
