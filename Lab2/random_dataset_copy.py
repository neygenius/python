import os
import shutil
import random
import main
from main import AnnotationFile
import dataset_copy


def random_copy_img(obj: type(AnnotationFile), number: int) -> None:
    """
    Копирует изображение из dataset в dataset2, дает ему случайное название (номер от 0 до 10000)
    и добавляет в новую аннотацию
    :param obj: Объект класса Annotation
    :param number: Номер изображения
    """
    repeat = 0
    while repeat == 1:
        rand_number = random.randint(0, 10000)
        if os.path.isfile(os.path.join(obj.directory, f"{rand_number:05d}.jpg")):
            repeat = 1
        else:
            break
        shutil.copy(os.path.join("dataset", obj.class_name, f"{number:04d}.jpg"), obj.directory)
        os.rename(os.path.join(obj.directory, f"{number:04d}.jpg"),
                  os.path.join(obj.directory, f"{rand_number:05d}.jpg"))
        obj.add(os.path.abspath(obj.directory), f"{rand_number:05d}.jpg")


if __name__ == "__main__":
    dataset_copy.create_dataset("dataset2")
    main.check_file("dataset2")
    for keyword in main.KEYWORDS:
        for number in range(999):
            random_copy_img(AnnotationFile("dataset2", keyword), number)
