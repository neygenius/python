import os
import shutil
import main
import random
import logging
from tqdm import tqdm
from main import AnnotationFile
import dataset_copy

file_log = logging.FileHandler("lab2.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.DEBUG)


def random_copy_img(obj: type(AnnotationFile), number: int, rand_number: int) -> None:
    """
    Копирует изображение из dataset в dataset2, дает ему случайное название (номер от 0 до 10000)
    и добавляет в новую аннотацию
    :param obj: Объект Annotation
    :param number: Номер изображения
    :param rand_number: Новый случайный номер изображения
    """
    shutil.copy(os.path.join("dataset", obj.class_name, f"{number:04d}.jpg"), obj.directory)
    logging.debug(f"Image of {obj.class_name} {number:04d}.jpg has been copied from <dataset> to <{obj.directory}>")
    os.rename(os.path.join(obj.directory, f"{number:04d}.jpg"),
              os.path.join(obj.directory, f"{rand_number:05d}.jpg"))
    logging.debug(f"Name of {obj.class_name} image has been changed from <{number:04d}.jpg> "
                  f"to <{rand_number:05d}.jpg>")
    abs_path = os.path.abspath(os.path.join(obj.directory, f"{rand_number:05d}.jpg"))
    obj.add(abs_path, f"{rand_number:05d}.jpg")


if __name__ == "__main__":
    dataset_copy.create_dataset("dataset2")
    main.check_file("dataset2")
    random_set = list(random.sample(range(10000), 2000))
    random_dict = {n: r_n for n, r_n in zip(range(2000), random_set)}
    counter, flag = 0, 0
    pbar = tqdm(total=2000)
    for keyword in main.KEYWORDS:
        for number in range(1000):
            random_copy_img(AnnotationFile("dataset2", keyword), number,
                            random_dict.get(number + flag))
            counter += 1
            pbar.update(1)
        flag = 1000
    logging.debug(f"{counter} lines were added to the annotation file")
