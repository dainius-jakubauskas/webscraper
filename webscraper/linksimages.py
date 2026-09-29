from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

def get_urls_from_html(html, base_url):
    link_list = []
    soup = BeautifulSoup(html, 'html.parser')

    link = soup.find_all("a")
    for element in link:
        x = element.get("href")
        if x:
            link_list.append(urljoin(base_url, x))
        else:
            continue

    return link_list




def get_images_from_html(html, base_url):
    image_list = []
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find_all("img")
    for element in images:
        y = element.get("src")
        if y:
            image_list.append(urljoin(base_url, y))
        else:
            continue

    return image_list
