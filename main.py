import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_images_urls (url, keyword):
    page = 1
    url_list = []
    while True:
        url_page = f"{url}search?p={page}&text={keyword}"
        headers = {"User-Agent":"Mozilla/5.0"}
        html_page = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(html_page.content, "html.pasrer")
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                continue
            img_url = urljoin(url_page, img_url)
        page += 1
        if len(url_list) > 1500:
            break
    return url_list

def download_one_image (url, path, num):
    if not os.path.isdir(path):
        os.mkdir(path)
    img = requests.get(url)
    file = os.path.join(f"{path}/{str(num).zfill(4).jpg}")
    save = open(file, "wb")
    save.write(img.content)
    save.close()
