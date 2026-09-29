from urllib.parse import urlsplit
from extractpagedata import extract_page_data
import aiohttp
import asyncio


def normalize_url(url):
    object = urlsplit(url)
    normalized_url = object.netloc + object.path
    normalized_url_lwr = normalized_url.rstrip('/').lower()

    return normalized_url_lwr


async def crawl_site_async(base_url, max_concurrency, max_pages):

    base_domain = urlsplit(base_url).netloc


    async with AsyncCrawler(base_url, base_domain, max_concurrency, max_pages) as crawler:
        page_data = await crawler.crawl()
        return page_data


#### OLD
#def get_html(url):
#    try:
#        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
#    except:
#        raise Exception("burning PC")
#
#    if response.status_code >= 400:
#        raise Exception("Request error")
#    if "text/html" not in response.headers.get("Content-Type", ""):
#        raise Exception("Bad type")
#
#    return response.text


#def crawl_page(base_url, current_url=None, page_data=None):
#    if page_data == None:
#        page_data = {}

#    if current_url == None:
#       current_url = base_url

#    base_netloc = urlsplit(base_url).netloc
#    current_netloc = urlsplit(current_url).netloc

#    if base_netloc != current_netloc:
#        return page_data

#    normalized_url = normalize_url(current_url)

#    if normalized_url in page_data:
#        return page_data

#    try:
#        html = get_html(current_url)
#        print(f"crawling {current_url}")
#    except Exception as e:
#        print(f"Error fetching {current_url}: {e}")
#        return page_data

#    extracted_data = extract_page_data(html, current_url)
#    page_data[normalized_url] = extracted_data

#    for link in extracted_data["outgoing_links"]:
#        crawl_page(base_url, link, page_data)

#    return page_data









class AsyncCrawler:
    def __init__(self, base_url, base_domain, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = base_domain
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session =  None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()


    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        if self.should_stop == True:
            return False

        async with self.lock:

            if normalized_url in self.visited:
                return False

            if  len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False

            self.visited.add(normalized_url)
            return True



    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:

                if response.status >= 400:
                    raise Exception("Request error")
                if "text/html" not in response.headers.get("Content-Type", ""):
                    raise Exception("Bad type")

                html = await response.text()

                return html

        except:
            raise Exception("burning PC")




    async def crawl_page(self,current_url):
        if self.should_stop == True:
            return

        try:
            normalized_url = normalize_url(current_url)

            base_netloc = urlsplit(self.base_url).netloc
            current_netloc = urlsplit(current_url).netloc

            if base_netloc != current_netloc:
                return

            is_new = await self.add_page_visit(normalized_url)

            if is_new == False:
                return

            async with self.semaphore:
                print(f"crawling {current_url}")
                html = await self.get_html(current_url)
                extracted_data = extract_page_data(html, current_url)
                async with self.lock:
                    self.page_data[normalized_url] = extracted_data
                outgoing_links = extracted_data["outgoing_links"]

                local_list = []
                for link in outgoing_links:
                    task = asyncio.create_task(self.crawl_page(link))
                    local_list.append(task)
                    self.all_tasks.add(task)

                await asyncio.gather(*local_list)
        finally:
            self.all_tasks.discard(asyncio.current_task())



    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
