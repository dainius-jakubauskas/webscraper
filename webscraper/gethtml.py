import requests



def get_html(url):
    try:

        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    except:
        raise Exception("burning PC")

        if response.status_code >= 400:
            raise Exception("Request error")
        if "text/html" not in response.headers.get("Content-Type", ""):
            raise Exception("Bad type")

        return response.text
