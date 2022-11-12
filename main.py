import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


URL = "https://yandex.ru/images/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}


def is_valid(url: str) -> bool:
    '''
    Функция, проверяющая наличие ссылки на файл в указанном атрибуте (источника)
    '''
    parsed = urlparse(url)
    if bool(parsed.netloc) and bool(parsed.scheme):


def get_images_urls(url: str, keyword: str, headers: dict, count=1000) -> list:
    '''
    Функция собирает список url ведущих к файлам изображений со страницы с поисковым запросом
    '''
    page = 1
    url_list = []
    while True:
        url_page = f"{url}search?p={page}&text={keyword}"
        html_page = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(html_page.content, "html.parser")
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                continue
            img_url = urljoin(url_page, img_url)
            if is_valid(img_url):
                url_list.append(img_url)
        page += 1
        if len(url_list) > count:
            break
    return url_list


def download_one_image(url: str, path: str, num: int) -> None:
    '''
    Функция скачивает и сохраняет одно изображение
    '''
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except PermissionError:
            print("Insufficient permissions to create a directory on the specified path")
    img = requests.get(url)
    file_name = f"{str(num).zfill(4)}.jpg"
    file = os.path.join(path, file_name)
    with open(file, "wb") as save:
        save.write(img.content)
        save.close()


def accounting_for_downloads(url: str, keyword: str, headers: dict) -> int:
    '''
    Функция загружает и подсчитывает количество загруженных изображений по указанному поискового запроса
    '''
    imgs = get_images_urls(url, keyword, headers)
    num = 0
    for img in imgs:
        download_one_image(img, keyword, num)
        num += 1
    return num


def image_download(url: str, path: str, keywords: list, headers: dict) -> None:
    '''
    Функция вызывающая остальные функции и оповещающая о том, по какому запросу произодится парсинг
    и сколько изображений было скачано по итогу
    '''
    os.chdir(path)
    if not os.path.isdir("dataset"):
        try:
            os.mkdir("dataset")
        except PermissionError:
            print("Insufficient permissions to create a directory on the specified path")
    os.chdir("dataset")
    for i in range(len(keywords)):
        print(keywords[i])
        amount = accounting_for_downloads(url, keywords[i], headers)
        print(f"{amount} images of a {keywords[i]} have been downloaded")


if __name__ == "__main__":
    path = "C:/Users/user/Desktop"
    keywords = ["polar bear", "brown bear"]
    image_download(URL, path, keywords, HEADERS)
