import sys
from crawl import crawl_site_async
import asyncio
import json
from json_report import write_json_report


async def main():
    if  len(sys.argv) == 4:
        print(f"starting crawl of: {sys.argv[1]}")
    elif len(sys.argv) < 4:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    url = sys.argv[1]
    mx_concurrency = int(sys.argv[2])
    mx_pages = int(sys.argv[3])


    page_data = await crawl_site_async(url, mx_concurrency, mx_pages)
    print(f"Total pages: {len(page_data)}")

    write_json_report(page_data)

    #for item in page_data.values():
    #    print(item)



####################
if __name__ == "__main__":
    asyncio.run(main())
