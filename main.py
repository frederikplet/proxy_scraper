# If you want to send a request to a website through a proxy server
import asyncio
from scraper import proxy_request

async def request(url):
    result = await proxy_request(url)
    print(result)

url = 'https://www.google.com/'
asyncio.run(request(url))



# If you want to get a list of proxies
from scraper import scrape_all

def scrape():
    proxies = scrape_all()
    print("Total proxies fetched:", len(proxies))
    return proxies

proxies = scrape()



# If you want to scrape a specific website
from scraper import freeproxylist

def specific_website():
    proxies = freeproxylist()
    print("Total proxies fetched from freeproxylist:", len(proxies))
    return proxies

proxies = specific_website()