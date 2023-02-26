import os
import shutil
import random
import logging
from main import AnnotationFile

file_log = logging.FileHandler("lab2.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.DEBUG)

RAND_DICT = {n: r_n for n, r_n in zip(range(2000), list(random.sample(range(10000), 2000)))}


def random_copy_img(obj: type(AnnotationFile), origin_folder: str, number: int, rand_number: int) -> None:
    """
    Копирует изображение из dataset в dataset2, дает ему случайное название (номер от 0 до 10000)
    и добавляет в новую аннотацию
    :param obj: Объект Annotation
    :param origin_folder: Изначальная директория датасета
    :param number: Номер изображения
    :param rand_number: Новый случайный номер изображения
    """
    shutil.copy(os.path.join(origin_folder, obj.class_name, f"{number:04d}.jpg"), obj.directory)
    logging.debug(f"Image of {obj.class_name} {number:04d}.jpg has been copied from <{origin_folder}> to <{obj.directory}>")
    os.rename(os.path.join(obj.directory, f"{number:04d}.jpg"),
              os.path.join(obj.directory, f"{rand_number:05d}.jpg"))
    logging.debug(f"Name of {obj.class_name} image has been changed from <{number:04d}.jpg> "
                  f"to <{rand_number:05d}.jpg>")
    abs_path = os.path.abspath(os.path.join(obj.directory, f"{rand_number:05d}.jpg"))
    obj.add(abs_path, f"{rand_number:05d}.jpg")
