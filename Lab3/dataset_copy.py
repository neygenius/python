import os
import shutil
import main
import logging
from tqdm import tqdm
from main import AnnotationFile

file_log = logging.FileHandler("lab2.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.DEBUG)


def create_dataset(directory: str) -> None:
    """
    Создание нового dataset и проверка его существования
    :param directory: Директория
    """
    try:
        if not os.path.isdir(directory):
            os.mkdir(directory)
            logging.debug(f"Folder <{directory}> has been created")
        else:
            shutil.rmtree(directory)
            os.mkdir(directory)
            logging.debug(f"Folder <{directory}> has been created")
    except OSError as err:
        logging.error(f"Folder could not be created. Error: {err}", exc_info=True)


def copy_img(obj: type(AnnotationFile), origin_folder: str, number: int) -> None:
    """
    Копирует изображение из dataset в dataset1, меняет его название и добавляет в новую аннотацию
    :param obj: Объект Annotation
    :param origin_folder: Изначальная директория датасета
    :param number: Номер изображения
    """
    shutil.copy(os.path.join(origin_folder, obj.class_name, f"{number:04d}.jpg"), obj.directory)
    logging.debug(f"Image of {obj.class_name} {number:04d}.jpg has been copied from <{origin_folder}> to <{obj.directory}>")
    os.rename(os.path.join(obj.directory, f"{number:04d}.jpg"),
              os.path.join(obj.directory, f"{obj.class_name}_{number:04d}.jpg"))
    logging.debug(f"Name of {obj.class_name} image has been changed from <{number:04d}.jpg> "
                  f"to <{obj.class_name}_{number:04d}.jpg>")
    abs_path = os.path.abspath(os.path.join(obj.directory, f"{obj.class_name}_{number:04d}.jpg"))
    obj.add(abs_path, f"{obj.class_name}_{number:04d}.jpg")


if __name__ == "__main__":
    create_dataset("dataset1")
    main.check_file("dataset1")
    counter = 0
    pbar = tqdm(total=2000)
    for keyword in main.KEYWORDS:
        for number in range(1000):
            copy_img(AnnotationFile("dataset1", keyword), "dataset", number)
            counter += 1
            pbar.update(1)
    logging.debug(f"{counter} lines were added to the annotation file")
