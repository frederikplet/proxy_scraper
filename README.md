# Proxy scraper

Proxy Scraper is a powerful tool that enables efficient scraping of proxy information from various websites. Currently, our tool supports the following websites:

https://free-proxy-list.net/
https://www.proxy-list.download/
https://www.us-proxy.org/
https://proxyscrape.com/
https://advanced.name/

Our roadmap includes plans for expanding the list of supported websites in the future to provide even more comprehensive results.

## Getting Started
To start using the Proxy Scraper, make sure you have Python 3.7 or later installed on your machine. You can verify your Python version by using the python --version command in your terminal.

After ensuring your Python installation, clone the Proxy Scraper repository to your local machine, then move to the proxy-scraper directory. To install the necessary packages, use pip install -r requirements.txt in your terminal.

## Usage
Code examples can be found in main.py

Importing specific scraper
If you want to scrape a specific website, you can import the respective module. For instance, you can use the following line in your Python file.
```
from scraper import proxylistdownload, freeproxylist, usproxy, proxyscrape, advancedname
``` 


To scrape all supported websites at once, import and use the scrape_all function. This will help you collect all proxies from all the websites.

```
from scraper import scrape_all

def scrape():
    proxies = scrape_all()
    print("Total proxies fetched:", len(proxies))
    return proxies

proxies = scrape()
```

Please note that all scraper functions return a dictionary with the data scraped.

If you need to send a request through a proxy server, there's a function which is shown below that does that.

```
import asyncio
from scraper import proxy_request

async def request(url):
    result = await proxy_request(url)
    print(result)

url = 'https://www.google.com/'

asyncio.run(request(url))
```


## Future Improvements
We continually develop and enhance the Proxy Scraper tool. Future improvements will include support for additional proxy websites.


## Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

## requirements.txt

I am sorry for the missing requirements file, there are some errors generating it.