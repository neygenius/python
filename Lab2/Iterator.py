import next


class ElementIterator:
    def __init__(self, element_path: str):
        """
        :param element_path: Путь к файлу
        """
        self.element_path = element_path

    def __next__(self) -> str:
        """
        Возвращает путь следующего элемента
        """
        self.element_path = next.next_element(self.element_path)
        return self.element_path


if __name__ == "__main__":
    obj = ElementIterator("dataset\\polar_bear\\0000.jpg")
    print(obj.__next__())
