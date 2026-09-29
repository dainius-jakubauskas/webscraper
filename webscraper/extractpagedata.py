from typing import TypedDict
from linksimages import get_urls_from_html, get_images_from_html
from heading import get_heading_from_html, get_first_paragraph_from_html

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def extract_page_data(html: str, page_url: str) -> PageData:

    data : PageData = {

    "url":   page_url,
    "heading":  get_heading_from_html(html),
    "first_paragraph" : get_first_paragraph_from_html(html),
    "outgoing_links" : get_urls_from_html(html, page_url),
    "image_urls" : get_images_from_html(html, page_url),

    }

    return data
