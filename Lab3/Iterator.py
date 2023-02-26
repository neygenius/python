import next


class FileIterator:
    def __init__(self, path: str) -> None:
        """
        :param path: Путь к файлу
        """
        self.path = path

    def __next__(self) -> str:
        """
        Возвращает путь к следующему файлу
        """
        self.path = next.next_file(self.path)
        return self.path


if __name__ == "__main__":
    obj = FileIterator("dataset\\polar_bear\\0000.jpg")
    print(obj.__next__())
