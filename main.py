import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_images_urls (url, keyword):
    page = 1
    url_list = []
    while True:
        url_page = f"{url}search?p={page}&text={keyword}"
        html_page = requests.get(url_page, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(html_page.content, "html.parser")
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                continue
            img_url = urljoin(url_page, img_url)
            if is_valid(img_url):
                url_list.append(img_url)
        page += 1
        if len(url_list) > 1000:
            break
    return url_list

def download_one_image (url, path, num):
    if not os.path.isdir(path):
        os.mkdir(path)
    img = requests.get(url)
    file = f"{path}/{str(num).zfill(4)}.jpg"
    save = open(file, "wb")
    save.write(img.content)
    save.close()

def images_count (url, keyword):
    imgs = get_images_urls(url, keyword)
    num = 0
    for img in imgs:
        download_one_image(img, keyword, num)
        num += 1
    return num

def image_download (url, path, keywords):
    os.chdir(path)
    if not os.path.isdir("dataset"):
        os.mkdir("dataset")
    os.chdir("dataset")
    for i in range(len(keywords)):
        print(keywords[i])
        amount = images_count(url, keywords[i])
        print(f"{amount} images of a {keywords[i]} have been downloaded")

if __name__ == "__main__":
    url = "https://yandex.ru/images/"
    path = "C:/Users/mrney/Desktop"
    keywords = ["polar bear", "brown bear"]
    image_download(url, path, keywords)